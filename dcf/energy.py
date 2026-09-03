"""Synthetic non-leap 8760-hour year. No weather file or measured load is implied."""
from __future__ import annotations
from datetime import datetime, timedelta
import math
from .engineering import power_balance

def hourly(c: dict, occupancy: float = 1):
    if not 0 <= occupancy <= 1:
        raise ValueError("occupancy must be in [0,1]")
    origin = datetime(2025, 1, 1)
    for h in range(8760):
        time = origin + timedelta(hours=h)
        daily = math.sin(2*math.pi*(time.hour-9)/24)
        seasonal = math.sin(2*math.pi*(h/24-80)/365)
        ambient = c["weather_mean_c"] + c["weather_daily_amplitude_c"]*daily + c["weather_seasonal_amplitude_c"]*seasonal
        draw = c["mean_draw_fraction"] + c["draw_amplitude"]*math.sin(2*math.pi*(time.hour-8)/24)
        balance = power_balance(c, c["it_kw"]*occupancy*draw, ambient)
        solar = max(0, math.sin(math.pi*(time.hour-6)/12)) if 6 <= time.hour <= 18 else 0
        pv = c["pv_kwp"]*c["pv_performance_ratio"]*solar
        used = min(pv, balance["facility_kw"])
        yield {"timestamp_local": time.isoformat(), "month": time.month, "ambient_c": ambient,
               **balance, "pv_potential_kw": pv, "pv_used_kw": used,
               "pv_curtailed_kw": pv-used, "grid_kw": balance["facility_kw"]-used}

def annual(c: dict, occupancy: float = 1, rows=None) -> dict:
    rows = list(hourly(c, occupancy)) if rows is None else rows
    if len(rows) != 8760:
        raise ValueError("Annual energy requires exactly 8760 hourly samples")
    monthly = []
    for month in range(1, 13):
        group = [r for r in rows if r["month"] == month]
        if not group:
            raise ValueError("Missing calendar month")
        it = sum(r["it_kw"] for r in group)
        facility = sum(r["facility_kw"] for r in group)
        grid = sum(r["grid_kw"] for r in group)
        peak = max(r["grid_kw"] for r in group)
        monthly.append({"month": month, "hours": len(group), "it_kwh": it,
                        "facility_kwh": facility, "grid_kwh": grid, "grid_peak_kw": peak,
                        "electricity_usd": grid*c["electricity_usd_per_kwh"] + peak*c["demand_usd_per_kw_month"],
                        "pue": facility/it if it else None})
    it = sum(r["it_kwh"] for r in monthly)
    facility = sum(r["facility_kwh"] for r in monthly)
    grid = sum(r["grid_kwh"] for r in monthly)
    return {"occupancy": occupancy, "hours": 8760, "it_kwh": it, "facility_kwh": facility,
            "grid_kwh": grid, "pv_used_kwh": sum(r["pv_used_kw"] for r in rows),
            "pv_curtailed_kwh": sum(r["pv_curtailed_kw"] for r in rows),
            "pue": facility/it if it else None, "electricity_usd": sum(r["electricity_usd"] for r in monthly),
            "operational_grid_tco2e": grid*c["grid_kgco2e_per_kwh"]/1000,
            "direct_site_water_m3": it*c["site_water_l_per_it_kwh"]/1000,
            "direct_wue_l_kwh": c["site_water_l_per_it_kwh"] if it else None, "monthly": monthly}
