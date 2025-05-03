import re
import httpx
from pathlib import Path
from bs4 import BeautifulSoup


def get_card_sets():
    CARD_LIST_URL = "https://en.onepiece-cardgame.com/cardlist/?series=569001"
    response = httpx.get(CARD_LIST_URL)

    bsoup = BeautifulSoup(response.text, "lxml")
    options = bsoup.css.select("#series option", recursive=False)
    # print(f"Found {len(options)} options.")

    card_sets = []
    for option in options:
        # print(f"Option: {option}\nValue: {option['value']}\nContents: {option.contents}")
        if "ALL" in option.contents or "Recording" in option.contents:
            continue
        card_sets.append({
            "id": option["value"],
            "name": option.contents[0].replace('<br class="spInline">', ''),
        })

    return card_sets


def get_card_set_images(card_set):
    BASE_URL = "https://en.onepiece-cardgame.com"
    DECK_URL = f"https://en.onepiece-cardgame.com/cardlist/?series={card_set['id']}"

    response = httpx.get(DECK_URL)
    bsoup = BeautifulSoup(response.text, "lxml")
    images = bsoup.css.select("div.resultCol a img", recursive=False)

    image_urls = [img["data-src"][2:] for img in images]

    for i, image_url in enumerate(image_urls):
        question_mark_i = image_url.find("?")
        image_urls[i] = f"{BASE_URL}/{image_url[:question_mark_i]}"
        print(image_urls[i])

    pattern = re.compile(r"\[.+\]")
    match = pattern.search(card_set["name"])
    set_dir_name = match.group() if match else card_set["name"]

    print(f"Cards: {len(image_urls)}")
    print(f"Creating directory '{set_dir_name}'")

    set_dir = Path(set_dir_name)
    set_dir.mkdir(exist_ok=True)

    for image_url in image_urls:
        response = httpx.get(image_url)

        last_slash_i = image_url.rfind("/")
        image_name = image_url[last_slash_i + 1:]

        with open(set_dir / image_name, "wb") as image_file:
            image_file.write(response.content)


def show_ui(card_sets):
    print("One Piece TCG Deck Generator")
    for i, card_set in enumerate(card_sets):
        print(f"{i}: {card_set['name']}")

    has_error = False
    option = input("Select a card set: ")
    try:
        option = int(option)
        card_set = card_sets[option]
    except ValueError:
        has_error = True
        print(f"Error casting the value '{option}'")
    except IndexError:
        has_error = True
        print(f"Invalid option '{option}'")
    finally:
        if has_error:
            exit()
    get_card_set_images(card_set)


card_sets = get_card_sets()
show_ui(card_sets)

