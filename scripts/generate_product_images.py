from __future__ import annotations

import csv
import json
import math
import random
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PREVIEW_ASSETS = ROOT / "live-preview" / "assets"
MASTER_ASSETS = ROOT / "product_media_master"
ASSETS.mkdir(parents=True, exist_ok=True)
PREVIEW_ASSETS.mkdir(parents=True, exist_ok=True)
MASTER_ASSETS.mkdir(parents=True, exist_ok=True)

W = H = 1600
PAPER = "#F4EEDF"
CREAM = "#FFF9ED"
INK = "#16263B"
POPPY = "#D85143"
MUSTARD = "#E4AC42"
SAGE = "#55796D"
BLUE = "#5872A8"
THREAD = {
    "N": INK,
    "C": CREAM,
    "R": POPPY,
    "Y": MUSTARD,
    "G": SAGE,
    "B": BLUE,
}

FONT_HEAD = "C:/Windows/Fonts/georgiab.ttf"
FONT_BODY = "C:/Windows/Fonts/trebuc.ttf"
FONT_BODY_BOLD = "C:/Windows/Fonts/trebucbd.ttf"


def font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def paper_background(seed: int, tone=PAPER):
    random.seed(seed)
    base = Image.new("RGB", (W, H), tone)
    px = base.load()
    for y in range(H):
        for x in range(W):
            n = random.randint(-5, 5)
            r, g, b = px[x, y]
            px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)))
    return base.filter(ImageFilter.GaussianBlur(0.35))


def shadowed_paste(base, layer, xy, blur=26, alpha=95):
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    mask = layer.getchannel("A")
    sh = Image.new("RGBA", layer.size, (22, 38, 59, alpha))
    shadow.paste(sh, xy, mask)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(shadow)
    base.alpha_composite(layer, xy)


def flower_chart():
    grid = [["N" for _ in range(30)] for _ in range(30)]
    # stems and leaves
    for y in range(13, 28):
        for x in (14, 15):
            grid[y][x] = "G"
    for i in range(6):
        for dx in range(2):
            grid[18 + i][13 - i // 2 + dx] = "G"
            grid[20 + i][16 + i // 2 + dx] = "G"
    # three geometric flowers
    for cx, cy, c, r in [(15, 9, "R", 5), (9, 14, "Y", 3), (22, 14, "B", 4)]:
        for y in range(30):
            for x in range(30):
                if abs(x - cx) + abs(y - cy) <= r + 1 and (x - cx) ** 2 + (y - cy) ** 2 <= (r + .9) ** 2:
                    grid[y][x] = c
        grid[cy][cx] = "C"
    return grid


def sardine_chart():
    grid = [["C" for _ in range(30)] for _ in range(30)]
    for y in range(8, 23):
        for x in range(4, 24):
            if ((x - 14) / 10) ** 2 + ((y - 15) / 7) ** 2 <= 1:
                grid[y][x] = "B"
    for y in range(10, 21):
        width = max(0, 5 - abs(y - 15) // 2)
        for x in range(24, 24 + width):
            if x < 30:
                grid[y][x] = "Y"
    for y in range(10, 21):
        for x in range(6, 10):
            if ((x - 8) / 3) ** 2 + ((y - 15) / 5) ** 2 <= 1:
                grid[y][x] = "G"
    grid[13][7] = "C"
    grid[13][8] = "N"
    for x in (12, 16, 20):
        for y in range(10, 21):
            if grid[y][x] == "B":
                grid[y][x] = "C"
    return grid


def victory_chart():
    grid = [["C" for _ in range(30)] for _ in range(30)]
    for y in range(5, 18):
        left = 8 + max(0, (y - 8) // 4)
        right = 22 - max(0, (y - 8) // 4)
        for x in range(left, right):
            grid[y][x] = "Y"
    for y in range(6, 14):
        for x in range(3, 9):
            if ((x - 8) / 5) ** 2 + ((y - 9) / 5) ** 2 <= 1:
                grid[y][x] = "B"
        for x in range(21, 27):
            if ((x - 21) / 5) ** 2 + ((y - 9) / 5) ** 2 <= 1:
                grid[y][x] = "B"
    for y in range(17, 25):
        for x in range(14, 16):
            grid[y][x] = "G"
    for y in range(24, 27):
        for x in range(9, 21):
            grid[y][x] = "N"
    # star
    for x, y in [(15, 8), (13, 11), (17, 11), (12, 9), (18, 9), (15, 12)]:
        grid[y][x] = "R"
    return grid


def stitched_canvas(chart, size=650, border=44, unfinished=False):
    layer = Image.new("RGBA", (size + border * 2, size + border * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((6, 6, layer.width - 6, layer.height - 6), radius=10, fill="#FBF8F0", outline=INK, width=7)
    cell = size / 30
    ox = oy = border
    for y, row in enumerate(chart):
        for x, code in enumerate(row):
            x0 = ox + x * cell
            y0 = oy + y * cell
            x1 = ox + (x + 1) * cell
            y1 = oy + (y + 1) * cell
            if unfinished and x > 25 and y > 23:
                d.rectangle((x0, y0, x1, y1), fill="#EEE5D4")
                d.line((x0, y0, x1, y0), fill="#B6A88E", width=1)
                d.line((x0, y0, x0, y1), fill="#B6A88E", width=1)
            else:
                c = THREAD[code]
                d.rectangle((x0, y0, x1, y1), fill=c)
                # raised diagonal stitch + highlight for tactile look
                d.line((x0 + 2, y1 - 2, x1 - 2, y0 + 2), fill="#0E1726", width=max(2, int(cell * .18)))
                d.line((x0 + 3, y1 - 4, x1 - 3, y0 + 1), fill=c, width=max(2, int(cell * .13)))
    return layer


def thread_card(color, label, size=(150, 235)):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((10, 10, size[0]-10, size[1]-10), radius=14, fill="#F8F0DF", outline=INK, width=4)
    for i in range(18):
        y = 38 + i * 7
        d.line((22, y, size[0]-22, y + random.randint(-2, 2)), fill=color, width=7)
    d.rectangle((30, 86, size[0]-30, 150), fill=CREAM, outline=INK, width=2)
    d.text((size[0]/2, 100), label, anchor="ma", fill=INK, font=font(FONT_BODY_BOLD, 18))
    return layer


def packaging(name, subtitle="FIRST STITCH MINI", size=(700, 920)):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((10, 10, size[0]-10, size[1]-10), radius=18, fill="#D9C69E", outline=INK, width=7)
    d.rectangle((52, 58, size[0]-52, size[1]-58), fill=CREAM, outline=INK, width=4)
    d.text((82, 95), "FIRST THREAD", fill=INK, font=font(FONT_BODY_BOLD, 32))
    d.text((82, 134), "STUDIO", fill=POPPY, font=font(FONT_BODY_BOLD, 20))
    y = 320
    for line in name.upper().split(" "):
        d.text((82, y), line, fill=INK, font=font(FONT_HEAD, 68))
        y += 78
    d.text((82, size[1]-180), subtitle, fill=INK, font=font(FONT_BODY_BOLD, 21))
    d.text((82, size[1]-135), "ORIGINAL DESIGN · ADULT BEGINNER", fill=INK, font=font(FONT_BODY, 17))
    return layer


def instruction_card(size=(420, 540)):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((5, 5, size[0]-5, size[1]-5), radius=12, fill=CREAM, outline=INK, width=5)
    d.text((34, 38), "YOUR FIRST", fill=INK, font=font(FONT_BODY_BOLD, 25))
    d.text((34, 75), "FIVE STITCHES", fill=INK, font=font(FONT_HEAD, 43))
    labels = ["1  THREAD", "2  ANCHOR", "3  STITCH", "4  TURN", "5  RECOVER"]
    for i, label in enumerate(labels):
        y = 170 + i * 58
        d.ellipse((34, y, 62, y+28), fill=[POPPY, MUSTARD, SAGE, BLUE, INK][i])
        d.text((78, y-1), label, fill=INK, font=font(FONT_BODY_BOLD, 18))
        d.line((78, y+30, size[0]-38, y+30), fill="#CFC3AC", width=2)
    return layer


def make_kit_photo(filename, name, chart, seed, accent, unfinished=False):
    base = paper_background(seed).convert("RGBA")
    d = ImageDraw.Draw(base)
    d.rectangle((0, 0, W, 105), fill=accent)
    d.text((70, 52), "DIGITAL PRODUCT VISUALIZATION · FINAL MATERIALS MAY VARY", anchor="lm", fill="white", font=font(FONT_BODY_BOLD, 20))

    pack = packaging(name).rotate(-4, expand=True, resample=Image.Resampling.BICUBIC)
    shadowed_paste(base, pack, (85, 190), 28, 80)

    canvas = stitched_canvas(chart, 610, 36, unfinished=unfinished).rotate(5, expand=True, resample=Image.Resampling.BICUBIC)
    shadowed_paste(base, canvas, (730, 180), 28, 100)

    colors = [THREAD[c] for c in ["R", "Y", "G", "B", "N", "C"]]
    for i, c in enumerate(colors):
        tc = thread_card(c, f"{i+1:02d}").rotate(-7 + i * 2, expand=True, resample=Image.Resampling.BICUBIC)
        x = 630 + i * 135
        y = 980 + (i % 2) * 30
        shadowed_paste(base, tc, (x, y), 13, 70)

    card = instruction_card().rotate(4, expand=True, resample=Image.Resampling.BICUBIC)
    shadowed_paste(base, card, (1080, 920), 22, 70)

    # needle and threader
    d = ImageDraw.Draw(base)
    d.line((800, 1320, 1220, 1460), fill="#858A91", width=12)
    d.ellipse((1207, 1451, 1236, 1476), outline="#858A91", width=7)
    d.ellipse((1245, 1330, 1335, 1420), outline=MUSTARD, width=13)
    d.polygon([(1290, 1420), (1277, 1480), (1305, 1480)], fill=MUSTARD)

    d.text((80, 1510), f"{name} · founding design", fill=INK, font=font(FONT_HEAD, 34))
    base.convert("RGB").save(ASSETS / filename, quality=93)
    shutil.copy2(ASSETS / filename, PREVIEW_ASSETS / filename)


def make_detail(filename, name, chart, seed, accent):
    base = paper_background(seed, "#E8DDC7").convert("RGBA")
    d = ImageDraw.Draw(base)
    canvas = stitched_canvas(chart, 1120, 55, unfinished=False).rotate(-3, expand=True, resample=Image.Resampling.BICUBIC)
    shadowed_paste(base, canvas, (190, 120), 34, 110)
    d.rounded_rectangle((80, 1240, 780, 1510), radius=14, fill=CREAM, outline=INK, width=5)
    d.text((120, 1295), name.upper(), fill=INK, font=font(FONT_HEAD, 45))
    d.text((120, 1370), "ORIGINAL 30 × 30 STITCH ART", fill=accent, font=font(FONT_BODY_BOLD, 23))
    d.text((120, 1420), "Digital visualization · final canvas pending sample approval", fill=INK, font=font(FONT_BODY, 18))
    base.convert("RGB").save(ASSETS / filename, quality=93)
    shutil.copy2(ASSETS / filename, PREVIEW_ASSETS / filename)


def make_contents(filename, name, chart, seed):
    base = paper_background(seed, CREAM).convert("RGBA")
    d = ImageDraw.Draw(base)
    d.text((80, 80), "PLANNED KIT CONTENTS", fill=POPPY, font=font(FONT_BODY_BOLD, 25))
    d.text((80, 130), name, fill=INK, font=font(FONT_HEAD, 60))
    canvas = stitched_canvas(chart, 490, 32, unfinished=True).rotate(-4, expand=True, resample=Image.Resampling.BICUBIC)
    shadowed_paste(base, canvas, (80, 300), 24, 80)
    card = instruction_card((360, 460)).rotate(5, expand=True, resample=Image.Resampling.BICUBIC)
    shadowed_paste(base, card, (1140, 230), 20, 70)
    colors = [THREAD[c] for c in ["R", "Y", "G", "B", "N", "C"]]
    for i, c in enumerate(colors):
        tc = thread_card(c, str(i+1), (125, 205)).rotate((-6+i*2), expand=True, resample=Image.Resampling.BICUBIC)
        shadowed_paste(base, tc, (630 + (i % 3) * 155, 330 + (i // 3) * 270), 10, 60)
    items = ["Printed canvas", "Pre-sorted thread", "Blunt needle", "Threader", "Quick-start card", "Original video help"]
    for i, item in enumerate(items):
        y = 1100 + i * 62
        d.ellipse((820, y, 842, y+22), fill=[POPPY, MUSTARD, SAGE, BLUE, INK, POPPY][i])
        d.text((870, y-7), item, fill=INK, font=font(FONT_BODY_BOLD, 24))
    base.convert("RGB").save(ASSETS / filename, quality=93)
    shutil.copy2(ASSETS / filename, PREVIEW_ASSETS / filename)


def make_duo():
    base = paper_background(51).convert("RGBA")
    d = ImageDraw.Draw(base)
    d.rectangle((0, 0, W, 120), fill=POPPY)
    d.text((70, 60), "FIRST STITCH DUO · PICK ANY TWO", anchor="lm", fill="white", font=font(FONT_BODY_BOLD, 25))
    for name, chart, x, y, rot in [
        ("Night Garden", flower_chart(), 110, 250, -5),
        ("Lucky Sardine", sardine_chart(), 720, 300, 5),
    ]:
        pack = packaging(name, size=(590, 780)).rotate(rot, expand=True, resample=Image.Resampling.BICUBIC)
        shadowed_paste(base, pack, (x, y), 30, 90)
        canvas = stitched_canvas(chart, 380, 28).rotate(-rot, expand=True, resample=Image.Resampling.BICUBIC)
        shadowed_paste(base, canvas, (x+210, y+520), 20, 90)
    d.rounded_rectangle((80, 1390, 1520, 1530), radius=18, fill=INK)
    d.text((800, 1460), "TWO COMPLETE PROJECTS · KEEP BOTH OR MAKE ONE TOGETHER", anchor="mm", fill=CREAM, font=font(FONT_BODY_BOLD, 24))
    base.convert("RGB").save(ASSETS / "first-stitch-duo.png", quality=93)
    shutil.copy2(ASSETS / "first-stitch-duo.png", PREVIEW_ASSETS / "first-stitch-duo.png")
    shutil.copy2(ASSETS / "first-stitch-duo.png", ASSETS / "duo-layout.png")
    shutil.copy2(ASSETS / "first-stitch-duo.png", PREVIEW_ASSETS / "duo-layout.png")


def make_rescue():
    base = paper_background(88).convert("RGBA")
    d = ImageDraw.Draw(base)
    d.text((90, 100), "STITCH RESCUE PACK", fill=INK, font=font(FONT_HEAD, 62))
    d.text((92, 180), "BACKUP TOOLS FOR A CALMER FINISH", fill=POPPY, font=font(FONT_BODY_BOLD, 24))
    card = Image.new("RGBA", (1050, 800), (0,0,0,0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((10,10,1040,790), radius=22, fill=CREAM, outline=INK, width=7)
    cd.text((70, 80), "INCLUDED", fill=POPPY, font=font(FONT_BODY_BOLD, 23))
    for i, item in enumerate(["1 blunt tapestry needle", "1 brass threader", "matching thread reserve"]):
        cd.text((90, 180+i*150), f"0{i+1}", fill=MUSTARD, font=font(FONT_HEAD, 50))
        cd.text((190, 190+i*150), item, fill=INK, font=font(FONT_BODY_BOLD, 30))
    cd.line((90,650,950,650), fill="#CFC3AC", width=3)
    cd.text((90, 690), "ADULT USE · CONTAINS A NEEDLE", fill=INK, font=font(FONT_BODY, 20))
    card = card.rotate(-3, expand=True, resample=Image.Resampling.BICUBIC)
    shadowed_paste(base, card, (230, 360), 35, 95)
    d.line((420, 1240, 1120, 1450), fill="#858A91", width=18)
    d.ellipse((1098, 1438, 1140, 1472), outline="#858A91", width=9)
    d.ellipse((1120, 1170, 1280, 1330), outline=MUSTARD, width=18)
    base.convert("RGB").save(ASSETS / "stitch-rescue-pack.png", quality=93)
    shutil.copy2(ASSETS / "stitch-rescue-pack.png", PREVIEW_ASSETS / "stitch-rescue-pack.png")


def make_logo():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 160" role="img" aria-labelledby="t"><title id="t">First Thread Studio</title><rect width="720" height="160" fill="none"/><text x="0" y="80" fill="#16263B" font-family="Georgia,serif" font-size="70" font-weight="700">First Thread</text><text x="4" y="130" fill="#D85143" font-family="Arial,sans-serif" font-size="24" font-weight="700" letter-spacing="9">STUDIO</text><path d="M600 35c48 0 70 28 70 52s-22 42-52 42c-34 0-48-22-48-42 0-15 10-28 26-28 14 0 24 9 24 20" fill="none" stroke="#E4AC42" stroke-width="8" stroke-linecap="round"/><circle cx="600" cy="79" r="5" fill="#16263B"/></svg>'''
    (ASSETS / "first-thread-logo.svg").write_text(svg, encoding="utf-8")
    (PREVIEW_ASSETS / "first-thread-logo.svg").write_text(svg, encoding="utf-8")


def optimize_assets():
    """Preserve lossless masters and publish lightweight storefront WebP files."""
    for png in sorted(ASSETS.glob("*.png")):
        master = MASTER_ASSETS / png.name
        shutil.copy2(png, master)
        webp_name = png.with_suffix(".webp").name
        with Image.open(png) as image:
            rgb = image.convert("RGB")
            rgb.save(ASSETS / webp_name, "WEBP", quality=88, method=6)
            rgb.save(PREVIEW_ASSETS / webp_name, "WEBP", quality=88, method=6)
        preview_png = PREVIEW_ASSETS / png.name
        if preview_png.exists():
            preview_png.unlink()
        png.unlink()


def write_csv():
    data = json.loads((ROOT / "store_data.json").read_text(encoding="utf-8"))
    out = ROOT / "shopify_products_import.csv"
    fields = ["Handle","Title","Body (HTML)","Vendor","Product Category","Type","Tags","Published","Option1 Name","Option1 Value","Variant SKU","Variant Grams","Variant Inventory Tracker","Variant Inventory Qty","Variant Inventory Policy","Variant Fulfillment Service","Variant Price","Variant Compare At Price","Variant Requires Shipping","Variant Taxable","Image Src","Image Position","Image Alt Text","Gift Card","SEO Title","SEO Description","Status"]
    rows = []
    for product in data["products"]:
        for i, image in enumerate(product["images"], start=1):
            row = {k:"" for k in fields}
            row["Handle"] = product["handle"]
            if i == 1:
                row.update({
                    "Title":product["title"],"Body (HTML)":product["description_html"],"Vendor":data["brand"]["name"],
                    "Product Category":(
                        "Arts & Entertainment > Hobbies & Creative Arts > Arts & Crafts > Art & Crafting Tools > Needles & Hooks > Hand-Sewing Needles > Tapestry Needles"
                        if product["handle"] == "stitch-rescue-pack"
                        else "Arts & Entertainment > Hobbies & Creative Arts > Arts & Crafts > Art & Craft Kits > Needlecraft Kits"
                    ),
                    "Type":product["product_type"],"Tags":", ".join(product["tags"]),"Published":"FALSE",
                    "Option1 Name":"Title","Option1 Value":"Default Title","Variant SKU":product["sku"],"Variant Grams":"",
                    "Variant Inventory Tracker":"shopify","Variant Inventory Qty":"0","Variant Inventory Policy":"deny",
                    "Variant Fulfillment Service":"manual","Variant Price":product["price"],"Variant Compare At Price":product["compare_at_price"],
                    "Variant Requires Shipping":"TRUE","Variant Taxable":"TRUE","Gift Card":"FALSE",
                    "SEO Title":product["seo_title"],"SEO Description":product["seo_description"],"Status":"draft"
                })
            row["Image Src"] = f"__PUBLIC_ASSET_BASE__/{image}"
            row["Image Position"] = str(i)
            row["Image Alt Text"] = f"Digital visualization of the planned {product['short_title']} product; final materials may vary."
            rows.append(row)
    with out.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader(); w.writerows(rows)

    # Safe pre-media import: one complete draft row per product, with no URL sentinel.
    no_images = ROOT / "shopify_products_import_no_images.csv"
    complete_rows = []
    for row in rows:
        if not row["Title"]:
            continue
        clean = dict(row)
        clean["Image Src"] = ""
        clean["Image Position"] = ""
        clean["Image Alt Text"] = ""
        complete_rows.append(clean)
    with no_images.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader(); w.writerows(complete_rows)


def main():
    charts = {
        "night-garden": ("Night Garden", flower_chart(), POPPY),
        "lucky-sardine": ("Lucky Sardine", sardine_chart(), BLUE),
        "little-victory": ("Little Victory", victory_chart(), MUSTARD),
    }
    for i, (slug, (name, chart, accent)) in enumerate(charts.items(), start=1):
        make_kit_photo(f"{slug}-kit.png", name, chart, 20+i, accent, unfinished=(slug=="night-garden"))
        make_detail(f"{slug}-detail.png", name, chart, 30+i, accent)
        make_contents(f"kit-contents-{slug}.png", name, chart, 40+i)
    make_duo(); make_rescue(); make_logo(); optimize_assets(); write_csv()
    print(
        f"Generated {len(list(MASTER_ASSETS.glob('*.png')))} master PNGs, "
        f"{len(list(ASSETS.glob('*.webp')))} optimized WebP assets, logo, and Shopify product CSV"
    )


if __name__ == "__main__":
    main()
