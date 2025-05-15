import re
import httpx
from PIL import Image, ImageColor
from pathlib import Path
from bs4 import BeautifulSoup
from PyQt6.QtWidgets import QApplication
from gui import MainWindow


def main():
    # Can pass sys.argv if gui program accepts CLI arguments.
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

    exit()

    card_sets = get_card_sets()
    show_ui(card_sets)


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
        print(f"Found image {i+1}: {image_urls[i]}")

    pattern = re.compile(r"\[.+\]")
    match = pattern.search(card_set["name"])
    set_dir_name = match.group() if match else card_set["name"]

    print(f"Total cards: {len(image_urls)}")

    set_dir = Path(set_dir_name)
    if not set_dir.exists():
        print(f"Creating directory '{set_dir_name}'")
    set_dir.mkdir(exist_ok=True)

    images = []
    for image_url in image_urls:
        last_slash_i = image_url.rfind("/")
        image_name = image_url[last_slash_i + 1:]

        image_path = set_dir / image_name
        images.append(image_path)
        if image_path.exists():
            print(f"Skipping download of '{image_path.name}' already exists.")
            continue

        try:
            print(f"Downloading '{image_path.name}'... ", end="")
            response = httpx.get(image_url)
            print("Done.")
            with open(image_path, "wb") as image_file:
                print(f"Creating '{image_path.name}'... ", end="")
                image_file.write(response.content)
                print("Done.")
        except Error as e:
            print(f"Error downloading file: {e}")
    return images


def create_card_deck_image(image_paths):
    print("Creating deck image.. ")
    example_image = Image.open(image_paths[0])

    IMAGE_COUNT = len([f for f in image_paths[0].parent.iterdir()])
    IMAGE_WIDTH = example_image.width * 10
    IMAGE_HEIGHT = example_image.height * (int(IMAGE_COUNT / 10) + 1)
    deck_image = Image.new("RGBA", (IMAGE_WIDTH, IMAGE_HEIGHT), "#00000000")

    col_offset = 0
    row_offset = 0
    for image_path in image_paths:
        image = Image.open(image_path)

        col = image.width * col_offset
        row = image.height * row_offset
        deck_image.paste(image, (col, row))

        if col_offset != 0 and col_offset % 10 == 0:
            col_offset = 0
            row_offset += 1
        else:
            col_offset += 1

    deck_image.save(image_paths[0].parent / "deck.png")
    print("Finished creating deck.")


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
    images = get_card_set_images(card_set)
    create_card_deck_image(images)


if __name__ == "__main__":
    main()

