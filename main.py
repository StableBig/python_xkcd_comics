import requests
from dotenv import load_dotenv
import os
from telegram import Bot
import asyncio
import random


def load_environment_variables():
    load_dotenv()
    return os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID")


def get_latest_comic_number():
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    latest_comic_info = response.json()
    return latest_comic_info['num']


def get_random_comic_info(latest_comic_num):
    random_comic_num = random.randint(1, latest_comic_num)
    url = f"https://xkcd.com/{random_comic_num}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    random_comic_info = response.json()
    return {
        'num': random_comic_num,
        'img_url': random_comic_info['img'],
        'alt_text': random_comic_info['alt']
    }


def download_comic_image(image_url, filename="xkcd_comic.png"):
    response = requests.get(image_url)
    response.raise_for_status()
    with open(filename, "wb") as file:
        file.write(response.content)
    return filename


async def send_telegram_photo(telegram_bot_token, telegram_chat_id, comic_filename, comic_caption):
    bot = Bot(token=telegram_bot_token)
    with open(comic_filename, "rb") as comic_file:
        await bot.send_photo(
            chat_id=telegram_chat_id,
            photo=comic_file,
            caption=comic_caption
        )
    print(f"Комикс отправлен в Telegram!")


def delete_local_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Файл {filename} успешно удалён.")
    else:
        print(f"Файл {filename} не найден.")


def main():
    telegram_bot_token, telegram_chat_id = load_environment_variables()
    latest_comic_num = get_latest_comic_number()
    random_comic_info = get_random_comic_info(latest_comic_num)
    comic_filename = download_comic_image(random_comic_info['img_url'])

    asyncio.run(send_telegram_photo(
        telegram_bot_token=telegram_bot_token,
        telegram_chat_id=telegram_chat_id,
        comic_filename=comic_filename,
        comic_caption=f"#{random_comic_info['num']}: {random_comic_info['alt_text']}"
    ))

    delete_local_file(comic_filename)


if __name__ == "__main__":
    main()
