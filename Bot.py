import os
import discord
import random
from discord.ext import commands
from flask import Flask # Cần thêm thư viện này
from threading import Thread

# --- ĐOẠN CODE CẦN THÊM VÀO ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot đang chạy!"

def run_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_server).start()
# --- HẾT ĐOẠN CODE CẦN THÊM ---

# Cấu hình intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} đã sẵn sàng!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() in ['chào', 'hi']:
        cau_tra_loi = [
            'Chào bạn',
            'Chào thằng gay',
            'Chào thằng lồn <:0GDroolingCat:1525444808972308540>'
        ]
        phan_hoi = random.choice(cau_tra_loi)
        await message.channel.send(phan_hoi)

    await bot.process_commands(message)

# Đảm bảo bạn đã thêm biến môi trường DISCORD_TOKEN trong Render Settings
bot.run(os.environ['DISCORD_TOKEN'])
