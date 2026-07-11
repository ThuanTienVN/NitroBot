import os
import discord
import random
from discord.ext import commands

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

    if message.content.lower() == 'chào':
        # Danh sách các câu trả lời
        cau_tra_loi = [
            'Chào bạn', 
            'Chào thằng gay',
            'Chào thằng lồn <:OGDroolingCat:1525444808972308540>'
        ]
        # Chọn ngẫu nhiên 1 câu trong danh sách
        phan_hoi = random.choice(cau_tra_loi)
        await message.channel.send(phan_hoi)

    await bot.process_commands(message)
# Thay bằng Token thật của bạn
bot.run(os.environ['DISCORD_TOKEN'])