import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://en.onepiece-cardgame.com"
DECK_URL = "https://en.onepiece-cardgame.com/cardlist/?series=569110"

response = httpx.get(DECK_URL)
print(response.status_code)

bsoup = BeautifulSoup(response.text, "lxml")
images = bsoup.css.select("div.resultCol a img", recursive=False)

image_urls = [img["data-src"][2:] for img in images]


# images = images.filter(lambda img: "dummy.gif" not in img, images)
#
for image_url in image_urls:
    print("/".join([BASE_URL, image_url]))

