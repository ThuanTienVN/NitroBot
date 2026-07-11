import os
import discord
import random
import json
from discord.ext import commands
from flask import Flask
from threading import Thread

# ==========================
# Cấu hình Server ảo
# ==========================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot đang chạy!"

# ==========================
# Lưu dữ liệu
# ==========================
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

# ==========================
# Discord Bot
# ==========================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

cooldown_users = set()

# ==========================
# Bot Ready
# ==========================
@bot.event
async def on_ready():
    print("======================")
    print("BOT ONLINE")
    print(f"User : {bot.user}")
    print(f"ID   : {bot.user.id}")
    print("======================")

# ==========================
# Nhận tin nhắn
# ==========================
@bot.event
async def on_message(message):

    if message.author.bot:
        return

    content = message.content.lower().strip()
    user_id = str(message.author.id)

    # ----------------------
    # Chào
    # ----------------------
    if content in ["chào", "hi"]:
        cau_tra_loi = [
            "Chào bạn",
            "Chào thằng gay",
            "Chào thằng lồn <:0GDroolingCat:1525444808972308540>"
        ]
        await message.channel.send(random.choice(cau_tra_loi))
        return

    # ----------------------
    # Béo
    # ----------------------
    elif content == "béo":
        await message.channel.send("<@1517328324618096711>")
        return

    # ----------------------
    # Câu cá
    # ----------------------
    elif content == "ncauca":

        inventory = load_data()

        if random.random() < 0.3:

            rac = [
                "một chiếc dép cũ",
                "một cái áo rách",
                "một mớ rác thải",
                "một chiếc vớ thối"
            ]

            ket_qua = (
                f"Bạn quăng cần xuống... và câu được "
                f"{random.choice(rac)}. Chán thế!"
            )

        else:

            so_luong = random.randint(1, 50)

            inventory[user_id] = inventory.get(user_id, 0) + so_luong

            save_data(inventory)

            ket_qua = (
                f"Bạn quăng cần xuống và câu được "
                f"{so_luong} con cá! "
                f"Tổng số cá trong kho là: "
                f"{inventory[user_id]} con."
            )

        await message.channel.send(ket_qua)
        return

    # ----------------------
    # Xem kho cá
    # ----------------------
    elif content == "nfish":

        inventory = load_data()

        tong_ca = inventory.get(user_id, 0)

        await message.channel.send(
            f"Bạn đang sở hữu tổng cộng {tong_ca} con cá. Tiếp tục đi câu nhé!"
        )
        return

    await bot.process_commands(message)

# ==========================
# Chạy Bot
# ==========================
bot.run(os.environ["DISCORD_TOKEN"])
