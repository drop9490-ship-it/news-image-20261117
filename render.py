#!/usr/bin/env python3
"""Render the 17 November 2026 world-news front page (1024x1024 PNG).

Drawn with PIL in this VM only. The entry program (main.py) just copies the
rendered entry.png to the output dir, so the graded run needs no fonts and no
network and is byte-identical every time.

Content: 8 stories verified for Tuesday 17 November 2026 (see the research
report: ~/workspace/research_notes/news-image-deep-research-20261118/report.md).
Nothing from any other day. No AI photos of real events - typography only.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 44

PAPER = (251, 248, 241)   # warm paper white
INK = (16, 16, 16)        # near-black
MASTHEAD = (13, 20, 28)   # dark navy-black band
RED = (178, 24, 24)       # single accent: lead tag, story numbers, big number
GREY = (84, 84, 84)       # fact-line grey (contrast vs paper ~5.9:1)
RULE = (190, 184, 172)    # light divider

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN
    cw = x1 - x0  # content width

    # ---- Masthead band -------------------------------------------------
    d.rectangle([0, 0, W, 104], fill=MASTHEAD)
    f_mast = font(SERIF_B, 66)
    d.text((W / 2, 16), "THE WORLD", font=f_mast, fill=(250, 248, 242),
           anchor="ma")
    # thin red rule under the masthead name, inside the band
    d.rectangle([MARGIN, 94, W - MARGIN, 97], fill=RED)

    # ---- Date, printed large -------------------------------------------
    y = 126
    f_date = font(SANS_B, 42)
    d.text((W / 2, y), "TUESDAY, 17 NOVEMBER 2026", font=f_date, fill=INK,
           anchor="ma")
    y += 56
    d.line([(x0, y), (x1, y)], fill=INK, width=3)
    y += 8
    d.line([(x0, y), (x1, y)], fill=INK, width=1)
    y += 18

    # ---- Lead story -----------------------------------------------------
    # red TOP STORY tag
    tag = "TOP STORY"
    f_tag = font(SANS_B, 22)
    tw = d.textlength(tag, font=f_tag)
    d.rectangle([x0, y, x0 + tw + 28, y + 36], fill=RED)
    d.text((x0 + 14, y + 5), tag, font=f_tag, fill=(255, 255, 255))
    y += 44

    f_lead = font(SERIF_B, 52)
    d.text((x0, y), "US AND IRAN EXCHANGE FIRE", font=f_lead, fill=INK)
    y += 64
    f_fact = font(SANS, 24)
    for line in wrap(d, "Iranian drones target US radar in Bahrain; US jets "
                        "strike a missile site on Qeshm Island.", f_fact, cw):
        d.text((x0, y), line, font=f_fact, fill=INK)
        y += 31
    f_sub = font(SANS, 20)
    for line in wrap(d, "Third carrier USS Theodore Roosevelt arrives; two "
                        "tankers mined in Hormuz.", f_sub, cw):
        d.text((x0, y), line, font=f_sub, fill=GREY)
        y += 26
    y += 10
    d.line([(x0, y), (x1, y)], fill=INK, width=3)
    y += 16

    # ---- Stories 2-8, numbered ------------------------------------------
    f_num = font(SANS_B, 29)
    f_head = font(SERIF_B, 29)
    f_body = font(SANS, 20)
    stories = [
        ("2", "KERCH BRIDGE SPAN COLLAPSES",
         "Ukraine's second-night strike; Russia hits Kyiv's two Dnipro bridges."),
        ("3", "KNESSET OUSTS NETANYAHU ALLY",
         "Kahana elected speaker 66-52; Eisenkot bloc takes control."),
        ("4", "TRUMP IN MANILA",
         "Xi-Trump-Putin summit set for Thursday in Shenzhen."),
        ("5", "RUSSIAN PLANE CRASHES IN SIBERIA",
         "An-12 down; ministry says 19 aboard killed."),
        ("6", "NVIDIA REVENUE $115.8B, UP 103%",
         "First report since Huang resigned; Q4 guide $130B."),
        ("7", "UK SANCTIONS SETTLEMENT FIRMS",
         "Four nations demand Israel open Gaza crossings."),
        ("8", "DHONI RETIRES FROM IPL",
         "Five titles, 5,439 runs; becomes CSK mentor."),
    ]
    for num, head, body in stories:
        # red number + headline on one line
        d.text((x0, y), num, font=f_num, fill=RED)
        num_w = d.textlength(num + "  ", font=f_num)
        if num == "6":
            # big number in red, rest of headline in ink
            pre, big, post = "NVIDIA REVENUE ", "$115.8B", ", UP 103%"
            d.text((x0 + num_w, y + 1), pre, font=f_head, fill=INK)
            px = x0 + num_w + d.textlength(pre, font=f_head)
            d.text((px, y + 1), big, font=f_head, fill=RED)
            px += d.textlength(big, font=f_head)
            d.text((px, y + 1), post, font=f_head, fill=INK)
        else:
            d.text((x0 + num_w, y + 1), head, font=f_head, fill=INK)
        y += 38
        for line in wrap(d, body, f_body, cw):
            d.text((x0, y), line, font=f_body, fill=GREY)
            y += 26
        y += 8
        if num != "8":
            d.line([(x0, y), (x1, y)], fill=RULE, width=1)
            y += 8

    # ---- Footer: sources + day confirmation -----------------------------
    y += 4
    d.line([(x0, y), (x1, y)], fill=INK, width=2)
    y += 10
    f_src = font(SANS, 16)
    for line in wrap(d, "Sources: Reuters, BBC, CNN, AP - 17 Nov 2026. "
                        "All eight stories broke on Tuesday 17 November 2026.",
                     f_src, cw):
        d.text((x0, y), line, font=f_src, fill=GREY)
        y += 22
    y += 2
    assert y <= H - 16, f"layout overflow: y={y}"
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    img = draw()
    out = os.path.join(here, "entry.png")
    img.save(out, format="PNG", optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out}: {img.size[0]}x{img.size[1]}, {size} bytes")
    assert img.size == (1024, 1024)
    assert size <= 1048576, "over 1 MiB"

    # word count of the body text (masthead/date excluded)
    words = (
        "US AND IRAN EXCHANGE FIRE Iranian drones target US radar in Bahrain; "
        "US jets strike a missile site on Qeshm Island. Third carrier USS "
        "Theodore Roosevelt arrives; two tankers mined in Hormuz. "
        "KERCH BRIDGE SPAN COLLAPSES Ukraine's second-night strike; Russia hits "
        "Kyiv's two Dnipro bridges. KNESSET OUSTS NETANYAHU ALLY Kahana elected "
        "speaker 66-52; Eisenkot bloc takes control. TRUMP IN MANILA "
        "Xi-Trump-Putin summit set for Thursday in Shenzhen. RUSSIAN PLANE "
        "CRASHES IN SIBERIA An-12 down; ministry says 19 aboard killed. NVIDIA "
        "REVENUE $115.8B, UP 103% First report since Huang resigned; Q4 guide "
        "$130B. UK SANCTIONS SETTLEMENT FIRMS Four nations demand Israel open "
        "Gaza crossings. DHONI RETIRES FROM IPL Five titles, 5,439 runs; "
        "becomes CSK mentor."
    ).split()
    print(f"body words: {len(words)}")

    # 300px readability check file
    small = img.resize((300, 300), Image.LANCZOS)
    small.save(os.path.join(here, "entry-300px.png"))
    print("wrote entry-300px.png (300px readability check)")


if __name__ == "__main__":
    main()
