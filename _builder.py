"""Shared helpers: embed images and render the index.html template."""

import base64
import io
import json
import pathlib
import urllib.parse
import urllib.request

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

ROOT = pathlib.Path(__file__).parent
TEMPLATE = ROOT / "_template.html"

UA = "html-css-js-projects/1.0 (https://github.com/somanathghalimath/html-css-js-projects; hobby)"

MIME_BY_EXT = {
    ".jpg":  "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png":  "image/png",
    ".webp": "image/webp",
    ".gif":  "image/gif",
}

# Anything wider/taller than this gets downscaled. 1000 looks crisp on
# retina phones and tablets while keeping the embedded payload small.
MAX_DIM = 1000
JPEG_QUALITY = 82


def _optimize(raw_bytes, suffix):
    """Return (bytes, mime). Downscale large images and re-encode."""
    suffix = suffix.lower()
    mime = MIME_BY_EXT.get(suffix, "application/octet-stream")
    if not HAS_PIL or suffix not in (".jpg", ".jpeg", ".png", ".webp"):
        return raw_bytes, mime

    try:
        with Image.open(io.BytesIO(raw_bytes)) as im:
            w, h = im.size
            needs_resize = max(w, h) > MAX_DIM
            # For JPEGs we always re-encode at our quality cap (saves bytes
            # even when dimensions are already fine). PNGs are only touched
            # if they need resizing — preserves lossless brand logos.
            needs_recompress = suffix in (".jpg", ".jpeg")
            if not needs_resize and not needs_recompress:
                return raw_bytes, mime

            if needs_resize:
                im.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)

            buf = io.BytesIO()
            if suffix in (".jpg", ".jpeg"):
                if im.mode != "RGB":
                    im = im.convert("RGB")
                im.save(buf, format="JPEG", quality=JPEG_QUALITY,
                        optimize=True, progressive=True)
                mime = "image/jpeg"
            elif suffix == ".png":
                im.save(buf, format="PNG", optimize=True)
            elif suffix == ".webp":
                im.save(buf, format="WEBP", quality=JPEG_QUALITY, method=6)
            new_bytes = buf.getvalue()
            # Keep whichever is smaller (avoid making files bigger)
            if len(new_bytes) < len(raw_bytes):
                return new_bytes, mime
            return raw_bytes, MIME_BY_EXT[suffix]
    except Exception as e:
        print("  (skip optimize for " + suffix + ": " + str(e) + ")")
        return raw_bytes, MIME_BY_EXT[suffix]


def data_uri(path):
    raw = path.read_bytes()
    optimized, mime = _optimize(raw, path.suffix)
    if len(optimized) < len(raw):
        delta = (len(raw) - len(optimized)) / 1024
        print("  optimized " + path.name + ": " +
              str(round(len(raw)/1024)) + " KB -> " +
              str(round(len(optimized)/1024)) + " KB (-" +
              str(round(delta)) + " KB)")
    b64 = base64.b64encode(optimized).decode("ascii")
    return "data:" + mime + ";base64," + b64


def find_existing(assets_dir, stem):
    for ext in MIME_BY_EXT:
        p = assets_dir / (stem + ext)
        if p.exists():
            return p
    return None


def fetch_wikipedia_portrait(title, assets_dir, stem):
    qs = urllib.parse.urlencode({
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "piprop": "thumbnail",
        "pithumbsize": "600",
        "titles": title,
    })
    url = "https://en.wikipedia.org/w/api.php?" + qs
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    page = next(iter(data["query"]["pages"].values()))
    if "thumbnail" not in page:
        raise RuntimeError("No thumbnail on Wikipedia for " + repr(title))
    img_url = page["thumbnail"]["source"]

    bare = urllib.parse.urlsplit(img_url).path.lower()
    if   bare.endswith(".png"):  ext = ".png"
    elif bare.endswith(".webp"): ext = ".webp"
    elif bare.endswith(".jpeg"): ext = ".jpeg"
    else:                        ext = ".jpg"

    out_path = assets_dir / (stem + ext)
    print("  -> downloading " + img_url)
    req = urllib.request.Request(img_url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        out_path.write_bytes(resp.read())
    return out_path


def emit(title, project_dir, entries, features=None):
    """Render the template and write <project_dir>/index.html.

    entries:  list of (display_name, image_path).
    features: optional dict of opt-in features (e.g. {"scratch": True}).
    """
    items = [{"name": name, "src": data_uri(path)} for name, path in entries]
    items_json = json.dumps(items, ensure_ascii=False)
    features_json = json.dumps(features or {})
    html = TEMPLATE.read_text(encoding="utf-8")
    html = (html
        .replace("{{TITLE}}", title)
        .replace("{{TOTAL}}", str(len(items)))
        .replace("{{ITEMS_JSON}}", items_json)
        .replace("{{FEATURES_JSON}}", features_json))
    out = project_dir / "index.html"
    out.write_text(html, encoding="utf-8")
    print("Wrote " + str(out) + " (" + str(round(out.stat().st_size / 1024, 1)) + " KB)")
