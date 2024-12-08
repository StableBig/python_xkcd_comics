import requests
from dotenv import load_dotenv
import os
from telegram import Bot
import asyncio
import random

load_dotenv()

telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

latest_comic_url = "https://xkcd.com/info.0.json"

response = requests.get(latest_comic_url)
response.raise_for_status()

latest_comic_data = response.json()
latest_comic_num = latest_comic_data['num']

random_comic_num = random.randint(1, latest_comic_num)

random_comic_url = f"https://xkcd.com/{random_comic_num}/info.0.json"

response = requests.get(random_comic_url)
response.raise_for_status()

comic_data = response.json()
comic_image_url = comic_data['img']
comic_alt_text = comic_data['alt']

image_response = requests.get(comic_image_url)
image_response.raise_for_status()

comic_filename = "xkcd_comic.png"
with open(comic_filename, "wb") as file:
    file.write(image_response.content)


async def send_telegram_photo():
    bot = Bot(token=telegram_bot_token)
    with open(comic_filename, "rb") as comic_file:
        await bot.send_photo(
            chat_id=telegram_chat_id,
            photo=comic_file,
            caption=f"#{random_comic_num}: {comic_alt_text}"
        )
    print(f"Комикс #{random_comic_num} отправлен в Telegram!")


asyncio.run(send_telegram_photo())

if os.path.exists(comic_filename):
    os.remove(comic_filename)
    print(f"Файл {comic_filename} успешно удалён.")
else:
    print(f"Файл {comic_filename} не найден.")
