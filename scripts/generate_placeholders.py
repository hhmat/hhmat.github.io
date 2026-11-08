"""Generate original, lightweight editorial placeholders and social artwork."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "public" / "images"
ICONS = ROOT / "public" / "icons"
IMAGES.mkdir(parents=True, exist_ok=True)
ICONS.mkdir(parents=True, exist_ok=True)

NAVY = "#172a43"
NAVY_LIGHT = "#274665"
ORANGE = "#e76832"
PAPER = "#f6f8fa"
MIST = "#dce5eb"
SLATE = "#607387"


def svg_document(body: str, width: int = 800, height: int = 600, label: str = "Abstract editorial placeholder") -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{label}</title><desc id="desc">Original geometric artwork used as a replaceable website placeholder.</desc>
<defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{MIST}" stroke-opacity=".22" stroke-width="1"/></pattern></defs>
{body}</svg>'''


def save(name: str, body: str, width: int = 800, height: int = 600, label: str = "Abstract editorial placeholder") -> None:
    (IMAGES / name).write_text(svg_document(body, width, height, label), encoding="utf-8")


save("haytham-profile-placeholder.svg", f'''
<rect width="800" height="1000" fill="{NAVY}"/><rect width="800" height="1000" fill="url(#grid)"/>
<circle cx="610" cy="205" r="230" fill="none" stroke="{ORANGE}" stroke-width="2"/><circle cx="610" cy="205" r="176" fill="{NAVY_LIGHT}"/>
<path d="M0 750L800 460V1000H0Z" fill="{PAPER}"/><path d="M0 750L800 460" stroke="{ORANGE}" stroke-width="3"/>
<text x="72" y="160" fill="{PAPER}" font-family="Arial,sans-serif" font-size="22" letter-spacing="5">HAYTHAM HUSSEIN</text>
<text x="58" y="635" fill="{PAPER}" font-family="Georgia,serif" font-size="280" letter-spacing="-24">HH</text>
<text x="72" y="846" fill="{NAVY}" font-family="Georgia,serif" font-size="52">Research · Data · Impact</text>
<text x="72" y="908" fill="{SLATE}" font-family="Arial,sans-serif" font-size="20" letter-spacing="3">PROFESSIONAL PORTRAIT PLACEHOLDER</text>
''', 800, 1000, "Haytham Hussein editorial portrait placeholder")

motifs = {
    "project-evidence.svg": f'<rect width="800" height="500" fill="{PAPER}"/><rect width="800" height="500" fill="url(#grid)"/><path d="M90 360C190 90 355 420 700 110" fill="none" stroke="{NAVY}" stroke-width="8"/><path d="M90 400C245 185 420 460 700 235" fill="none" stroke="{ORANGE}" stroke-width="3"/><circle cx="355" cy="274" r="18" fill="{NAVY}"/><text x="70" y="82" font-family="Georgia,serif" font-size="40" fill="{NAVY}">Evidence / interpretation</text>',
    "project-data.svg": f'<rect width="800" height="500" fill="{NAVY}"/><rect width="800" height="500" fill="url(#grid)"/><g fill="{PAPER}"><rect x="95" y="260" width="62" height="150"/><rect x="195" y="170" width="62" height="240"/><rect x="295" y="215" width="62" height="195"/><rect x="395" y="105" width="62" height="305"/></g><path d="M90 325L225 215 325 265 425 140 690 245" fill="none" stroke="{ORANGE}" stroke-width="5"/><text x="70" y="82" font-family="Georgia,serif" font-size="40" fill="{PAPER}">Data / responsibility</text>',
    "project-digital.svg": f'<rect width="800" height="500" fill="{MIST}"/><rect x="75" y="95" width="650" height="330" fill="{PAPER}" stroke="{NAVY}" stroke-width="2"/><rect x="105" y="130" width="190" height="260" fill="{NAVY}"/><rect x="335" y="130" width="350" height="30" fill="{MIST}"/><rect x="335" y="195" width="270" height="14" fill="{SLATE}"/><rect x="335" y="230" width="310" height="14" fill="{SLATE}"/><rect x="335" y="300" width="135" height="50" fill="{ORANGE}"/><text x="75" y="70" font-family="Georgia,serif" font-size="40" fill="{NAVY}">People / digital services</text>',
    "project-community.svg": f'<rect width="800" height="500" fill="{PAPER}"/><rect width="800" height="500" fill="url(#grid)"/><g fill="none" stroke="{NAVY}" stroke-width="4"><circle cx="300" cy="250" r="130"/><circle cx="500" cy="250" r="130"/></g><path d="M400 132A130 130 0 0 0 400 368A130 130 0 0 0 400 132" fill="{ORANGE}" fill-opacity=".82"/><text x="70" y="82" font-family="Georgia,serif" font-size="40" fill="{NAVY}">Community / exchange</text>',
    "project-software.svg": f'<rect width="800" height="500" fill="{NAVY}"/><rect width="800" height="500" fill="url(#grid)"/><g font-family="monospace" font-size="28" fill="{PAPER}"><text x="100" y="150">01  define the question</text><text x="100" y="210">02  test the workflow</text><text x="100" y="270">03  document decisions</text><text x="100" y="330">04  share the output</text></g><path d="M570 115l95 85-95 85" fill="none" stroke="{ORANGE}" stroke-width="7"/><text x="70" y="82" font-family="Georgia,serif" font-size="40" fill="{PAPER}">Software / reproducibility</text>',
    "project-map.svg": f'<rect width="800" height="500" fill="{MIST}"/><path d="M90 80L280 45 460 100 700 55V420L480 455 285 405 90 445Z" fill="{PAPER}" stroke="{NAVY}" stroke-width="2"/><path d="M280 45L285 405M460 100L480 455M90 245L710 230" stroke="{NAVY}" stroke-opacity=".35" stroke-width="3"/><path d="M140 350C240 200 335 355 430 210S600 150 650 110" fill="none" stroke="{ORANGE}" stroke-width="6"/><circle cx="430" cy="210" r="14" fill="{NAVY}"/><text x="70" y="82" font-family="Georgia,serif" font-size="40" fill="{NAVY}">Place / evidence</text>',
}
for filename, body in motifs.items():
    save(filename, body, 800, 500, filename.replace("project-", "").replace(".svg", "").replace("-", " "))

save("news-feature.svg", f'''<rect width="800" height="600" fill="{NAVY}"/><rect width="800" height="600" fill="url(#grid)"/><circle cx="590" cy="260" r="190" fill="none" stroke="{ORANGE}" stroke-width="2"/><circle cx="590" cy="260" r="120" fill="{NAVY_LIGHT}"/><path d="M70 420H700" stroke="{PAPER}" stroke-width="1"/><text x="65" y="140" fill="{PAPER}" font-family="Georgia,serif" font-size="64">Notes on</text><text x="65" y="215" fill="{PAPER}" font-family="Georgia,serif" font-size="64">research &amp; practice</text><text x="70" y="475" fill="{PAPER}" font-family="Arial,sans-serif" font-size="20" letter-spacing="4">READ · QUESTION · CONNECT</text>''', 800, 600, "Research and practice editorial artwork")

gallery_bodies = [
    ("gallery-conference.svg", f'<rect width="800" height="600" fill="{NAVY}"/><path d="M100 450L300 130 480 450M280 450L500 130 700 450" fill="none" stroke="{PAPER}" stroke-width="3"/><circle cx="400" cy="290" r="70" fill="{ORANGE}"/>'),
    ("gallery-event.svg", f'<rect width="800" height="600" fill="{MIST}"/><g fill="none" stroke="{NAVY}" stroke-width="3"><circle cx="400" cy="300" r="210"/><circle cx="400" cy="300" r="145"/><circle cx="400" cy="300" r="80"/></g><circle cx="400" cy="300" r="25" fill="{ORANGE}"/>'),
    ("gallery-research.svg", f'<rect width="800" height="600" fill="{PAPER}"/><rect width="800" height="600" fill="url(#grid)"/><path d="M110 470L250 300 365 390 550 160 690 250" fill="none" stroke="{NAVY}" stroke-width="5"/><g fill="{ORANGE}"><circle cx="250" cy="300" r="16"/><circle cx="365" cy="390" r="16"/><circle cx="550" cy="160" r="16"/></g>'),
    ("gallery-community.svg", f'<rect width="800" height="600" fill="{NAVY}"/><g fill="{NAVY_LIGHT}" stroke="{PAPER}" stroke-width="2"><circle cx="280" cy="230" r="130"/><circle cx="520" cy="230" r="130"/><circle cx="400" cy="410" r="130"/></g><circle cx="400" cy="300" r="50" fill="{ORANGE}"/>'),
    ("gallery-exchange.svg", f'<rect width="800" height="600" fill="{PAPER}"/><path d="M60 140C260 140 240 460 400 300S540 140 740 140M60 460C260 460 240 140 400 300S540 460 740 460" fill="none" stroke="{NAVY}" stroke-width="5"/><circle cx="400" cy="300" r="30" fill="{ORANGE}"/>'),
    ("gallery-showcase.svg", f'<rect width="800" height="600" fill="{MIST}"/><rect x="90" y="100" width="280" height="400" fill="{NAVY}"/><rect x="410" y="100" width="300" height="180" fill="{PAPER}"/><rect x="410" y="320" width="300" height="180" fill="{ORANGE}"/><path d="M130 160H330M130 205H330M130 250H270" stroke="{PAPER}" stroke-width="5"/>'),
]
for filename, body in gallery_bodies:
    save(filename, body, 800, 600, filename.replace("gallery-", "").replace(".svg", "").replace("-", " "))

(ICONS / "favicon.svg").write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="4" fill="{NAVY}"/><path d="M14 14v36M50 14v36M14 32h36" stroke="{PAPER}" stroke-width="6"/><circle cx="50" cy="14" r="5" fill="{ORANGE}"/></svg>''', encoding="utf-8")

image = Image.new("RGB", (1200, 630), NAVY)
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, 1200, 630), outline=NAVY_LIGHT, width=24)
draw.line((72, 82, 160, 82), fill=ORANGE, width=5)
large = ImageFont.load_default(size=76)
medium = ImageFont.load_default(size=34)
small = ImageFont.load_default(size=23)
draw.text((72, 125), "Haytham Hussein", font=large, fill=PAPER)
draw.text((76, 250), "Electrochemistry, materials &", font=medium, fill=PAPER)
draw.text((76, 300), "sustainable technologies.", font=medium, fill=PAPER)
draw.text((76, 475), "AXA RESEARCH FELLOW  ·  UNIVERSITY OF NOTTINGHAM", font=small, fill=MIST)
draw.ellipse((920, 110, 1110, 300), outline=ORANGE, width=4)
draw.text((954, 166), "HH", font=large, fill=PAPER)
image.save(IMAGES / "og-image.png", optimize=True)
print(f"Generated {len(list(IMAGES.glob('*')))} image assets and favicon in {IMAGES.parent}")
