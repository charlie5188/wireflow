#!/usr/bin/env python3
"""Render a flow-spec.json and its screen captures as one offline, bilingual flow-map HTML file."""
import argparse, base64, json, math, mimetypes, re
from pathlib import Path

ID = re.compile(r"[A-Za-z][A-Za-z0-9_.:-]{0,79}")
LANGS = ("en", "ja")


def text_ok(value):
    return isinstance(value, str) or (isinstance(value, dict) and all(isinstance(value.get(k), str) and value[k] for k in LANGS))


def rect_ok(r, vw, vh):
    return isinstance(r, dict) and all(isinstance(r.get(k), (int, float)) and math.isfinite(r[k]) for k in "xywh") \
        and r["w"] > 0 and r["h"] > 0 and 0 <= r["x"] <= vw and 0 <= r["y"] <= vh


def validate(spec, root):
    vw, vh = spec["viewport"]["width"], spec["viewport"]["height"]
    screens = spec["screens"]
    ids = [s["id"] for s in screens]
    if not ids or len(set(ids)) != len(ids) or not all(ID.fullmatch(i) for i in ids):
        raise ValueError("Screen IDs must be present, unique and safe")
    if not text_ok(spec["title"]):
        raise ValueError("title needs en and ja text")
    cells = set()
    for s in screens:
        if not text_ok(s["title"]):
            raise ValueError(f"{s['id']}: title needs en and ja text")
        cell = (s["grid"]["col"], s["grid"]["row"])
        if cell in cells:
            raise ValueError(f"{s['id']}: grid cell {cell} is already used")
        cells.add(cell)
        for n in s.get("notes", []):
            if not text_ok(n["text"]) or ("anchor" in n and not rect_ok(n["anchor"], vw, vh)):
                raise ValueError(f"{s['id']}: note needs en/ja text and an anchor inside the viewport")
        path = (root / s["capture"]).resolve()
        if root not in path.parents or not path.is_file():
            raise ValueError(f"{s['id']}: capture must be a file inside the input directory")
    tids = [t["id"] for t in spec["transitions"]]
    if len(set(tids)) != len(tids) or not all(ID.fullmatch(i) for i in tids):
        raise ValueError("Transition IDs must be unique and safe")
    for t in spec["transitions"]:
        if t["from"] not in ids or t["to"] not in ids:
            raise ValueError(f"{t['id']}: from/to must name a screen")
        if not text_ok(t["trigger"]) or not text_ok(t["effect"]):
            raise ValueError(f"{t['id']}: trigger and effect need en and ja text")
        if "anchor" in t and not rect_ok(t["anchor"], vw, vh):
            raise ValueError(f"{t['id']}: anchor must sit inside the source viewport")
    for b in spec.get("bands", []):
        if not text_ok(b["title"]) or not set(b["screens"]) <= set(ids):
            raise ValueError("Bands need en/ja titles and existing screen IDs")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input_dir", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    root = args.input_dir.resolve()
    spec = json.loads((root / "flow-spec.json").read_text(encoding="utf-8"))
    validate(spec, root)
    vw, vh = spec["viewport"]["width"], spec["viewport"]["height"]
    comment_w = spec.get("commentWidth", 620)
    col_step = vw + 70 + comment_w + spec.get("columnGap", 900)
    row_step = vh + spec.get("rowGap", 960)
    images = {}
    for s in spec["screens"]:
        s["x"], s["y"] = round(s["grid"]["col"] * col_step), round(s["grid"]["row"] * row_step)
        cap = root / s["capture"]
        mime = mimetypes.guess_type(cap.name)[0]
        if mime not in ("image/png", "image/jpeg", "image/webp"):
            raise ValueError("Captures must be PNG, JPEG or WebP")
        images[s["id"]] = f"data:{mime};base64," + base64.b64encode(cap.read_bytes()).decode()
    payload = dict(spec, images=images)
    template = (Path(__file__).resolve().parent.parent / "assets/flow-map.html").read_text(encoding="utf-8")
    title = spec["title"]["en"] if isinstance(spec["title"], dict) else spec["title"]
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    html = template.replace("__TITLE__", title.replace("<", "&lt;")).replace("__PAYLOAD__", data)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html, encoding="utf-8")
    print(json.dumps({"screens": len(spec["screens"]), "transitions": len(spec["transitions"]),
                      "keyPaths": sum(1 for t in spec["transitions"] if t.get("key"))}))


if __name__ == "__main__":
    main()
