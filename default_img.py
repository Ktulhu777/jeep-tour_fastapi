from PIL import Image, ImageDraw, ImageFont

from random import choice

color = ('red', 'green', 'pink', 'blue', 'violet')
ImageFont.load_default()
font = ImageFont.truetype("PS.ttf", size=500)


def make_default_png(username):
    with Image.new('RGB', (640, 640), color=choice(color)) as img:
        filename = f'ava_{username}.png'
        text_draw = ImageDraw.Draw(img)
        text_draw.text((170.0, 10.0), username[0].upper(), font=font)
        img.save(filename)
        return filename



