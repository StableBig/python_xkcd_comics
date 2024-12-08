import requests

comic_url = "https://xkcd.com/353/info.0.json"

response = requests.get(comic_url)
response.raise_for_status()

comic_data = response.json()
comic_image_url = comic_data['img']

image_response = requests.get(comic_image_url)
image_response.raise_for_status()

with open("xkcd_comic.png", "wb") as file:
    file.write(image_response.content)

print("Комикс скачан и сохранён как xkcd_comic.png")
