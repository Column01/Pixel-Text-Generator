import argparse
import json

import numpy as np

from PIL import Image


with open("mapping.json", "r", encoding="utf-8") as fp:
    mapping = json.load(fp)


padding = Image.new("RGB", (1, 8), (255, 255, 255))
space = Image.new("RGB", (3, 8), (255, 255, 255))


def create_word(word: str) -> tuple[Image.Image, int]:
    images: list[Image.Image] = []
    for i, char in enumerate(word):
        img_path = mapping.get(char, None)
        if img_path is not None:
            img = Image.open(img_path)
            images.append(img)
            # Skip padding for letters if the character is a lowercase "l" or if the character is before a lowercase "l"
            # It has two pixels of padding on either side already
            if char != "l":
                if len(word) > i + 1:
                    next_char = word[i + 1]
                    if next_char == "l":
                        continue
                images.append(padding)
        else:
            print(f"Character '{char}' not in text -> image mapping. Skipping...")

    width = sum([image.size[0] for image in images])
    height = max([image.size[1] for image in images])

    image = Image.new("RGB", (width, height), (255, 255, 255))
    cur_width = 0
    for img in images:
        image.paste(img, (cur_width, 0))
        cur_width += img.size[0]

    return image, width


def create_image(text: list[str], width=80):
    final: list[list[tuple[Image.Image, int]]] = []
    line: list[tuple[Image.Image, int]] = []
    longest_line = 0
    line_length = 0

    for word in text:
        if word == "":
            continue
        image_word, word_width = create_word(word)
        if line_length + word_width >= width:
            # Word is too long for this line, start a new line
            # Remove last empty space from the line
            if len(line) > 0:
                line.pop()
                final.append(line.copy())
                line.clear()
            # Add the first word to the new line
            line.append(image_word)
            line.append(space)
            line_length = word_width + space.size[0]
        else:
            # Add the word to the line
            line.append(image_word)
            line.append(space)
            line_length += word_width + space.size[0]

        # Compute the longest line
        longest_line = max(line_length, longest_line)

    # Add the last line we processed
    final.append(line)
    # Each line is 8px tall, but we also need to add a few extra lines for the padding
    height = len(final) * 8 + (len(final))

    width = longest_line

    # An empty line to space each line of text
    padding_line = Image.new("RGB", (width, 1), (255, 255, 255))

    # Create the final image of the correct dimensions
    final_image = Image.new("RGB", (width, height), (255, 255, 255))

    for i, line in enumerate(final):
        # Calculate the current line height (line count * 8px high + line count [padding lines])
        cur_height = (i * 8) + i

        # Add 1px padding between lines
        final_image.paste(padding_line, (0, cur_height))
        cur_height += 1

        # Add the line contents to the final image
        cur_width = 0
        for image in line:
            final_image.paste(image, (cur_width, cur_height))
            cur_width += image.size[0]

    return final_image


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Pixel-Text-Generator",
        description="Converts text into a pixel-text representation as an image.",
    )

    parser.add_argument(
        "--width", "-w", type=int, help="The max width in pixels as an integer."
    )
    parser.add_argument(
        "--path",
        "-p",
        type=str,
        help="A file path to a .txt file containing text to pixelize",
        required=True,
    )

    args = parser.parse_args()
    text = None

    if args.path:
        with open(args.path, "r", encoding="utf-8") as fp:
            text = fp.read()
            text = text.replace("\n", "").split(" ")

    print(f"Pixelizing the following text: \n{text}")
    image = create_image(text, args.width)
    image.save("output.png")

    arr = np.array(image)
    pixels = np.sum(np.all(arr == [0, 0, 0], axis=-1))
    print(f"\nTotal pixels required: {pixels}")
