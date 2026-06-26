#!/usr/bin/env python3
"""Generate Peter's first field-walk water clue map from local farm exports."""

from __future__ import annotations

import argparse
import html
import json
import re
import statistics
import zipfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


DORSET_BBOX = {
    "min_lat": 50.0,
    "max_lat": 51.0,
    "min_lon": -3.0,
    "max_lon": -2.0,
}

RISK_CLUES = {
    "kitehill": ["very high erosion risk", "high runoff risk", "steep slope"],
    "higher kitehill": ["very high erosion risk", "high runoff risk", "steep slope"],
    "rookery mead meadow": ["high runoff risk", "steep slope"],
    "river": ["high erosion risk", "moderate runoff risk"],
    "road": ["high erosion risk", "moderate runoff risk"],
    "puddletown down": ["high erosion risk", "moderate runoff risk"],
    "fat ox": ["high erosion risk", "moderate runoff risk"],
    "chebbard drive": ["high erosion risk", "moderate runoff risk"],
    "bulls ground": ["high erosion risk", "moderate runoff risk"],
    "chalky ground": ["high erosion risk", "moderate runoff risk"],
    "cowleaze": ["high erosion risk", "moderate runoff risk"],
    "lower flippings": ["high erosion risk", "moderate runoff risk"],
}

NAME_CLUES = {
    "river": ("name suggests river/water edge", 5),
    "mead": ("name suggests meadow/wetter ground", 2),
    "meadow": ("name suggests meadow/wetter ground", 2),
    "lower": ("name suggests lower ground", 1),
    "cowleaze": ("name suggests old pasture/leaze", 2),
    "flippings": ("local named clue: flippings/lower ground", 1),
    "margin": ("field margin clue", 1),
    "road": ("roadside runoff interception clue", 1),
}

RISK_WEIGHTS = {
    "high runoff risk": 5,
    "moderate runoff risk": 2,
    "very high erosion risk": 4,
    "high erosion risk": 3,
    "steep slope": 3,
}


@dataclass
class FieldShape:
    name: str
    source_zip: str
    rings: list[list[list[float]]]
    centre_lat: float
    centre_lon: float
    points: int


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def in_dorset(lat: float, lon: float) -> bool:
    return (
        DORSET_BBOX["min_lat"] <= lat <= DORSET_BBOX["max_lat"]
        and DORSET_BBOX["min_lon"] <= lon <= DORSET_BBOX["max_lon"]
    )


def parse_coordinates(text: str) -> list[list[float]]:
    points: list[list[float]] = []
    for raw in text.split():
        bits = raw.split(",")
        if len(bits) < 2:
            continue
        lon, lat = float(bits[0]), float(bits[1])
        if in_dorset(lat, lon):
            points.append([lat, lon])
    return points


def read_kml_shapes(raw_dir: Path) -> list[FieldShape]:
    fields: list[FieldShape] = []
    ns = {"kml": "http://www.opengis.net/kml/2.2"}
    for zip_path in sorted(raw_dir.glob("Field_*.zip")):
        with zipfile.ZipFile(zip_path) as archive:
            kml_names = [name for name in archive.namelist() if name.lower().endswith(".kml")]
            if not kml_names:
                continue
            kml_text = archive.read(kml_names[0]).decode("utf-8", errors="replace")

        root = ET.fromstring(kml_text)
        rings: list[list[list[float]]] = []
        for coords in root.findall(".//kml:coordinates", ns):
            if coords.text:
                ring = parse_coordinates(coords.text)
                if len(ring) >= 3:
                    rings.append(ring)

        if not rings:
            continue

        flat = [point for ring in rings for point in ring]
        centre_lat = statistics.fmean(point[0] for point in flat)
        centre_lon = statistics.fmean(point[1] for point in flat)
        if not in_dorset(centre_lat, centre_lon):
            continue

        name = zip_path.stem.removeprefix("Field_").replace("_", " ").strip()
        fields.append(
            FieldShape(
                name=name,
                source_zip=zip_path.name,
                rings=rings,
                centre_lat=centre_lat,
                centre_lon=centre_lon,
                points=len(flat),
            )
        )
    return fields


def risk_for_field(name: str) -> list[str]:
    normal = slug(name)
    clues: list[str] = []
    for key, values in RISK_CLUES.items():
        if key in normal or normal in key:
            clues.extend(values)
    return sorted(set(clues))


def score_field(field: FieldShape) -> dict:
    normal = slug(field.name)
    score = 0
    clues: list[str] = []
    for token, (label, weight) in NAME_CLUES.items():
        if token in normal:
            score += weight
            clues.append(label)

    risks = risk_for_field(field.name)
    for risk in risks:
        score += RISK_WEIGHTS.get(risk, 1)
        clues.append(risk)

    if score >= 9:
        priority = "high"
    elif score >= 4:
        priority = "medium"
    elif score > 0:
        priority = "low"
    else:
        priority = "background"

    return {
        "name": field.name,
        "source_zip": field.source_zip,
        "rings": field.rings,
        "centre": [field.centre_lat, field.centre_lon],
        "score": score,
        "priority": priority,
        "clues": clues or ["no current water clue; shown for orientation"],
    }


def render_html(records: list[dict]) -> str:
    ranked = sorted(records, key=lambda rec: (-rec["score"], rec["name"]))
    centre_lat = statistics.fmean(rec["centre"][0] for rec in records)
    centre_lon = statistics.fmean(rec["centre"][1] for rec in records)
    data = json.dumps(ranked, separators=(",", ":"))
    top_items = "\n".join(
        f"<li><button data-field='{html.escape(rec['name'], quote=True)}'>"
        f"<strong>{html.escape(rec['name'])}</strong>"
        f"<span>{rec['priority']} · score {rec['score']} · {html.escape('; '.join(rec['clues'][:3]))}</span>"
        "</button></li>"
        for rec in ranked[:14]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>RegenOS Water Walk Map</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <style>
    html, body {{ height: 100%; margin: 0; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #17211b; }}
    body {{ background: #eef2ec; }}
    .app {{ min-height: 100%; display: grid; grid-template-rows: auto minmax(52vh, 1fr) auto; }}
    header {{ padding: 10px 12px; background: #f8faf5; border-bottom: 1px solid #d7ddcf; }}
    h1 {{ margin: 0; font-size: 18px; font-weight: 750; }}
    .meta {{ margin-top: 4px; font-size: 12px; color: #586255; }}
    #map {{ width: 100%; height: 100%; min-height: 52vh; }}
    .sheet {{ max-height: 38vh; overflow: auto; background: #f8faf5; border-top: 1px solid #d7ddcf; }}
    .notice {{ padding: 10px 12px; font-size: 13px; line-height: 1.35; background: #fff7d6; border-bottom: 1px solid #eadc93; }}
    ol {{ list-style: none; margin: 0; padding: 0; }}
    li {{ border-bottom: 1px solid #e0e5d9; }}
    button {{ width: 100%; border: 0; background: transparent; text-align: left; padding: 10px 12px; color: inherit; }}
    button strong {{ display: block; font-size: 15px; }}
    button span {{ display: block; margin-top: 3px; font-size: 12px; color: #5d665a; line-height: 1.3; }}
    .legend {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; font-size: 12px; }}
    .legend span {{ display: inline-flex; align-items: center; gap: 4px; }}
    .swatch {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; }}
    .leaflet-popup-content {{ font-size: 13px; line-height: 1.35; }}
    .popup-title {{ font-weight: 750; margin-bottom: 4px; }}
  </style>
</head>
<body>
  <div class="app">
    <header>
      <h1>Water Walk Map</h1>
      <div class="meta">Dewlish field clues · OpenStreetMap base · clue map, not a recommendation</div>
      <div class="legend">
        <span><i class="swatch" style="background:#c43f2f"></i>high</span>
        <span><i class="swatch" style="background:#de8f26"></i>medium</span>
        <span><i class="swatch" style="background:#d3bd4f"></i>low</span>
        <span><i class="swatch" style="background:#8d9a86"></i>orientation</span>
      </div>
    </header>
    <main id="map"></main>
    <section class="sheet">
      <div class="notice">MVP use: walk to the highlighted places, look for wet ground, ditches, springs, standing water, erosion lines, runoff paths, and possible pond/check-dam locations. Ground truth beats this map.</div>
      <ol>{top_items}</ol>
    </section>
  </div>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    const fields = {data};
    const map = L.map('map', {{ preferCanvas: true }}).setView([{centre_lat:.6f}, {centre_lon:.6f}], 14);
    L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap contributors'
    }}).addTo(map);
    const colours = {{
      high: '#c43f2f',
      medium: '#de8f26',
      low: '#d3bd4f',
      background: '#8d9a86'
    }};
    const layers = new Map();
    function popup(rec) {{
      return `<div class="popup-title">${{rec.name}}</div>
        <div><b>Priority:</b> ${{rec.priority}} · score ${{rec.score}}</div>
        <div><b>Why:</b> ${{rec.clues.join('; ')}}</div>
        <div><b>Look for:</b> wet patches, ditches, runoff lines, erosion, water-holding corners.</div>`;
    }}
    for (const rec of fields) {{
      const layer = L.polygon(rec.rings, {{
        color: colours[rec.priority],
        fillColor: colours[rec.priority],
        fillOpacity: rec.priority === 'background' ? 0.08 : 0.28,
        weight: rec.priority === 'background' ? 1 : 3
      }}).bindPopup(popup(rec)).addTo(map);
      layers.set(rec.name, layer);
    }}
    document.querySelectorAll('[data-field]').forEach(button => {{
      button.addEventListener('click', () => {{
        const layer = layers.get(button.dataset.field);
        if (!layer) return;
        map.fitBounds(layer.getBounds(), {{ padding: [24, 24], maxZoom: 16 }});
        layer.openPopup();
      }});
    }});
  </script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", default="local/raw/dewlish-usb-2026-06-26")
    parser.add_argument("--out-dir", default="local/reports/water-walk-map")
    args = parser.parse_args()

    raw_dir = Path(args.raw_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    shapes = read_kml_shapes(raw_dir)
    if not shapes:
        raise SystemExit(f"No Dorset field KML shapes found in {raw_dir}")

    records = [score_field(field) for field in shapes]
    (out_dir / "fields.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    (out_dir / "index.html").write_text(render_html(records), encoding="utf-8")

    top = sorted(records, key=lambda rec: (-rec["score"], rec["name"]))[:10]
    print(f"Wrote {out_dir / 'index.html'}")
    print("Top clues:")
    for rec in top:
        print(f"- {rec['name']}: {rec['priority']} score={rec['score']} ({'; '.join(rec['clues'][:3])})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
