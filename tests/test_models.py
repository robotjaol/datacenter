import copy
import json
import math
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
from dcf.config import load, validate
from dcf.engineering import power_balance, size, n_plus_one
from dcf.energy import annual, hourly
from dcf.finance import npv, irr, model
from dcf.controls import commission, assess, Observation
from dcf.geometry import layout, write_geometry
from dcf.reliability import evaluate
from dcf.site import rank

ROOT = Path(__file__).resolve().parents[1]

class Models(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = load(ROOT/"configs/tropical-5mw.json")
        cls.rows = list(hourly(cls.c))

    def test_reject_nonfinite_boolean_unknown_and_missing(self):
        for key, value in [("it_kw", float("nan")), ("power_factor", 0), ("halls", True), ("occupancy", [1, -1])]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate({**self.c, key: value})
        with self.assertRaises(ValueError):
            validate({**self.c, "pue": 1.2})
        c = self.c.copy()
        del c["it_kw"]
        with self.assertRaises(ValueError):
            validate(c)

    def test_capacity_and_profile_consistency(self):
        for change in ({"rack_kw": 26}, {"mean_draw_fraction": 0.95}, {"replacement_year": 50}):
            with self.assertRaises(ValueError):
                validate({**self.c, **change})

    def test_electrical_balance_conserves_power(self):
        for load in (0, 1250, 5000):
            b = power_balance(self.c, load, 35)
            summed = sum(b[k] for k in ("it_kw", "distribution_loss_kw", "ups_loss_kw", "fan_kw", "compressor_kw", "pump_kw", "other_kw", "transformer_loss_kw"))
            self.assertAlmostEqual(summed, b["facility_kw"], places=8)
        self.assertEqual(power_balance(self.c, 0, 35)["instantaneous_power_ratio"], None)

    def test_n_plus_one_and_per_path_boundaries(self):
        self.assertEqual(n_plus_one(0, 1250)["installed_units"], 0)
        self.assertEqual(size({**self.c, "liquid_fraction": 0})["cdus_per_hall_kwth"]["installed_units"], 0)
        self.assertEqual(n_plus_one(2500, 1250)["installed_units"], 3)
        self.assertEqual(n_plus_one(2500.01, 1250)["installed_units"], 4)
        for key, group in size(self.c).items():
            if isinstance(group, dict) and "required" in group:
                self.assertGreaterEqual(group["remaining_capacity_after_one_loss"], group["required"])
                self.assertLess((group["duty_units"]-1)*group["unit_rating"]*group["derating"], group["required"])

    def test_heat_split_and_water_units(self):
        s = size(self.c)
        self.assertAlmostEqual(s["air_it_kwth"]+s["liquid_it_kwth"], self.c["it_kw"])
        self.assertAlmostEqual(s["chw_mass_flow_kg_s"]*4.186*self.c["water_delta_t_k"], s["design_balance"]["cooling_kwth"])

    def test_8760_energy_weighted_pue_and_calendar(self):
        a = annual(self.c, rows=self.rows)
        self.assertEqual(len(self.rows), 8760)
        self.assertEqual(a["monthly"][1]["hours"], 672)
        self.assertEqual(sum(m["hours"] for m in a["monthly"]), 8760)
        self.assertAlmostEqual(a["it_kwh"], 5000*0.75*8760, places=5)
        self.assertAlmostEqual(a["pue"], a["facility_kwh"]/a["it_kwh"])
        self.assertAlmostEqual(a["electricity_usd"], a["grid_kwh"]*0.1 + sum(m["grid_peak_kw"] for m in a["monthly"])*5, places=5)

    def test_zero_it_and_pv_boundaries(self):
        c = {**self.c, "pv_kwp": 1_000_000}
        a = annual(c, 0)
        self.assertIsNone(a["pue"])
        self.assertGreater(a["facility_kwh"], 0)
        self.assertGreater(a["pv_curtailed_kwh"], 0)
        self.assertGreaterEqual(a["grid_kwh"], 0)
        self.assertAlmostEqual(a["grid_kwh"]+a["pv_used_kwh"], a["facility_kwh"], places=5)

    def test_weather_penalty_and_occupancy(self):
        self.assertGreater(power_balance(self.c, 5000, 40)["facility_kw"], power_balance(self.c, 5000, 30)["facility_kw"])
        self.assertGreater(annual(self.c, 1)["facility_kwh"], annual(self.c, 0.5)["facility_kwh"])

    def test_finance_known_examples_and_sign_patterns(self):
        self.assertAlmostEqual(npv(0.1, [-100, 110]), 0)
        self.assertAlmostEqual(irr([-100, 110]), 0.1)
        self.assertAlmostEqual(irr([-100, 80]), -0.2)
        self.assertIsNone(irr([-100, -1]))
        self.assertIsNone(irr([-100, 230, -132]))
        self.assertIsNone(irr([0, 1, 2]))
        with self.assertRaises(ValueError):
            npv(-1, [-100, 110])

    def test_financial_recovery_cashflow_and_terminal(self):
        f = model(self.c)
        self.assertEqual(f["capex_usd"], 57_600_000)
        self.assertAlmostEqual(f["npv_usd"], sum(y["pv_cashflow_usd"] for y in f["years"])-f["capex_usd"])
        for year in f["years"]:
            self.assertEqual(year["electricity_usd"], year["energy_recovery_usd"])
            expected = year["capacity_revenue_usd"]-year["fixed_opex_usd"]-year["maintenance_usd"]-year["replacement_usd"]+year["residual_usd"]
            self.assertAlmostEqual(year["net_cashflow_usd"], expected)
        self.assertGreater(f["years"][7]["replacement_usd"], 0)
        self.assertTrue(all(y["residual_usd"] == 0 for y in f["years"][:-1]))
        self.assertAlmostEqual(npv(f["irr"], f["cashflows_usd"]), 0, places=5)

    def test_control_failures_and_no_writes(self):
        self.assertTrue(all(r["passed"] for r in commission()))
        self.assertEqual(assess(Observation(telemetry_fresh=False, generator_ready=True))["observed_source"], "UNKNOWN")
        self.assertFalse(assess(Observation())["writes_enabled"])

    def test_availability_common_cause_and_seed(self):
        a = evaluate(0.1, 0.02, 100000, 42)
        self.assertAlmostEqual(a["exact_availability"], 0.9702)
        self.assertEqual(a, evaluate(0.1, 0.02, 100000, 42))
        self.assertLess(abs(a["sample_availability"]-a["exact_availability"]), 0.003)
        self.assertEqual(evaluate(0, 0, 100, 1)["exact_availability"], 1)
        self.assertEqual(evaluate(0, 1, 100, 1)["exact_availability"], 0)

    def test_geometry_identity_and_bounds(self):
        rooms, racks = layout(self.c)
        self.assertEqual(len(racks), 200)
        self.assertEqual(len({r["asset_id"] for r in racks}), 200)
        for r in racks:
            room = next(x for x in rooms if x["id"] == r["hall_id"])
            self.assertGreaterEqual(r["x"], room["x"])
            self.assertGreaterEqual(r["y"], room["y"])
            self.assertLessEqual(r["x"]+r["width"], room["x"]+room["width"])
            self.assertLessEqual(r["y"]+r["depth"], room["y"]+room["depth"])
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            write_geometry(self.c, out)
            ET.parse(out/"hall-layout.svg")
            self.assertEqual((out/"facility-massing.usda").read_text().count('def Cube'), 200)
            self.assertTrue((out/"hall-layout.dxf").read_text().endswith("EOF\n"))

    def test_site_gates_override_high_score(self):
        sites = rank(ROOT/"data/site-candidates.csv")
        self.assertEqual(sites[-1]["site"], "Site Beta")
        self.assertFalse(sites[-1]["eligible"])
        self.assertTrue(sites[0]["eligible"])

if __name__ == "__main__":
    unittest.main()
