"""Generate original scientific-figure examples for the project gallery."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).parent
GALLERY = ROOT / "gallery"
CANVAS = "#FAFAF8"
INK = "#2E3640"
MUTED = "#AEB7BE"
BLUE = "#4D779B"
CORAL = "#C45C69"
AMBER = "#E6A72F"
PALE_BLUE = "#DDE8F0"
PALE_CORAL = "#F3D9DC"


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default()


def canvas(width: int = 960, height: int = 600) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (width, height), CANVAS)
    return image, ImageDraw.Draw(image)


def axes(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    left, top, right, bottom = box
    for i in range(1, 5):
        y = top + (bottom - top) * i // 5
        draw.line((left, y, right, y), fill="#E3E6E7", width=1)
    draw.line((left, top, left, bottom), fill=INK, width=3)
    draw.line((left, bottom, right, bottom), fill=INK, width=3)
    for i in range(5):
        x = left + (right - left) * i // 4
        draw.line((x, bottom, x, bottom + 8), fill=INK, width=2)


def trajectory() -> Image.Image:
    image, draw = canvas()
    draw.text((56, 40), "Treatment response over time", fill=INK, font=font(27, True))
    draw.text((56, 78), "Original synthetic example · paired categories with uncertainty", fill="#65717A", font=font(16))
    box = (105, 140, 890, 505)
    axes(draw, box)
    left, top, right, bottom = box
    x_values = np.linspace(left + 24, right - 24, 9).astype(int)
    blue_y = np.array([426, 397, 367, 337, 350, 302, 277, 240, 203])
    coral_y = np.array([456, 444, 425, 440, 402, 417, 388, 365, 316])
    for ys, colour, marker in ((blue_y, BLUE, "circle"), (coral_y, CORAL, "square")):
        upper = ys - 28
        lower = ys + 28
        draw.line(list(zip(x_values, upper)), fill=colour, width=2, joint="curve")
        draw.line(list(zip(x_values, lower)), fill=colour, width=2, joint="curve")
        draw.line(list(zip(x_values, ys)), fill=colour, width=5, joint="curve")
        for x, y in zip(x_values, ys):
            if marker == "circle":
                draw.ellipse((x - 8, y - 8, x + 8, y + 8), fill=colour, outline=CANVAS, width=2)
            else:
                draw.rounded_rectangle((x - 8, y - 8, x + 8, y + 8), radius=2, fill=colour, outline=CANVAS, width=2)
    draw.text((126, 518), "0", fill="#65717A", font=font(14))
    draw.text((500, 518), "Study week", fill="#65717A", font=font(14))
    draw.text((835, 518), "8", fill="#65717A", font=font(14))
    draw.rounded_rectangle((625, 153, 867, 224), radius=10, fill="#FFFFFF", outline="#D8DDDF")
    draw.ellipse((647, 174, 661, 188), fill=BLUE)
    draw.text((674, 169), "Condition A", fill=INK, font=font(15))
    draw.rounded_rectangle((647, 198, 661, 212), radius=2, fill=CORAL)
    draw.text((674, 193), "Condition B", fill=INK, font=font(15))
    return image


def response_surface() -> Image.Image:
    image, draw = canvas()
    draw.text((56, 40), "Response landscape", fill=INK, font=font(27, True))
    draw.text((56, 78), "Original synthetic example · ordered field with a neutral midpoint", fill="#65717A", font=font(16))
    left, top, right, bottom = 105, 140, 790, 510
    width, height = right - left, bottom - top
    y, x = np.mgrid[-1.0:1.0:complex(height), -1.4:1.4:complex(width)]
    z = np.sin(2.3 * x) * np.cos(2.1 * y) + 0.35 * x - 0.18 * y
    z = (z - z.min()) / (z.max() - z.min())
    stops = np.array([[42, 70, 96], [100, 140, 175], [230, 234, 231], [246, 205, 128], [197, 84, 91]])
    positions = np.linspace(0, 1, len(stops))
    colour = np.empty((height, width, 3), dtype=np.uint8)
    for channel in range(3):
        colour[:, :, channel] = np.interp(z, positions, stops[:, channel]).astype(np.uint8)
    heatmap = Image.fromarray(colour, "RGB")
    image.paste(heatmap, (left, top))
    contour = ImageDraw.Draw(image)
    for level in np.linspace(0.12, 0.88, 8):
        points = []
        for x_pos in range(left, right, 8):
            normalized = (x_pos - left) / width
            y_pos = top + int(height * (0.52 + 0.22 * np.sin(5.4 * normalized + level * 5) - 0.30 * (level - 0.5)))
            points.append((x_pos, y_pos))
        contour.line(points, fill="#FFFFFF", width=1)
    draw.rectangle((left, top, right, bottom), outline=INK, width=2)
    draw.text((104, 522), "Parameter 1", fill="#65717A", font=font(14))
    draw.text((708, 522), "Parameter 2", fill="#65717A", font=font(14))
    draw.text((823, 161), "Low", fill=INK, font=font(15, True))
    swatches = ["#2A4660", "#648CAF", "#E6EAE7", "#F6CD80", "#C5545B"]
    for index, colour_hex in enumerate(swatches):
        y_pos = 197 + index * 53
        draw.rounded_rectangle((824, y_pos, 868, y_pos + 34), radius=6, fill=colour_hex)
    draw.text((823, 470), "High", fill=INK, font=font(15, True))
    return image


def group_separation() -> Image.Image:
    image, draw = canvas()
    draw.text((56, 40), "Group separation", fill=INK, font=font(27, True))
    draw.text((56, 78), "Original synthetic example · contextual points plus a rare highlight", fill="#65717A", font=font(16))
    box = (105, 140, 890, 510)
    axes(draw, box)
    rng = np.random.default_rng(16)
    x1 = rng.normal(350, 88, 105)
    y1 = rng.normal(374, 58, 105) - 0.22 * (x1 - 350)
    x2 = rng.normal(645, 63, 48)
    y2 = rng.normal(255, 45, 48) - 0.18 * (x2 - 645)
    for x, y in zip(x1, y1):
        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=INK)
    for x, y in zip(x2, y2):
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=AMBER, outline=CANVAS, width=1)
    draw.ellipse((736, 184, 750, 198), fill=AMBER, outline=INK, width=2)
    draw.line((743, 200, 743, 452), fill=AMBER, width=3)
    draw.text((130, 522), "Latent dimension 1", fill="#65717A", font=font(14))
    draw.text((715, 522), "Latent dimension 2", fill="#65717A", font=font(14))
    draw.rounded_rectangle((585, 380, 855, 460), radius=10, fill="#FFFFFF", outline="#D8DDDF")
    draw.ellipse((606, 400, 619, 413), fill=INK)
    draw.text((633, 395), "Context observations", fill=INK, font=font(14))
    draw.ellipse((606, 430, 619, 443), fill=AMBER)
    draw.text((633, 425), "Exceptional cluster", fill=INK, font=font(14))
    return image


def overview(images: list[Image.Image]) -> Image.Image:
    sheet = Image.new("RGB", (1500, 585), CANVAS)
    for index, image in enumerate(images):
        thumb = image.resize((480, 300), Image.Resampling.LANCZOS)
        x = 15 + index * 495
        sheet.paste(thumb, (x, 22))
        labels = [("Paired categories", BLUE), ("Ordered response", CORAL), ("Rare emphasis", AMBER)]
        title, colour = labels[index]
        draw = ImageDraw.Draw(sheet)
        draw.rounded_rectangle((x + 20, 358, x + 58, 396), radius=8, fill=colour)
        draw.text((x + 72, 361), title, fill=INK, font=font(22, True))
        descriptions = [
            "Compare co-occurring series, uncertainty, and structural neutrals.",
            "Preserve ordered lightness and an interpretable midpoint.",
            "Keep context quiet so exceptions carry visual meaning.",
        ]
        draw.multiline_text((x + 20, 414), descriptions[index], fill="#65717A", font=font(16), spacing=5)
    draw = ImageDraw.Draw(sheet)
    draw.text((30, 522), "All figures are original synthetic examples generated locally for this repository.", fill="#65717A", font=font(15))
    return sheet


def main() -> None:
    GALLERY.mkdir(exist_ok=True)
    figures = [trajectory(), response_surface(), group_separation()]
    names = ["trajectory-study.png", "response-surface.png", "group-separation.png"]
    for image, name in zip(figures, names):
        image.save(GALLERY / name)
    overview(figures).save(ROOT / "gallery-overview.png")
    print("Wrote original gallery figures")


if __name__ == "__main__":
    main()
