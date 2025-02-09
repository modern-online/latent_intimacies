#!/usr/bin/env python3
import time

from PIL import Image, ImageDraw, ImageFont

import st7789

display_type = "square"


# Create ST7789 LCD display class.

if display_type in ("square", "rect", "round"):
    disp = st7789.ST7789(
        height=135 if display_type == "rect" else 240,
        rotation=0 if display_type == "rect" else 90,
        port=0,
        cs=st7789.BG_SPI_CS_FRONT,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
        dc=9,
        backlight=None,  # 18 for back BG slot, 19 for front BG slot.
        spi_speed_hz=80 * 1000 * 1000,
        offset_left=0 if display_type == "square" else 40,
        offset_top=53 if display_type == "rect" else 0,
    )

def update_message (message):
    size_x, size_y = draw.textsize(message, font)

    text_x = disp.width
    text_y = (disp.height - size_y) // 2

    t_start = time.time()

    return t_start, size_x, text_x, text_y


def update_display(message, t_start, size_x, text_x, text_y):
    x = (time.time() - t_start) * 100
    x %= size_x + disp.width
    draw.rectangle((0, 0, disp.width, disp.height), (0, 0, 0))
    draw.text((int(text_x - x), text_y), message, font=font, fill=(255, 255, 255))
    disp.display(img)
    

# Initialize display.
disp.begin()

WIDTH = disp.width
HEIGHT = disp.height

img = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)