import os
import discord
import random
from datetime import datetime
from discord.ext import commands
from flask import Flask
from threading import Thread

# --- Cấu hình Server ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot đang chạy!"
Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))).start()

# --- Biến lưu trữ (Tạm thời) ---
inventory = {}     # {user_id: số_coin}
daily_check = {}   # {user_id: ngày_nhận}

# --- Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} đã sẵn sàng!')

@bot.event
async def on_message(message):
    if message.author == bot.user: return
    
    content = message.content.lower().strip()
    user_id = str(message.author.id)

    # 1. Lệnh nhelp
    if content == 'nhelp':
        await message.channel.send("📋 **Danh sách lệnh:**\n`ncauca`: Câu cá (tự động bán lấy coin)\n`nme`: Xem số dư coin của bạn\n`ndaily`: Nhận coin mỗi ngày\n`chào/hi`: Chào bot\n`béo`: Gọi tên người bạn béo")

    # 2. Lệnh ndaily
    elif content == 'ndaily':
        today = datetime.now().strftime("%Y-%m-%d")
        if daily_check.get(user_id) == today:
            await message.channel.send("Bạn đã nhận quà hôm nay rồi, mai quay lại nhé!")
        else:
            thuong = random.randint(1, 50)
            inventory[user_id] = inventory.get(user_id, 0) + thuong
            daily_check[user_id] = today
            await message.channel.send(f"Bạn nhận được {thuong} coin làm vốn khởi nghiệp! Tổng số dư: {inventory[user_id]} coin.")

    # 3. Lệnh ncauca (tự động cộng tiền vào số dư)
    elif content == 'ncauca':
        if random.random() < 0.3:
            rac = ['một chiếc dép cũ', 'một cái áo rách', 'một mớ rác thải']
            await message.channel.send(f'Bạn quăng cần xuống... và câu được {random.choice(rac)}. Chán thế!')
        else:
            so_ca = random.randint(1, 50)
            inventory[user_id] = inventory.get(user_id, 0) + so_ca
            await message.channel.send(f'Bạn câu được {so_ca} con cá và bán được {so_ca} coin! Tổng số dư: {inventory[user_id]} coin.')

    # 4. Lệnh nme (xem số dư)
    elif content == 'nme':
        so_du = inventory.get(user_id, 0)
        await message.channel.send(f"💰 **Số dư của bạn:** {so_du} coin.")

    # 5. Phản hồi
    elif content in ['chào', 'hi']:
        await message.channel.send(random.choice(['Chào bạn', 'Chào thằng gay', 'Chào thằng lồn <:0GDroolingCat:1525444808972308540>']))
    elif content == 'béo':
        await message.channel.send('<@1517328324618096711>')

    await bot.process_commands(message)

bot.run(os.environ['DISCORD_TOKEN'])
