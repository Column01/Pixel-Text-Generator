# Pixel-Text-Generator
A simple script using PIL to convert text into a pixel-text representation image

## Pre-requisites

- `pip install pillow numpy`

## Usage

- Place your text in a `.txt` file, and copy the path to that file.
    - Newlines will **not** be preserved, they are removed in pre-processing.
- `python main.py --width 80 --path input.txt`
- The image is saved as `output.png` in the program folder

## Sample (enlarged)

<img width="158" height="54" alt="output" src="https://github.com/user-attachments/assets/05f702f9-f58a-4de6-be2f-3d16f7c1fb82" />

## Future ideas

- Text alignment options (centered, left or right aligned.)
- Simple UI with image preview