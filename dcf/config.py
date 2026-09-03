"""Strict configuration validation with explicit units; no third-party runtime."""
from __future__ import annotations
import json
import math
from pathlib import Path

# Bounds are model-domain limits, not code or equipment compliance limits.
BOUNDS = {
    "it_kw": (1, 1_000_000), "halls": (1, 100), "racks_per_hall": (1, 1000),
    "rack_kw": (0.1, 1000), "design_ambient_c": (-30, 60),
    "ups_efficiency": (0.5, 1), "distribution_efficiency": (0.5, 1),
    "transformer_efficiency": (0.5, 1), "power_factor": (0.5, 1),
    "design_margin": (0, 1), "ups_module_kw": (1, 100000),
    "transformer_unit_kva": (1, 100000), "generator_unit_kw": (1, 100000),
    "generator_derating": (0.1, 1), "battery_minutes": (1, 240),
    "battery_inverter_efficiency": (0.1, 1), "battery_usable_fraction": (0.1, 1),
    "battery_end_of_life_fraction": (0.1, 1), "liquid_fraction": (0, 1),
    "cop_at_30c": (1, 20), "cop_degradation_per_c": (0, 1), "minimum_cop": (1, 10),
    "chiller_unit_kwth": (1, 100000), "cdu_unit_kwth": (1, 100000), "fan_fraction": (0, 0.5),
    "pump_fraction": (0, 0.5), "envelope_kw": (0, 100000),
    "other_facility_kw": (0, 100000), "water_delta_t_k": (0.5, 30),
    "air_delta_t_k": (0.5, 50), "mean_draw_fraction": (0, 1),
    "draw_amplitude": (0, 0.5), "weather_mean_c": (-30, 60),
    "weather_daily_amplitude_c": (0, 30), "weather_seasonal_amplitude_c": (0, 30),
    "electricity_usd_per_kwh": (0, 10), "demand_usd_per_kw_month": (0, 1000),
    "grid_kgco2e_per_kwh": (0, 3), "site_water_l_per_it_kwh": (0, 10),
    "pv_kwp": (0, 1_000_000), "pv_performance_ratio": (0, 1),
    "bess_supported_kw": (0, 1_000_000), "bess_hours": (0, 100),
    "bess_discharge_efficiency": (0.1, 1), "bess_usable_fraction": (0.1, 1),
    "bess_end_of_life_fraction": (0.1, 1), "base_capex_usd": (1, 1e12),
    "contingency_fraction": (0, 1), "fixed_opex_usd_year": (0, 1e12),
    "maintenance_fraction": (0, 1), "capacity_usd_kw_month": (0, 10000),
    "energy_recovery_fraction": (0, 1), "discount_rate": (0, 1),
    "escalation": (-0.1, 0.5), "replacement_year": (1, 50),
    "replacement_usd": (0, 1e12), "residual_fraction": (0, 1),
    "path_unavailability": (0, 1), "common_cause_unavailability": (0, 1),
    "reliability_samples": (100, 1_000_000), "seed": (0, 2147483647),
}
INTEGERS = {"halls", "racks_per_hall", "replacement_year", "reliability_samples", "seed"}

def validate(c: dict) -> dict:
    expected = set(BOUNDS) | {"name", "schema_version", "occupancy"}
    if not isinstance(c, dict) or set(c) != expected:
        actual = set(c) if isinstance(c, dict) else set()
        raise ValueError(f"Configuration fields: missing={sorted(expected-actual)}, unknown={sorted(actual-expected)}")
    if not isinstance(c["name"], str) or not c["name"].strip():
        raise ValueError("name must be nonempty text")
    if type(c["schema_version"]) is not int or c["schema_version"] != 1:
        raise ValueError("schema_version must be integer 1")
    for key, (low, high) in BOUNDS.items():
        value = c[key]
        if type(value) not in (int, float) or not math.isfinite(value) or not low <= value <= high:
            raise ValueError(f"{key} must be finite in [{low}, {high}]")
        if key in INTEGERS and type(value) is not int:
            raise ValueError(f"{key} must be an integer")
    occ = c["occupancy"]
    if not isinstance(occ, list) or not 1 <= len(occ) <= 50:
        raise ValueError("occupancy must contain 1-50 annual fractions")
    if any(type(v) not in (int, float) or not math.isfinite(v) or not 0 <= v <= 1 for v in occ):
        raise ValueError("occupancy fractions must be finite in [0,1]")
    if c["replacement_year"] > len(occ):
        raise ValueError("replacement_year must lie within the study period")
    rack_total = c["halls"] * c["racks_per_hall"] * c["rack_kw"]
    if not math.isclose(c["it_kw"], rack_total, rel_tol=1e-9):
        raise ValueError("it_kw must equal halls * racks_per_hall * rack_kw")
    if not 0 <= c["mean_draw_fraction"] - c["draw_amplitude"] <= c["mean_draw_fraction"] + c["draw_amplitude"] <= 1:
        raise ValueError("draw profile must remain within [0,1]")
    if c["minimum_cop"] > c["cop_at_30c"]:
        raise ValueError("minimum_cop cannot exceed cop_at_30c")
    return c

def load(path: str | Path) -> dict:
    return validate(json.loads(Path(path).read_text(encoding="utf-8-sig")))

def schema() -> dict:
    properties = {k: {"type": "integer" if k in INTEGERS else "number", "minimum": a, "maximum": b}
                  for k, (a, b) in BOUNDS.items()}
    properties.update(name={"type": "string", "minLength": 1}, schema_version={"const": 1},
                      occupancy={"type": "array", "minItems": 1, "maxItems": 50,
                                 "items": {"type": "number", "minimum": 0, "maximum": 1}})
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": "Facility scenario v1",
            "description": "Cross-field constraints are additionally enforced by dcf.config.validate.",
            "type": "object", "additionalProperties": False, "required": list(properties), "properties": properties}
