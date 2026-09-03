"""Run bounded design alternatives, preserving the baseline scenario file."""
from pathlib import Path
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from dcf.config import load,validate
from dcf.energy import annual
from dcf.engineering import size
from dcf.finance import model
from dcf.cli import write_csv

def main():
    c=load(ROOT/'configs/tropical-5mw.json')
    cases={
        'Reference':{},
        'Hotter climate +6C':{'weather_mean_c':35,'design_ambient_c':41},
        'Improved COP 5.5':{'cop_at_30c':5.5},
        'Energy recovery 80%':{'energy_recovery_fraction':0.8},
        'Zero residual recovery':{'residual_fraction':0},
        '1 MWp illustrative PV':{'pv_kwp':1000},
        'Air only':{'liquid_fraction':0},
    }
    rows=[]
    for name,changes in cases.items():
        case=validate({**c,**changes});e=annual(case);f=model(case);s=size(case)
        rows.append({'scenario':name,'annual_pue':e['pue'],'facility_kwh':e['facility_kwh'],
                     'grid_kwh':e['grid_kwh'],'npv_usd':f['npv_usd'],'irr':f['irr'],
                     'design_facility_kw':s['design_balance']['facility_kw'],
                     'cdus_per_hall':s['cdus_per_hall_kwth']['installed_units'],
                     'limitation':'Fixed CAPEX except residual treatment; alternative equipment/PV costs not modeled'})
    path=ROOT/'artifacts/scenario-comparison.csv';write_csv(path,rows)
    print(path)

if __name__=='__main__':main()
