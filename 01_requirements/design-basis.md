# Basis of design — revision 0.1

**Reference configuration:** `configs/tropical-5mw.json`. Units are SI with nominal USD economics. Capacity: four × 1.25 MW halls, 50 racks/hall, 25 kW/rack design allowance. The default energy run assumes fully leased space drawing 75% on average, with a ±10 percentage point daily variation. Finance uses an independent 35–95% occupancy ramp.

**Electrical:** nominal conceptual MV intake, dual A/B distribution, each with transformers, generation, UPS and final rack distribution. The example diagram uses 20 kV/400 V solely as an illustrative interface; actual utility voltage, transformer impedance and equipment fault ratings are unresolved. Critical rack loads are dual cord. Single-cord conversion is outside the reference allowance.

**Cooling:** air-cooled chilled-water plant; 70% of IT heat removed by air terminals and 30% through liquid CDUs. Reference design ambient 35 C; 6 K water and 12 K air rises. Temperatures are model assumptions, not certified design extremes or universal equipment limits. FWS and TCS remain distinct interfaces.

**Financial:** all-at-once year-zero capital, 15-year operation, 10% nominal discount, 2% annual escalation; rates are synthetic. The 48 million USD base allowance has 20% contingency. Customer energy recovery is 100% in the base case; change it explicitly to model risk.

**Environmental:** synthetic dry-bulb profile, constant grid factor, direct water factor and no PV in baseline. Humidity, seasonal extremes and site hazards require sourced data. ASHRAE 2021 guidance is a historical reference; confirm current Datacom guidance and supplier envelopes.

The assumptions register enumerates every scalar and annual occupancy input, its units, origin and validation owner. Approval state for all inputs is `illustrative/unapproved`.
