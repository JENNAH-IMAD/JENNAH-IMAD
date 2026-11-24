#!/usr/bin/env python3
"""Render the ImFix profile banner as a subtle animated GIF for GitHub."""
from __future__ import annotations

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "cards" / "portfolio-theme.gif"
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
FONT_REG = ImageFont.truetype(str(FONT_DIR / "DejaVuSansMono.ttf"), 13)
FONT_SMALL = ImageFont.truetype(str(FONT_DIR / "DejaVuSansMono.ttf"), 9)
FONT_FOOT = ImageFont.truetype(str(FONT_DIR / "DejaVuSansMono.ttf"), 11)
FONT_ROLE = ImageFont.truetype(str(FONT_DIR / "DejaVuSansMono.ttf"), 15)
FONT_BOLD = ImageFont.truetype(str(FONT_DIR / "DejaVuSansMono-Bold.ttf"), 57)
FONT_LOGO = ImageFont.truetype(str(FONT_DIR / "DejaVuSansMono-Bold.ttf"), 22)
BG, SURFACE = (23, 26, 27), (28, 32, 33)
RULE, RULE_SOFT = (55, 60, 62), (48, 54, 56)
TEXT, MUTED, SUBTLE, ACCENT = (230, 232, 231), (185, 192, 191), (154, 162, 161), (198, 206, 205)


def faded(color: tuple[int, int, int], opacity: float) -> tuple[int, int, int]:
    return tuple(round(c * max(0.0, min(1.0, opacity))) for c in color)


def render(intro: int, pulse: int) -> Image.Image:
    image = Image.new("RGB", (1000, 320), BG)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((1, 1, 998, 318), radius=4, outline=RULE)
    draw.line((32, 75, 968, 75), fill=RULE_SOFT)
    draw.line((32, 274, 968, 274), fill=RULE_SOFT)
    draw.rounded_rectangle((40, 34, 48, 42), radius=1, fill=ACCENT)
    draw.text((62, 32), "IMAD JENNAH / PORTFOLIO V2", font=FONT_FOOT, fill=MUTED)
    draw.text((960, 32), "CASABLANCA, MOROCCO", font=FONT_FOOT, fill=MUTED, anchor="ra")

    title_opacity = min(1, max(0, (intro - 1) / 8))
    role_opacity = min(1, max(0, (intro - 4) / 7))
    note_opacity = min(1, max(0, (intro - 7) / 7))
    footer_opacity = min(1, max(0, (intro - 9) / 5))
    draw.text((40, 94 + round(11 * (1 - title_opacity))), "IMAD JENNAH", font=FONT_BOLD, fill=faded(TEXT, title_opacity))
    draw.text((43, 183 + round(7 * (1 - role_opacity))), "FULL-STACK SOFTWARE ENGINEER  ·  AI ENTHUSIAST", font=FONT_ROLE, fill=faded(TEXT, role_opacity))
    draw.text((43, 222 + round(5 * (1 - note_opacity))), "CONCEVOIR. DÉVELOPPER. AMÉLIORER.", font=FONT_REG, fill=faded(SUBTLE, note_opacity))

    phase = pulse * 2 * math.pi / 14
    x, y = 820, 105 + round(math.sin(phase) * 2)
    draw.rectangle((x, y, x + 140, y + 94), fill=SURFACE, outline=RULE)
    dot_opacity = .48 + .52 * (.5 + .5 * math.sin(phase))
    draw.ellipse((x + 121, y + 12, x + 127, y + 18), fill=faded(ACCENT, dot_opacity))
    draw.line(((x + 27, y + 27), (x + 17, y + 38), (x + 27, y + 49)), fill=TEXT, width=3, joint="curve")
    draw.line(((x + 55, y + 27), (x + 65, y + 38), (x + 55, y + 49)), fill=TEXT, width=3, joint="curve")
    draw.line((x + 49, y + 18, x + 35, y + 58), fill=TEXT, width=3)
    draw.text((x + 62, y + 27), "ImFix", font=FONT_LOGO, fill=TEXT)
    draw.text((x + 14, y + 68), "AVAILABLE FOR OPPORTUNITIES", font=FONT_SMALL, fill=SUBTLE)

    draw.text((40, 290), "JAVA  /  .NET  /  REACT  /  SPRING BOOT  /  ANGULAR", font=FONT_FOOT, fill=faded(SUBTLE, footer_opacity))
    draw.text((960, 290), "im-fix.vercel.app  ↗", font=FONT_FOOT, fill=faded(ACCENT, footer_opacity), anchor="ra")
    return image


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frames = [render(i, 0) for i in range(14)]
    frames.extend(render(14, i) for i in range(14))
    frames.append(render(14, 0))
    palette = frames[0].quantize(colors=128)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    indexed[0].save(OUTPUT, save_all=True, append_images=indexed[1:],
                    duration=[105] * (len(indexed) - 1) + [5000], loop=0,
                    optimize=True, disposal=1)
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
