from PIL import Image, ImageDraw, ImageFont
from random import choice

color = ('red', 'green', 'pink', 'blue', 'violet')
font = ImageFont.load_default()


def make_default_png(username):
    with Image.new('RGB', (640, 640), color=choice(color)) as img:
        filename = f'ava_{username}.png'
        text_draw = ImageDraw.Draw(img)
        text_draw.text((270, 60), username[0].upper(), font=font)
        img.save(filename)
        return filename



