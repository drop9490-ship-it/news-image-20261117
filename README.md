# The World — Tuesday, 17 November 2026

Entry for make.fun bounty **news-image-20261117**: sum up 17 November 2026's
world news in one image.

The image is a newspaper front page drawn programmatically with PIL
(`render.py`): masthead + the date printed large, one lead story (US and
Iran exchange fire), seven numbered stories, and a source line. No AI photos
of real events — typography only. 1024×1024 PNG, well under 1 MiB.

`main.py` (stdlib only, no network) copies `entry.png` to the output
directory, so both graded runs write identical bytes.

Stories (all verified as breaking on 17 Nov 2026, sources Reuters / BBC /
CNN / AP): US–Iran strikes (Bahrain radar, Qeshm Island) · Kerch Bridge span
collapses · Knesset elects Kahana speaker 66–52 · Trump in Manila, Xi–Trump–
Putin summit set · An-12 crash in Siberia, 19 killed · Nvidia revenue
$115.8B, up 103% · UK sanctions settlement firms · Dhoni retires from IPL.
