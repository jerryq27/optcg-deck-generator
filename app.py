import httpx
from bs4 import BeautifulSoup


def get_card_lists():
    CARD_LIST_URL = "https://en.onepiece-cardgame.com/cardlist/?series=569001"
    response = httpx.get(CARD_LIST_URL)

    bsoup = BeautifulSoup(response.text, "lxml")
    options = bsoup.css.select("#series option", recursive=False)
    print(f"Found {len(options)} options.")

    card_sets = []
    for option in options:
        # print(f"Option: {option}\nValue: {option['value']}\nContents: {option.contents}")
        if "ALL" in option.contents or "Recording" in option.contents:
            continue
        card_sets.append({
            "id": option["value"],
            "name": option.contents[0],
        })

    for i, card_set in enumerate(card_sets):
        print(f"{i}: {card_set['id']} -> {card_set['name'].replace('<br class="spInline">', '')}")

get_card_lists()

exit()

BASE_URL = "https://en.onepiece-cardgame.com"
DECK_URL = "https://en.onepiece-cardgame.com/cardlist/?series=569110"

response = httpx.get(DECK_URL)
print(response.status_code)

bsoup = BeautifulSoup(response.text, "lxml")
images = bsoup.css.select("div.resultCol a img", recursive=False)

image_urls = [img["data-src"][2:] for img in images]

for image_url in image_urls:
    print("/".join([BASE_URL, image_url]))

print(f"Cards: {len(image_urls)}")
