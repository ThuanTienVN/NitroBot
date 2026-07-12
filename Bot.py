import os
import discord
import random
from datetime import datetime, timedelta
from discord.ext import commands
from flask import Flask
from threading import Thread

# --- Cấu hình Server ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot đang chạy!"
Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))).start()

# --- Biến lưu trữ ---
inventory = {}     # {user_id: số_coin}
fish_storage = {}  # {user_id: số_cá_đang_có}
daily_check = {}   # {user_id: ngày_nhận}
cooldown_check = {} # {user_id: thời_gian_câu_tiếp_theo}

# --- Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_message(message):
    if message.author == bot.user: return
    
    content = message.content.lower().strip()
    user_id = str(message.author.id)
    now = datetime.now()

    # 1. Lệnh nhelp
    if content == 'nhelp':
        await message.channel.send("📋 **Danh sách lệnh:**\n`ncauca`: Câu cá (Cooldown 3p)\n`nfish`: Xem số cá chưa bán\n`nbanca`: Bán toàn bộ cá lấy coin\n`nme`: Xem số dư coin\n`ndaily`: Nhận coin mỗi ngày\n`nsanggay`: Phản hồi đặc biệt")

  # 2. Lệnh ncauca (Cooldown 3 phút, có tag người dùng)
    elif content == 'ncauca':
        last_time = cooldown_check.get(user_id)
        if last_time and now < last_time:
            wait_time = int((last_time - now).total_seconds() / 60) + 1
            await message.channel.send(f"{message.author.mention} Bạn đang thấm mệt, hãy nghỉ ngơi {wait_time} phút nữa rồi quay lại nhé!")
        else:
            if random.random() < 0.3:
                rac = ['một chiếc dép cũ', 'một cái áo rách', 'một mớ rác thải']
                await message.channel.send(f'{message.author.mention} Bạn quăng cần xuống... và câu được {random.choice(rac)}. Chán thế!')
            else:
                so_ca = random.randint(1, 10)
                fish_storage[user_id] = fish_storage.get(user_id, 0) + so_ca
                await message.channel.send(f'{message.author.mention} Bạn câu được {so_ca} con cá! Dùng `nbanca` để bán nhé.')
            
            cooldown_check[user_id] = now + timedelta(minutes=3)

    # 3. Lệnh nfish (Xem cá)
    elif content == 'nfish':
        so_ca = fish_storage.get(user_id, 0)
        await message.channel.send(f"🐟 Bạn đang có {so_ca} con cá trong kho.")

    # 4. Lệnh nbanca (Bán cá)
    elif content == 'nbanca':
        so_ca = fish_storage.get(user_id, 0)
        if so_ca > 0:
            coin = so_ca * 5  # Giả sử giá bán là 5 coin/con
            inventory[user_id] = inventory.get(user_id, 0) + coin
            fish_storage[user_id] = 0
            await message.channel.send(f"Bạn đã bán {so_ca} con cá và nhận được {coin} coin! Tổng số dư: {inventory[user_id]} coin.")
        else:
            await message.channel.send("Bạn không có cá để bán!")

    # 5. Lệnh nme
    elif content == 'nme':
        so_du = inventory.get(user_id, 0)
        await message.channel.send(f"💰 **Số dư của bạn:** {so_du} coin.")

    # 6. Lệnh ndaily
    elif content == 'ndaily':
        today = datetime.now().strftime("%Y-%m-%d")
        if daily_check.get(user_id) == today:
            await message.channel.send("Bạn đã nhận quà hôm nay rồi, mai quay lại nhé!")
        else:
            thuong = random.randint(1, 50)
            inventory[user_id] = inventory.get(user_id, 0) + thuong
            daily_check[user_id] = today
            await message.channel.send(f"Bạn nhận được {thuong} coin! Tổng số dư: {inventory[user_id]} coin.")

    # 7. Lệnh nsanggay
    elif content == 'nsanggay':
        await message.channel.send("cái gì v mẹ <:0GDroolingCat:1525444808972308540>")

    await bot.process_commands(message)

bot.run(os.environ['DISCORD_TOKEN'])
