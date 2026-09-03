"""Steady-state screening equations: kW, kVA, kWh, kWth, kg/s, m3/s."""
from __future__ import annotations
import math

def power_balance(c: dict, it_kw: float, ambient_c: float) -> dict:
    if it_kw < 0 or not math.isfinite(it_kw) or not math.isfinite(ambient_c):
        raise ValueError("Power must be nonnegative and inputs finite")
    distribution_loss = it_kw / c["distribution_efficiency"] - it_kw
    ups_loss = (it_kw + distribution_loss) / c["ups_efficiency"] - it_kw - distribution_loss
    fan = it_kw * (1-c["liquid_fraction"]) * c["fan_fraction"]
    heat = it_kw + distribution_loss + ups_loss + fan + c["envelope_kw"]
    cop = max(c["minimum_cop"], c["cop_at_30c"] - c["cop_degradation_per_c"] * (ambient_c-30))
    compressor = heat / cop
    pump = heat * c["pump_fraction"]
    downstream = it_kw + distribution_loss + ups_loss + fan + compressor + pump + c["other_facility_kw"]
    transformer_loss = downstream / c["transformer_efficiency"] - downstream
    total = downstream + transformer_loss
    return {"it_kw": it_kw, "distribution_loss_kw": distribution_loss, "ups_loss_kw": ups_loss,
            "fan_kw": fan, "cooling_kwth": heat, "cop": cop, "compressor_kw": compressor,
            "pump_kw": pump, "other_kw": c["other_facility_kw"], "transformer_loss_kw": transformer_loss,
            "facility_kw": total, "instantaneous_power_ratio": total/it_kw if it_kw else None}

def n_plus_one(required: float, unit: float, derating: float = 1) -> dict:
    if required < 0 or unit <= 0 or not 0 < derating <= 1:
        raise ValueError("Invalid equipment sizing inputs")
    duty = math.ceil(required/(unit*derating))
    return {"required": required, "unit_rating": unit, "derating": derating,
            "duty_units": duty, "installed_units": duty+1 if required else 0,
            "remaining_capacity_after_one_loss": duty*unit*derating,
            "spare_units": 1 if required else 0}

def size(c: dict) -> dict:
    design = power_balance(c, c["it_kw"], c["design_ambient_c"])
    margin = 1+c["design_margin"]
    ups_output = c["it_kw"]/c["distribution_efficiency"]
    return {"design_balance": design, "paths": 2,
            "ups_per_path_kw": n_plus_one(ups_output*margin, c["ups_module_kw"]),
            "transformers_per_path_kva": n_plus_one(design["facility_kw"]*margin/c["power_factor"], c["transformer_unit_kva"]),
            "generators_per_path_kw": n_plus_one(design["facility_kw"]*margin, c["generator_unit_kw"], c["generator_derating"]),
            "chillers_shared_kwth": n_plus_one(design["cooling_kwth"]*margin, c["chiller_unit_kwth"]),
            "cdus_per_hall_kwth": n_plus_one(c["it_kw"]*c["liquid_fraction"]*margin/c["halls"], c["cdu_unit_kwth"]),
            "battery_per_path_kwh": ups_output*c["battery_minutes"]/60 /
                (c["battery_inverter_efficiency"]*c["battery_usable_fraction"]*c["battery_end_of_life_fraction"]),
            "chw_mass_flow_kg_s": design["cooling_kwth"]/(4.186*c["water_delta_t_k"]),
            "liquid_it_kwth": c["it_kw"]*c["liquid_fraction"],
            "liquid_mass_flow_kg_s": c["it_kw"]*c["liquid_fraction"]/(4.186*c["water_delta_t_k"]),
            "air_it_kwth": c["it_kw"]*(1-c["liquid_fraction"]),
            "air_volume_flow_m3_s": (c["it_kw"]*(1-c["liquid_fraction"])+design["fan_kw"])/(1.2*1.006*c["air_delta_t_k"]),
            "bess_nameplate_kwh": c["bess_supported_kw"]*c["bess_hours"]/
                (c["bess_discharge_efficiency"]*c["bess_usable_fraction"]*c["bess_end_of_life_fraction"])}
