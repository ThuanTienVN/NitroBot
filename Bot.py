import os
import discord
import random
from discord.ext import commands
from flask import Flask
from threading import Thread

# --- Cấu hình Server ảo ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot đang chạy!"

def run_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_server).start()
# --- Hết phần cấu hình Server ---

# Cấu hình intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} đã sẵn sàng!')

@bot.event
async def on_message(message):
    # Tránh việc bot tự trả lời chính mình
    if message.author == bot.user:
        return

    content = message.content.lower()

    # Xử lý phản hồi cho "chào" hoặc "hi"
    if content in ['chào', 'hi']:
        cau_tra_loi = [
            'Chào bạn',
            'Chào thằng gay',
            'Chào thằng lồn <:0GDroolingCat:1525444808972308540>'
        ]
        phan_hoi = random.choice(cau_tra_loi)
        await message.channel.send(phan_hoi)
    
    # Xử lý phản hồi cho "béo"
    elif content == 'béo':
        phan_hoi = '<@1517328324618096711>'
        await message.channel.send(phan_hoi)

    # Lệnh ncauca không cần dấu !
    elif content == 'ncauca':
        # Tỉ lệ 30% ra rác, 70% ra cá
        if random.random() < 0.3:
            rac = ['một chiếc dép cũ', 'một cái áo rách', 'một mớ rác thải', 'một chiếc vớ thối']
            await message.channel.send(f'Bạn quăng cần xuống... và câu được {random.choice(rac)}. Chán thế!')
        else:
            diem = random.randint(1, 100)
            await message.channel.send(f'Bạn quăng cần xuống và câu được một con cá nặng {diem}kg! Wow!')

    # Quan trọng: Để bot vẫn nhận các lệnh ! khác (nếu bạn có dùng)
    await bot.process_commands(message)

# Đảm bảo đã thêm biến DISCORD_TOKEN trong Render Settings
bot.run(os.environ['DISCORD_TOKEN'])
