#!/usr/bin/env python3
"""Build the gta6-meme-x-01 meme image.

Composites the AI-generated Vice City artwork (assets/meme-bg.png, original
art made for this entry: a cute ghost waiting with suitcases and a calendar)
with classic meme bands:

  * a top band carrying the setup line,
  * the artwork in the middle (with a neon "make.fun" sign painted onto the
    blank billboard in the scene),
  * a bottom band carrying the punchline on the left and the make.fun
    branding (ghost mark + wordmark + tagline) on the right, big enough to
    stay recognisable when the post picture is shrunk to 480x480.

Output: assets/gta6-meme.png at 1600x1220.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BG_PATH = os.path.join(HERE, "assets", "meme-bg.png")
OUT_PATH = os.path.join(HERE, "assets", "gta6-meme.png")

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

W = 1600
TOP_H = 150
BOT_H = 175
ART_H = 900  # 1600x900 = the 16:9 artwork, unscaled in aspect
H = TOP_H + ART_H + BOT_H

NAVY = (10, 10, 26)
WHITE = (255, 255, 255)
PINK = (255, 62, 165)
CYAN = (38, 230, 218)
DIM = (178, 182, 205)


def font(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def draw_centered(draw, cx, y, text, fnt, fill, stroke=0, stroke_fill=(0, 0, 0)):
    box = draw.textbbox((0, 0), text, font=fnt, stroke_width=stroke)
    tw = box[2] - box[0]
    draw.text((cx - tw / 2 - box[0], y), text, font=fnt, fill=fill,
              stroke_width=stroke, stroke_fill=stroke_fill)
    return tw


def ghost_glyph(size):
    """A simple white ghost with two black oval eyes, on transparency."""
    s = size
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    body = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    # dome + straight sides down to 78% height
    bd.ellipse([s * 0.08, s * 0.02, s * 0.92, s * 0.86], fill=(255, 255, 255, 255))
    bd.rectangle([s * 0.08, s * 0.40, s * 0.92, s * 0.80], fill=(255, 255, 255, 255))
    # wavy hem: cut three scallops out of the bottom edge
    for i, cx in enumerate((0.22, 0.50, 0.78)):
        bd.ellipse([s * (cx - 0.13), s * 0.68, s * (cx + 0.13), s * 0.94],
                   fill=(0, 0, 0, 0))
    img.alpha_composite(body)
    d = ImageDraw.Draw(img)
    for cx in (0.36, 0.64):
        d.ellipse([s * (cx - 0.075), s * 0.34, s * (cx + 0.075), s * 0.56],
                  fill=(12, 12, 24, 255))
    return img


def neon_sign(base, text="make.fun"):
    """Paint a glowing make.fun sign onto the blank billboard, top-left."""
    W0, H0 = base.size
    # billboard interior in the 2048x1152 artwork, measured from the render
    x0, y0, x1, y1 = int(W0 * 0.048), int(H0 * 0.115), int(W0 * 0.150), int(H0 * 0.265)
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    fnt = font(int((y1 - y0) * 0.29))
    # soft glow pass, then the bright core
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    box = gd.textbbox((0, 0), text, font=fnt)
    tw, th = box[2] - box[0], box[3] - box[1]
    gd.text((cx - tw / 2 - box[0], cy - th / 2 - box[1]), text, font=fnt,
            fill=(255, 62, 165, 255))
    glow = glow.filter(ImageFilter.GaussianBlur(10))
    base.alpha_composite(glow)
    d = ImageDraw.Draw(base)
    d.text((cx - tw / 2 - box[0], cy - th / 2 - box[1]), text, font=fnt,
           fill=(255, 235, 248, 255))
    return base


def main():
    art = Image.open(BG_PATH).convert("RGBA")
    art = art.resize((W, ART_H), Image.LANCZOS)
    art = neon_sign(art)

    canvas = Image.new("RGBA", (W, H), NAVY + (255,))
    canvas.alpha_composite(art, (0, TOP_H))
    d = ImageDraw.Draw(canvas)

    # ---- top band: the setup
    draw_centered(d, W // 2, 34, "WAITED 13 YEARS FOR GTA VI", font(74), WHITE)

    # ---- bottom band: punchline (left) + make.fun branding (right)
    by = TOP_H + ART_H
    d.line([(0, by), (W, by)], fill=PINK + (255,), width=5)
    draw_centered(d, 430, by + 28, "IT'S FINALLY HERE.", font(56), WHITE)
    draw_centered(d, 430, by + 98, "TOOK THE WHOLE WEEK OFF.", font(44), CYAN)

    gx = 990
    ghost = ghost_glyph(120)
    canvas.alpha_composite(ghost, (gx, by + 28))
    d = ImageDraw.Draw(canvas)
    d.text((gx + 140, by + 34), "make.fun", font=font(66), fill=WHITE)
    tagline = "my AI agent earns money while I play"
    size = 32
    while size > 18:
        f = font(size, bold=False)
        if d.textbbox((0, 0), tagline, font=f)[2] <= W - (gx + 142) - 14:
            break
        size -= 1
    d.text((gx + 142, by + 114), tagline, font=f, fill=DIM)

    canvas.convert("RGB").save(OUT_PATH, "PNG")
    print(f"wrote {OUT_PATH} ({W}x{H})")


if __name__ == "__main__":
    main()
