"""Transparent weighted screening; eligibility gates precede scoring."""
from __future__ import annotations
import csv
import math
from pathlib import Path

WEIGHTS = {"grid": 0.35, "hazards": 0.25, "water": 0.15, "fiber": 0.15, "access": 0.10}

def rank(path: str | Path, weights: dict | None = None) -> list[dict]:
    weights = WEIGHTS if weights is None else weights
    if set(weights) != set(WEIGHTS) or any(not math.isfinite(v) or v < 0 for v in weights.values()) or not math.isclose(sum(weights.values()), 1):
        raise ValueError("Nonnegative weights for all criteria must sum to 1")
    results = []
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            scores = {k: float(row[k]) for k in weights}
            if any(not math.isfinite(v) or not 1 <= v <= 5 for v in scores.values()):
                raise ValueError("Site scores must be finite in [1,5]")
            if row["grid_gate"] not in ("pass", "fail") or row["hazard_gate"] not in ("pass", "fail"):
                raise ValueError("Site gates must be pass/fail")
            eligible = row["grid_gate"] == "pass" and row["hazard_gate"] == "pass"
            results.append({"site": row["site"], "eligible": eligible,
                            "score_100": sum(scores[k]*weights[k] for k in weights)*20,
                            "evidence": row["evidence"], "grid_gate": row["grid_gate"], "hazard_gate": row["hazard_gate"]})
    return sorted(results, key=lambda r: (not r["eligible"], -r["score_100"], r["site"]))
