"""Original 2D concept geometry and OpenUSD massing from the scenario.

DXF and USD files are exchange examples, not coordinated CAD/BIM or LOD claims.
"""
from __future__ import annotations
import math
from pathlib import Path

def layout(c: dict) -> tuple[list[dict], list[dict]]:
    # Hall grows with rack rows. SI metres throughout.
    cols = min(10, c["racks_per_hall"])
    rows = math.ceil(c["racks_per_hall"]/cols)
    width, depth = max(20, cols*1.2+8), max(20, rows*3.0+8)
    rooms, racks = [], []
    for h in range(c["halls"]):
        x, y = 10+(h%2)*(width+8), 10+(h//2)*(depth+8)
        hall_id = f"H{h+1:02}"
        rooms.append({"id": hall_id, "x": x, "y": y, "width": width, "depth": depth, "height": 6})
        for r in range(c["racks_per_hall"]):
            racks.append({"asset_id": f"{hall_id}-R{r+1:03}", "hall_id": hall_id,
                          "x": x+4+(r%cols)*1.2, "y": y+4+(r//cols)*3,
                          "width": 0.6, "depth": 1.2, "height": 2.2,
                          "design_kw": c["rack_kw"], "power_a": "LV-A", "power_b": "LV-B"})
    return rooms, racks

def write_geometry(c: dict, out: Path) -> list[dict]:
    rooms, racks = layout(c)
    max_x = max(r["x"]+r["width"] for r in rooms)+10
    max_y = max(r["y"]+r["depth"] for r in rooms)+22
    scale = min(1000/max_x, 680/max_y)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 840" role="img" aria-labelledby="title desc">',
           '<title id="title">Open Data Center Facility - hall and rack concept</title>',
           '<desc id="desc">Original parametric plan. Hall positions and rack IDs align with the asset CSV and USD massing.</desc>',
           '<rect width="1120" height="840" fill="#f1f5f9"/>',
           '<text x="45" y="42" font-family="Arial" font-size="26" fill="#102a43">OPEN DATA CENTER / HALL CONCEPT</text>',
           '<text x="45" y="68" font-family="Arial" font-size="14" fill="#486581">SI metres | white-space concept only | not for construction</text>']
    def rect(x, y, w, d, fill, stroke):
        return f'<rect x="{45+x*scale:.2f}" y="{80+y*scale:.2f}" width="{w*scale:.2f}" height="{d*scale:.2f}" fill="{fill}" stroke="{stroke}"/>'
    for room in rooms:
        svg.append(rect(room["x"], room["y"], room["width"], room["depth"], "white", "#829ab1"))
        svg.append(f'<text x="{50+room["x"]*scale}" y="{100+room["y"]*scale}" font-family="Arial" font-size="13">{room["id"]} / {c["racks_per_hall"]} racks / {c["it_kw"]/c["halls"]:,.0f} kW</text>')
    for rack in racks:
        svg.append(rect(rack["x"], rack["y"], rack["width"], rack["depth"], "#0f766e", "#115e59"))
    svg.extend(['<text x="45" y="777" font-family="Arial" font-size="14" fill="#102a43">A/B power routes, egress, fire compartments and structure require detailed coordination.</text>',
                '<text x="45" y="802" font-family="Arial" font-size="14" fill="#486581">Plant rooms and external yards are defined in the accommodation schedule; not placed in this drawing.</text>', '</svg>'])
    (out/"hall-layout.svg").write_text("\n".join(svg), encoding="utf-8")
    dxf = ["0", "SECTION", "2", "HEADER", "9", "$INSUNITS", "70", "6", "0", "ENDSEC", "0", "SECTION", "2", "ENTITIES"]
    for item in rooms+racks:
        x, y, w, d = item["x"], item["y"], item["width"], item["depth"]
        points = [(x, y), (x+w, y), (x+w, y+d), (x, y+d), (x, y)]
        for a, b in zip(points, points[1:]):
            dxf += ["0", "LINE", "8", "RACKS" if "asset_id" in item else "HALLS",
                    "10", str(a[0]), "20", str(a[1]), "30", "0", "11", str(b[0]), "21", str(b[1]), "31", "0"]
    dxf += ["0", "ENDSEC", "0", "EOF"]
    (out/"hall-layout.dxf").write_text("\n".join(dxf)+"\n", encoding="ascii")
    usd = ['#usda 1.0', '(', '    defaultPrim = "Facility"', '    metersPerUnit = 1', '    upAxis = "Z"', ')', 'def Xform "Facility"', '{']
    for rack in racks:
        name = rack["asset_id"].replace("-", "_")
        usd += [f'    def Cube "{name}"', '    {', '        double size = 1',
                f'        double3 xformOp:translate = ({rack["x"]+rack["width"]/2}, {rack["y"]+rack["depth"]/2}, {rack["height"]/2})',
                f'        double3 xformOp:scale = ({rack["width"]}, {rack["depth"]}, {rack["height"]})',
                '        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:scale"]',
                f'        custom string assetId = "{rack["asset_id"]}"', f'        custom double designKw = {rack["design_kw"]}', '    }']
    usd += ['}']
    (out/"facility-massing.usda").write_text("\n".join(usd)+"\n", encoding="utf-8")
    return racks
