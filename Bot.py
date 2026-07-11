import os
import discord
import random
import json
from discord.ext import commands
from flask import Flask
from threading import Thread

# ==========================
# Server ảo
# ==========================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot đang chạy!"

def run_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_server).start()

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

# ==========================
# Sự kiện
# ==========================
@bot.event
async def on_ready():
    print(f"{bot.user} đã sẵn sàng!")

@bot.event
async def on_message(message):
    # Không trả lời bot
    if message.author.bot:
        return

    content = message.content.lower().strip()
    user_id = str(message.author.id)

    # ==========================
    # Chào
    # ==========================
    if content in ["chào", "hi"]:
        replies = [
            "Chào bạn",
            "Chào thằng gay",
            "Chào thằng lồn <:0GDroolingCat:1525444808972308540>"
        ]
        await message.channel.send(random.choice(replies))
        return

    # ==========================
    # Béo
    # ==========================
    if content == "béo":
        await message.channel.send("<@1517328324618096711>")
        return

    # ==========================
    # Câu cá
    # ==========================
    if content == "ncauca":
        inventory = load_data()

        # 30% rác
        if random.random() < 0.3:
            rac = [
                "một chiếc dép cũ",
                "một cái áo rách",
                "một mớ rác thải",
                "một chiếc vớ thối"
            ]

            await message.channel.send(
                f"🎣 Bạn quăng cần xuống và câu được **{random.choice(rac)}**.\n"
                "Đúng là đen đủi!"
            )
            return

        # 70% cá
        so_luong = random.randint(1, 50)

        inventory[user_id] = inventory.get(user_id, 0) + so_luong
        save_data(inventory)

        await message.channel.send(
            f"🎣 Bạn quăng cần xuống và câu được **{so_luong}** con cá!\n"
            f"🐟 Hiện bạn có **{inventory[user_id]}** con cá."
        )
        return

    # ==========================
    # Xem kho cá
    # ==========================
    if content == "nfish":
        inventory = load_data()
        tong_ca = inventory.get(user_id, 0)

        await message.channel.send(
            f"🐟 Bạn đang sở hữu **{tong_ca}** con cá."
        )
        return

    # Cho phép command khác hoạt động
    await bot.process_commands(message)

# ==========================
# Chạy bot
# ==========================
bot.run(os.environ["DISCORD_TOKEN"])
