from PIL import Image, ImageDraw, ImageFont
import textwrap, os

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

BG = (248, 249, 250)
NAVY = (15, 42, 68)
GOLD = (255, 196, 0)
WHITE = (255, 255, 255)
INK = (20, 30, 40)
MUTED = (90, 100, 110)
PANEL_BG = (255, 255, 255)
BORDER = (220, 225, 230)

def font(path, size):
    return ImageFont.truetype(path, size)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# Header
d.rectangle([0, 0, W, 148], fill=NAVY)
d.rectangle([0, 148, W, 154], fill=GOLD)
d.text((32, 22), "WORLD NEWS", font=font(FB, 62), fill=WHITE)
d.text((32, 92), "26 NOVEMBER 2026  •  SIX STORIES FROM AROUND THE WORLD", font=font(FB, 22), fill=GOLD)

stories = [
    ("01  •  GULF — KUWAIT", "Iran drone strike kills two Italians in Kuwait",
     "Two Rheinmetall Italia technicians died at an air-defence site hit by Iranian drones. Tehran denied any role.", (176, 58, 58)),
    ("02  •  MIDDLE EAST — GAZA", "Israeli strikes kill nine in Gaza",
     "A strike on a Deir al-Balah apartment killed Hamas-appointed deputy education minister Khaled Abu Nada and his wife.", (11, 94, 158)),
    ("03  •  UKRAINE", "Russia hits Kyiv with ballistic missiles",
     "Overnight missiles and 113 drones struck a shopping centre and two other buildings, wounding seven, Mayor Klitschko said.", (146, 90, 12)),
    ("04  •  EUROPE — ECB", "Spain's De Cos picked to lead the ECB",
     "Eurozone leaders chose Pablo Hernandez de Cos to succeed Christine Lagarde as ECB president in February.", (27, 120, 90)),
    ("05  •  ASIA — NORTH KOREA", "Kim pushes tactical nuclear expansion",
     "Touring nuclear facilities, Kim Jong Un called wider tactical nuclear deployment an urgent task, KCNA reported.", (90, 40, 120)),
    ("06  •  ASIA — THAILAND", "Bangkok refinery blast injures nine",
     "An explosion and fire at Bangchak's refinery in the capital left nine hurt, three critically; nearby homes evacuated.", (0, 110, 110)),
]

# Grid: 2 cols x 3 rows
margin = 24
gap = 16
col_w = (W - margin*2 - gap) // 2
row_h = 252
top0 = 168
for i, (tag, title, body, color) in enumerate(stories):
    col = i % 2
    row = i // 2
    x0 = margin + col * (col_w + gap)
    y0 = top0 + row * (row_h + gap)
    x1 = x0 + col_w
    y1 = y0 + row_h
    # panel
    d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=PANEL_BG, outline=BORDER, width=2)
    d.rounded_rectangle([x0, y0, x1, y0+8], radius=4, fill=color)
    # tag
    d.text((x0+18, y0+22), tag, font=font(FB, 17), fill=color)
    # title, wrap to ~26 chars
    title_lines = textwrap.wrap(title, width=26)
    ty = y0 + 52
    for line in title_lines[:2]:
        d.text((x0+18, ty), line, font=font(FB, 27), fill=INK)
        ty += 34
    # body, wrap
    body_lines = textwrap.wrap(body, width=42)
    by = ty + 10
    for line in body_lines[:4]:
        d.text((x0+18, by), line, font=font(FR, 20), fill=(45, 55, 65))
        by += 27

# Footer
fy = top0 + 3*row_h + 2*gap + 8
d.text((32, fy), "Sources: Reuters, AP, AFP, CNN, WSJ  •  Events of 26 November 2026", font=font(FR, 16), fill=MUTED)

img.save(OUT, "PNG", optimize=True)
print(f"saved {OUT} {os.path.getsize(OUT)} bytes {img.size}")
