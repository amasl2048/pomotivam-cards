#!/bin/env python3
import json
from PIL import Image, ImageDraw, ImageFont

from config import w, h, MARGIN, T_WIDTH, FS1, FS2, FS3

font_file1 = r"c:\windows\fonts\arial.ttf"
font_file2 = r"c:\windows\fonts\ariali.ttf"
font1 = ImageFont.truetype(font_file1, FS1)
font2 = ImageFont.truetype(font_file2, FS2)  # italic font
font3 = ImageFont.truetype(font_file1, FS3)


def read_photo(picture: str, photos: dict) -> None:

    if picture in photos.keys():
        return

    with Image.open("photo/%s.png" % picture) as photo:
        photo.thumbnail( (T_WIDTH, T_WIDTH), Image.LANCZOS)
        print(picture, photo.format, photo.mode, photo.info)
        photos[picture] = photo
        return


def light_color(color: tuple, delta: int) -> tuple:

    color_l = []
    for i in range(3):
        color_l.append(color[i] + delta)

    return tuple(color_l)


def print_json(data: dict) -> None:

    for key in data.keys():
        js = json.dumps(data[key], ensure_ascii=False, indent=4)
        print(js)


def draw_text(num: str, line: dict, photo, hash: str):

    color = tuple(line["color"])
    color_l = light_color(color, 40)

    image = Image.new("RGBA", (w, h), color)
    image.paste(photo, (int(w/12), int(h/2)), photo)

    draw = ImageDraw.Draw(image)
    draw.rectangle( (MARGIN, MARGIN, w-MARGIN, h-MARGIN), outline="white" )

    draw.text((w/2, h/3), line["text"] , font=font1, anchor="mm", align="center", fill="black")
    draw.text((w*2/3, h*2/3), line["author"], anchor="mm", align="right", font=font2,  fill="black")

    draw.text((w-MARGIN, MARGIN/2), "%03d %03d %03d" % color, anchor="rm", font=font3,  fill=color_l)
    draw.text((MARGIN, h-MARGIN/2), line["number"], anchor="lm", font=font3,  fill=color_l)
    draw.text((w-MARGIN, h-MARGIN/2), hash, anchor="rm", font=font3,  fill=color_l)

    # draw rotate text vertical
    VLEN = 100
    txt_img = Image.new('RGBA', (VLEN, MARGIN))
    d = ImageDraw.Draw(txt_img)
    d.text((0, MARGIN/2), line["link"], anchor="lm", font=font3, fill="white")
    vtext = txt_img.rotate(90, expand=1)
    image.paste(vtext, (w-MARGIN, h-VLEN-MARGIN), vtext)

    image.save("output-cards/%s.png" % num)


if __name__ == "__main__":

    with open("cardchain.json", "r") as f:
        chain = json.load(f)

    photos = {}

    for num in chain.keys():
        data = chain[num]["card"]["body"]
        picture = data["picture"]
        read_photo(picture, photos)
        hash_str = "%s..%s" % (chain[num]["card_hash"][0:4], chain[num]["card_hash"][60:])
        draw_text(num, data, photos[picture], hash_str)
