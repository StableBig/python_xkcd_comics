import requests
from dotenv import load_dotenv
import os

load_dotenv()
client_id = os.getenv("CLIENT_ID")

print(f"Ваш client_id: {client_id}")

comic_url = "https://xkcd.com/353/info.0.json"

response = requests.get(comic_url)
response.raise_for_status()

comic_data = response.json()
comic_image_url = comic_data['img']
comic_alt_text = comic_data['alt']

image_response = requests.get(comic_image_url)
image_response.raise_for_status()

with open("xkcd_comic.png", "wb") as file:
    file.write(image_response.content)

print("Комментарий к комиксу:", comic_alt_text)
print("Комикс скачан и сохранён как xkcd_comic.png")
