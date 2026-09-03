"""Nominal, pre-tax, unlevered facility cash flow; energy tariff is illustrative."""
from __future__ import annotations
import math
from .energy import annual

def npv(rate: float, flows: list[float]) -> float:
    if not math.isfinite(rate) or rate <= -1 or any(not math.isfinite(x) for x in flows):
        raise ValueError("NPV requires a finite rate > -1 and finite cash flows")
    return sum(flow/(1+rate)**year for year, flow in enumerate(flows))

def irr(flows: list[float]) -> float | None:
    """Unique conventional IRR only; unsupported sign patterns return None."""
    if not flows or any(not math.isfinite(x) for x in flows):
        raise ValueError("IRR requires finite cash flows")
    nonzero = [f for f in flows if f != 0]
    changes = sum((a > 0) != (b > 0) for a, b in zip(nonzero, nonzero[1:]))
    if changes != 1 or nonzero[0] >= 0:
        return None
    low, high = -0.99, 1.0
    while npv(high, flows) > 0 and high < 1e6:
        high *= 2
    if npv(low, flows)*npv(high, flows) > 0:
        return None
    for _ in range(180):
        mid = (low+high)/2
        if npv(mid, flows) > 0:
            low = mid
        else:
            high = mid
    return (low+high)/2

def model(c: dict, energy_by_occupancy: dict | None = None) -> dict:
    capex = c["base_capex_usd"]*(1+c["contingency_fraction"])
    cache = {} if energy_by_occupancy is None else energy_by_occupancy
    rows = []
    flows = [-capex]
    gross_costs = [capex]
    cumulative = -capex
    payback = None
    for year, occupancy in enumerate(c["occupancy"], 1):
        if occupancy not in cache:
            cache[occupancy] = annual(c, occupancy)
        energy = cache[occupancy]
        escalation = (1+c["escalation"])**(year-1)
        capacity_revenue = c["it_kw"]*occupancy*c["capacity_usd_kw_month"]*12*escalation
        power_cost = energy["electricity_usd"]*escalation
        recovery = power_cost*c["energy_recovery_fraction"]
        fixed = c["fixed_opex_usd_year"]*escalation
        maintenance = c["base_capex_usd"]*c["maintenance_fraction"]*escalation
        replacement = c["replacement_usd"]*escalation if year == c["replacement_year"] else 0
        residual = c["base_capex_usd"]*c["residual_fraction"]*escalation if year == len(c["occupancy"]) else 0
        net = capacity_revenue + recovery - power_cost - fixed - maintenance - replacement + residual
        flows.append(net)
        gross_costs.append(power_cost+fixed+maintenance+replacement-residual)
        previous = cumulative
        cumulative += net
        if payback is None and cumulative >= 0 and net > 0:
            payback = year-1 + (-previous)/net
        rows.append({"year": year, "occupancy": occupancy, "facility_kwh": energy["facility_kwh"],
                     "grid_kwh": energy["grid_kwh"], "capacity_revenue_usd": capacity_revenue,
                     "energy_recovery_usd": recovery, "electricity_usd": power_cost, "fixed_opex_usd": fixed,
                     "maintenance_usd": maintenance, "replacement_usd": replacement,
                     "residual_usd": residual, "net_cashflow_usd": net, "cumulative_cashflow_usd": cumulative,
                     "discount_factor": 1/(1+c["discount_rate"])**year,
                     "pv_cashflow_usd": net/(1+c["discount_rate"])**year})
    return {"basis": "nominal USD, pre-tax, unlevered, year-0 capital, year-end annual cash flows",
            "capex_usd": capex, "npv_usd": npv(c["discount_rate"], flows), "irr": irr(flows),
            "simple_payback_years": payback, "gross_lifecycle_cost_npv_usd": npv(c["discount_rate"], gross_costs),
            "cashflows_usd": flows, "years": rows}

def sensitivity(c: dict) -> list[dict]:
    cache = {o: annual(c, o) for o in set(c["occupancy"])}
    results = []
    for capex_factor in (0.8, 1.0, 1.2):
        for capacity_price_factor in (0.8, 1.0, 1.2):
            case = {**c, "base_capex_usd": c["base_capex_usd"]*capex_factor,
                    "capacity_usd_kw_month": c["capacity_usd_kw_month"]*capacity_price_factor}
            result = model(case, cache)
            results.append({"capex_factor": capex_factor, "capacity_price_factor": capacity_price_factor,
                            "npv_usd": result["npv_usd"], "irr": result["irr"]})
    return results
