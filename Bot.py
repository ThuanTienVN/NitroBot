import os
import discord
import random
import json
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

# --- Cấu hình lưu trữ dữ liệu ---
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Tạo một set để lưu user đang "đợi" (tránh spam/lặp)
cooldown_users = set()

@bot.event
async def on_ready():
    print(f'Bot {bot.user} đã sẵn sàng!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower().strip() # .strip() để xóa khoảng trắng thừa
    user_id = str(message.author.id)

    # Lệnh chào/hi
    if content in ['chào', 'hi']:
        cau_tra_loi = ['Chào bạn', 'Chào thằng gay', 'Chào thằng lồn <:0GDroolingCat:1525444808972308540>']
        await message.channel.send(random.choice(cau_tra_loi))
    
    # Lệnh béo
    elif content == 'béo':
        await message.channel.send('<@1517328324618096711>')

    # Lệnh ncauca với cơ chế chống lặp
    elif content == 'ncauca':
        if user_id in cooldown_users:
            return # Bỏ qua nếu user đang spam hoặc bot đang xử lý
        
        cooldown_users.add(user_id)
        
        inventory = load_data()
        if random.random() < 0.3:
            rac = ['một chiếc dép cũ', 'một cái áo rách', 'một mớ rác thải', 'một chiếc vớ thối']
            await message.channel.send(f'Bạn quăng cần xuống... và câu được {random.choice(rac)}. Chán thế!')
        else:
            so_luong = random.randint(1, 50)
            inventory[user_id] = inventory.get(user_id, 0) + so_luong
            save_data(inventory)
            await message.channel.send(f'Bạn quăng cần xuống và câu được {so_luong} con cá! Tổng số cá trong kho là: {inventory[user_id]} con.')
        
        cooldown_users.remove(user_id) # Xóa khỏi danh sách để lần sau câu tiếp được

    # Lệnh nfish
    elif content == 'nfish':
        inventory = load_data()
        tong_ca = inventory.get(user_id, 0)
        await message.channel.send(f'Bạn đang sở hữu tổng cộng {tong_ca} con cá. Tiếp tục đi câu nhé!')

    await bot.process_commands(message)

bot.run(os.environ['DISCORD_TOKEN'])
