#!/usr/bin/env python3
"""Render the 26 November 2026 world-news summary card to entry.png."""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024
PAGE_BG = (248, 249, 250)
NAVY = (15, 42, 68)
GOLD = (255, 196, 0)
PANEL_BG = (255, 255, 255)
PANEL_EDGE = (208, 214, 220)
INK = (28, 32, 38)
BODY_INK = (62, 68, 76)
FOOT_INK = (105, 111, 118)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD_PATH = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
PLAIN_PATH = os.path.join(FONT_DIR, "DejaVuSans.ttf")

HEADER_H = 148
GOLD_STRIP = 8
MARGIN = 36
GAP = 20
GRID_TOP = 184
GRID_BOTTOM = 944
FOOTER_Y = 972

STORIES = [
    {
        "tag": "01 \u2022 GULF \u2014 KUWAIT",
        "title": "Iran drone strike kills two Italians in Kuwait",
        "body": (
            "Two Rheinmetall Italia technicians died at an air-defence site "
            "hit by Iranian drones. Tehran denied any role."
        ),
        "accent": (176, 58, 58),
    },
    {
        "tag": "02 \u2022 MIDDLE EAST \u2014 GAZA",
        "title": "Israeli strikes kill nine in Gaza",
        "body": (
            "A strike on a Deir al-Balah apartment killed Hamas-appointed "
            "deputy education minister Khaled Abu Nada and his wife."
        ),
        "accent": (11, 94, 158),
    },
    {
        "tag": "03 \u2022 UKRAINE",
        "title": "Russia hits Kyiv with ballistic missiles",
        "body": (
            "Overnight missiles and 113 drones struck a shopping centre and "
            "two other buildings, wounding seven, Mayor Klitschko said."
        ),
        "accent": (146, 90, 12),
    },
    {
        "tag": "04 \u2022 EUROPE \u2014 ECB",
        "title": "Spain's De Cos picked to lead the ECB",
        "body": (
            "Eurozone leaders chose Pablo Hernandez de Cos to succeed "
            "Christine Lagarde as ECB president in February."
        ),
        "accent": (27, 120, 90),
    },
    {
        "tag": "05 \u2022 ASIA \u2014 NORTH KOREA",
        "title": "Kim pushes tactical nuclear expansion",
        "body": (
            "Touring nuclear facilities, Kim Jong Un called wider tactical "
            "nuclear deployment an urgent task, KCNA reported."
        ),
        "accent": (90, 40, 120),
    },
    {
        "tag": "06 \u2022 ASIA \u2014 THAILAND",
        "title": "Bangkok refinery blast injures nine",
        "body": (
            "An explosion and fire at Bangchak's refinery in the capital "
            "left nine hurt, three critically; nearby homes evacuated."
        ),
        "accent": (0, 110, 110),
    },
]


def load_fonts():
    return {
        "masthead": ImageFont.truetype(BOLD_PATH, 62),
        "subhead": ImageFont.truetype(BOLD_PATH, 21),
        "tag": ImageFont.truetype(BOLD_PATH, 16),
        "title": ImageFont.truetype(BOLD_PATH, 24),
        "body": ImageFont.truetype(PLAIN_PATH, 18),
        "footer": ImageFont.truetype(PLAIN_PATH, 16),
    }


def paint_header(draw, fonts):
    draw.rectangle([0, 0, CANVAS, HEADER_H], fill=NAVY)
    draw.rectangle([0, HEADER_H, CANVAS, HEADER_H + GOLD_STRIP], fill=GOLD)
    draw.text((MARGIN, 30), "WORLD NEWS", font=fonts["masthead"], fill=(255, 255, 255))
    draw.text(
        (MARGIN + 2, 108),
        "26 NOVEMBER 2026 \u2022 SIX STORIES FROM AROUND THE WORLD",
        font=fonts["subhead"],
        fill=GOLD,
    )


def paint_panel(draw, fonts, story, left, top, width, height):
    right, bottom = left + width, top + height
    draw.rectangle([left, top, right, bottom], fill=PANEL_BG, outline=PANEL_EDGE, width=2)
    draw.rectangle([left, top, right, top + 8], fill=story["accent"])

    x = left + 20
    y = top + 24
    draw.text((x, y), story["tag"], font=fonts["tag"], fill=story["accent"])
    y += 30
    for line in textwrap.wrap(story["title"], width=26):
        draw.text((x, y), line, font=fonts["title"], fill=INK)
        y += 30
    y += 6
    for line in textwrap.wrap(story["body"], width=42):
        draw.text((x, y), line, font=fonts["body"], fill=BODY_INK)
        y += 24


def build_card():
    img = Image.new("RGB", (CANVAS, CANVAS), PAGE_BG)
    draw = ImageDraw.Draw(img)
    fonts = load_fonts()

    paint_header(draw, fonts)

    col_w = (CANVAS - 2 * MARGIN - GAP) // 2
    row_h = (GRID_BOTTOM - GRID_TOP - 2 * GAP) // 3
    for idx, story in enumerate(STORIES):
        row, col = divmod(idx, 2)
        left = MARGIN + col * (col_w + GAP)
        top = GRID_TOP + row * (row_h + GAP)
        paint_panel(draw, fonts, story, left, top, col_w, row_h)

    draw.text(
        (MARGIN, FOOTER_Y),
        "Sources: Reuters, AP, AFP, CNN, WSJ \u2022 Events of 26 November 2026",
        font=fonts["footer"],
        fill=FOOT_INK,
    )
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, "entry.png")
    build_card().save(target, format="PNG")
    print(f"saved {target} ({os.path.getsize(target)} bytes)")


if __name__ == "__main__":
    main()
