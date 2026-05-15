#!/usr/bin/env python3
"""Build brand-pop-quiz: embed logo images from assets/ into a single index.html."""
import sys
import pathlib

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent))

from _builder import emit  # noqa: E402

ITEMS = [
    # Electronics & appliances
    ("Samsung",      "samsung.png"),
    ("LG",           "lg-logo.png"),
    ("Panasonic",    "Panasonic-logo.jpg"),
    ("Mitsubishi",   "mitsubishi-logo.jpg"),
    ("Haier",        "haier.jpeg"),
    ("Daikin",       "daikin.jpg"),
    ("Godrej",       "godrej.jpeg"),
    ("Lloyd",        "llyod.jpeg"),
    ("Blue Star",    "bluestar.png"),
    ("Usha",         "usha.png"),
    ("Atomberg",     "atomberg.png"),
    # Conglomerates / retail / cars
    ("Tata",         "tata.png"),
    ("Croma",        "croma.jpeg"),
    ("Thar",         "thar.jpeg"),
    # Apps the kid knows
    ("WhatsApp",     "whatsapp.jpeg"),
    ("YouTube",      "youtube.png"),
    ("YouTube Kids", "youtube-kids.png"),
    ("Spotify",      "spotify.png"),
    ("Talking Tom",  "talking-tom.jpeg"),
]

entries = [(name, HERE / "assets" / fname) for name, fname in ITEMS]
emit("Brand Pop Quiz", HERE, entries)
