"""Offline supervisory-state example. No commands or connections to equipment."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Observation:
    utility_ok: bool = True
    generator_ready: bool = False
    battery_available: bool = True
    telemetry_fresh: bool = True
    leak: bool = False
    supply_temp_c: float = 24

def assess(x: Observation) -> dict:
    alarms = []
    if not x.telemetry_fresh:
        alarms.append("TELEMETRY_STALE")
    if x.leak:
        alarms.append("LIQUID_LEAK")
    if x.supply_temp_c >= 30:
        alarms.append("HIGH_INLET_TEMPERATURE")
    if not x.utility_ok:
        alarms.append("UTILITY_LOST")
    if not x.telemetry_fresh:
        source = "UNKNOWN"
    elif x.utility_ok:
        source = "UTILITY"
    elif x.generator_ready:
        source = "GENERATOR"
    elif x.battery_available:
        source = "BATTERY"
    else:
        source = "UNSERVED"
    return {"observed_source": source, "alarms": alarms,
            "operator_review_required": bool(alarms), "writes_enabled": False}

CASES = [
    ("IST-001", {}, "UTILITY", []),
    ("IST-002", {"utility_ok": False}, "BATTERY", ["UTILITY_LOST"]),
    ("IST-003", {"utility_ok": False, "generator_ready": True}, "GENERATOR", ["UTILITY_LOST"]),
    ("IST-004", {"utility_ok": False, "battery_available": False}, "UNSERVED", ["UTILITY_LOST"]),
    ("IST-005", {"telemetry_fresh": False}, "UNKNOWN", ["TELEMETRY_STALE"]),
    ("IST-006", {"leak": True, "supply_temp_c": 31}, "UTILITY", ["LIQUID_LEAK", "HIGH_INLET_TEMPERATURE"]),
]

def commission() -> list[dict]:
    results = []
    for identifier, inputs, source, alarms in CASES:
        actual = assess(Observation(**inputs))
        results.append({"id": identifier, "inputs": inputs, "actual": actual,
                        "expected_source": source, "expected_alarms": alarms,
                        "passed": actual["observed_source"] == source and actual["alarms"] == alarms and not actual["writes_enabled"],
                        "evidence_level": "offline software scenario; not physical IST"})
    return results
