#!/usr/bin/env python3
"""Create optimised WebP assets from the user-supplied source photographs."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source" / "photos"
OUTPUT = ROOT / "public" / "images"
REVIEW = ROOT / ".work" / "optimised-contact-sheet.jpg"

PROJECT_SIZE = (1200, 750)
GALLERY_SIZE = (1200, 900)

ASSETS = [
    ("mineral-specimens.jpeg", "project-critical-elements.webp", PROJECT_SIZE),
    ("plasma-experiment.jpeg", "project-co2-plasmas.webp", PROJECT_SIZE),
    ("fuel-cell-electrolyser-stack.jpeg", "project-fuel-cell-hydrogen.webp", PROJECT_SIZE),
    ("haadf-microscopy.png", "project-diamond-microscopy.webp", PROJECT_SIZE),
    ("mote-2d-semiconductor.png", "project-2d-semiconductors.webp", PROJECT_SIZE),
    ("functional-materials-synthesis.png", "project-functional-materials-synthesis.webp", PROJECT_SIZE),
    ("sodium-battery-scale-up.jpg", "project-sodium-battery.webp", PROJECT_SIZE),
    ("laboratory-automation.jpeg", "project-lab-automation.webp", PROJECT_SIZE),
    ("azurite-malachite.jpeg", "project-public-engagement.webp", PROJECT_SIZE),
    ("professional-gathering.jpeg", "gallery-professional-gathering.webp", GALLERY_SIZE),
    ("mote-2d-semiconductor.png", "gallery-2d-semiconductors.webp", GALLERY_SIZE),
    ("functional-materials-synthesis.png", "gallery-functional-materials-synthesis.webp", GALLERY_SIZE),
    ("plasma-experiment.jpeg", "gallery-plasma-electrochemistry.webp", GALLERY_SIZE),
    ("electrochemical-cell.jpeg", "gallery-electrochemical-cell.webp", GALLERY_SIZE),
    ("haadf-microscopy.png", "gallery-haadf-microscopy.webp", GALLERY_SIZE),
    ("research-facility.jpeg", "gallery-research-facility.webp", GALLERY_SIZE),
    ("mineral-specimens.jpeg", "gallery-mineral-education.webp", GALLERY_SIZE),
]


def open_oriented(filename: str) -> Image.Image:
    with Image.open(SOURCE / filename) as source:
        return ImageOps.exif_transpose(source).convert("RGB")


def save_webp(image: Image.Image, filename: str) -> None:
    destination = OUTPUT / filename
    image.save(destination, "WEBP", quality=82, method=6)
    print(f"{filename}: {image.width} × {image.height}, {destination.stat().st_size // 1024} KiB")


def make_review_sheet(filenames: list[str]) -> None:
    """Create a temporary contact sheet for visual crop verification."""
    columns = 3
    tile_width, image_height, label_height = 360, 240, 34
    rows = (len(filenames) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * tile_width, rows * (image_height + label_height)), "#edf1f2")
    draw = ImageDraw.Draw(sheet)
    for index, filename in enumerate(filenames):
        with Image.open(OUTPUT / filename) as image:
            preview = ImageOps.fit(image.convert("RGB"), (tile_width, image_height), Image.Resampling.LANCZOS)
        x = (index % columns) * tile_width
        y = (index // columns) * (image_height + label_height)
        sheet.paste(preview, (x, y))
        draw.text((x + 8, y + image_height + 9), filename, fill="#172b33")
    REVIEW.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(REVIEW, "JPEG", quality=88)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    portrait = open_oriented("haytham-hussein-portrait.jpeg")
    portrait = portrait.crop((120, 350, 1320, 1850)).resize((800, 1000), Image.Resampling.LANCZOS)
    save_webp(portrait, "haytham-hussein-portrait.webp")

    generated = []
    for source, destination, size in ASSETS:
        centering = (0.5, 0.55) if destination == "project-fuel-cell-hydrogen.webp" else (0.5, 0.5)
        image = ImageOps.fit(open_oriented(source), size, Image.Resampling.LANCZOS, centering=centering)
        save_webp(image, destination)
        generated.append(destination)
    make_review_sheet(generated)


if __name__ == "__main__":
    main()
