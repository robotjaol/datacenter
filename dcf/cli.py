"""Command line orchestration with deterministic outputs and source hashes."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys
from . import __version__
from .config import load, schema
from .engineering import size
from .energy import annual, hourly
from .finance import model, sensitivity
from .reliability import evaluate
from .controls import commission
from .geometry import write_geometry
from .site import rank

def write_json(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2, allow_nan=False)+"\n", encoding="utf-8")

def write_csv(path: Path, rows: list[dict]):
    if not rows:
        raise ValueError("CSV rows cannot be empty")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def run(config_path: Path, out: Path, site_path: Path) -> dict:
    c = load(config_path)
    # Validate external inputs before creating deliverables.
    sites = rank(site_path)
    sizing = size(c)
    rows = list(hourly(c))
    energy = annual(c, rows=rows)
    finance = model(c)
    reliability = evaluate(c["path_unavailability"], c["common_cause_unavailability"], c["reliability_samples"], c["seed"])
    tests = commission()
    report = {"model_version": __version__, "scenario": c["name"],
              "status": "concept study; synthetic inputs; not certified or construction-ready",
              "config_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(),
              "sizing": sizing, "energy": energy, "finance": finance, "reliability": reliability,
              "commissioning": tests, "sites": sites}
    out.mkdir(parents=True, exist_ok=True)
    write_json(out/"report.json", report)
    write_json(out/"scenario.json", c)
    write_json(out/"commissioning-results.json", tests)
    write_csv(out/"hourly-energy.csv", rows)
    write_csv(out/"monthly-energy.csv", energy["monthly"])
    write_csv(out/"cashflows.csv", finance["years"])
    write_csv(out/"sensitivity.csv", sensitivity(c))
    write_csv(out/"site-ranking.csv", sites)
    racks = write_geometry(c, out)
    write_csv(out/"rack-assets.csv", racks)
    groups = [("UPS", "ups_per_path_kw", "kW", ["A", "B"]),
              ("TX", "transformers_per_path_kva", "kVA", ["A", "B"]),
              ("GEN", "generators_per_path_kw", "kW", ["A", "B"]),
              ("CHL", "chillers_shared_kwth", "kWth", ["SHARED"]),
              ("CDU", "cdus_per_hall_kwth", "kWth", [f"H{h+1:02}" for h in range(c["halls"])])]
    equipment = []
    for kind, key, unit, paths in groups:
        for path in paths:
            for n in range(sizing[key]["installed_units"]):
                equipment.append({"asset_id": f"{kind}-{path}-{n+1:02}", "system": kind, "path": path,
                                  "nameplate": sizing[key]["unit_rating"], "unit": unit,
                                  "derating": sizing[key]["derating"], "status": "concept allowance"})
    write_csv(out/"equipment-schedule.csv", equipment)
    telemetry = [{"timestamp": "2025-01-01T00:00:00+07:00", "asset_id": r["asset_id"],
                  "metric": "active_power_kw", "value": c["rack_kw"]*c["mean_draw_fraction"],
                  "unit": "kW", "quality": "synthetic", "source": "offline-example"} for r in racks]
    write_json(out/"telemetry-sample.json", telemetry)
    # Hash generated evidence (not the manifest itself); no nondeterministic timestamps.
    names = ["report.json", "scenario.json", "commissioning-results.json", "hourly-energy.csv", "monthly-energy.csv",
             "cashflows.csv", "sensitivity.csv", "site-ranking.csv", "rack-assets.csv", "hall-layout.svg",
             "hall-layout.dxf", "facility-massing.usda", "equipment-schedule.csv", "telemetry-sample.json"]
    manifest = {name: hashlib.sha256((out/name).read_bytes()).hexdigest() for name in names}
    write_json(out/"manifest.json", manifest)
    return report

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Open Data Center Facility concept toolkit")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "run"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--config", type=Path, default=Path("configs/tropical-5mw.json"))
        if name == "run":
            cmd.add_argument("--output", type=Path, default=Path("build/reference"))
            cmd.add_argument("--sites", type=Path, default=Path("data/site-candidates.csv"))
    sub.add_parser("schema")
    args = parser.parse_args(argv)
    try:
        if args.command == "schema":
            print(json.dumps(schema(), indent=2))
        elif args.command == "validate":
            c = load(args.config)
            print(f"VALID: {c['name']} ({c['it_kw']:,.0f} kW design IT)")
        else:
            report = run(args.config, args.output, args.sites)
            print(f"Created {args.output.resolve()}")
            pue = report["energy"]["pue"]
            print(f"Annual PUE: {pue:.3f}" if pue is not None else "Annual PUE: undefined (zero IT energy)")
            print(f"Concept CAPEX: USD {report['finance']['capex_usd']:,.0f}")
            print(f"Pre-tax unlevered NPV: USD {report['finance']['npv_usd']:,.0f}")
        return 0
    except (ValueError, KeyError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
