# Model methodology and units

## Capacity and electrical balance

Design IT = halls × racks per hall × rack kW. It is installed design demand, not annual average power or leased capacity. Distribution input = IT/eta_distribution. UPS loss = distribution input × (1/eta_UPS - 1). Both electrical losses are included in the conditioned heat allowance. Each path's UPS sizing uses full IT plus downstream loss and design margin; do not double the IT demand when summing A/B installed equipment.

N duty units = ceil(required / (unit rating × derating)); installed = N+1. Surviving capacity is checked against the required value. Transformer requirement is design facility kW × margin / power factor. Generator requirement is facility kW × margin, with an explicit derating factor. This is steady-state capacity arithmetic; it omits starting kVA, nonlinear loads, fault duty, harmonics and dynamic transfer behavior.

Battery nameplate kWh/path = UPS output kW × minutes/60 / (inverter efficiency × usable fraction × end-of-life fraction). Runtime is an energy screen; manufacturer discharge curves, DC voltage, protection, temperature and battery-string failures remain unmodeled.

## Thermal and energy boundary

Fan kW = air-cooled IT kW × fan fraction. Chilled load Q = IT + distribution loss + UPS loss + fan heat + fixed envelope heat. Compressor kW = Q/COP; pump kW = Q × pump fraction. Pump heat is assumed rejected outside the modeled conditioned boundary. Other facility kW and transformer losses are outside that thermal boundary. An engineer must refine heat locations before equipment selection.

COP = max(minimum COP, COP_at_30C - slope × (ambient-30)). This original screening curve is not a manufacturer map. No humidity/latent load, economizer, psychrometrics, pressure-loss or transient storage model is included. Liquid share changes IT heat routing and fan allowance; both loops use the same plant COP in this release.

Water flow kg/s = Q_kW / (4.186 kJ/kg-K × deltaT_K). Airflow m3/s = air-side heat_kW / (1.2 kg/m3 × 1.006 kJ/kg-K × deltaT_K). Airflow covers air-cooled IT plus terminal-fan heat; UPS-room and envelope ventilation require separate distribution design.

Hourly draw uses a daily sinusoid around the specified mean, multiplied by leased occupancy. Weather is a daily plus seasonal sinusoid. The calendar is synthetic 2025, non-leap, fixed local standard time; 1 kW for one sample equals 1 kWh. Monthly demand charges use each month's peak grid kW. The profile is illustrative and does not imply measured 2025 weather.

Annual PUE = sum(gross facility kWh)/sum(IT kWh). It is undefined at zero IT energy. PV reduces imports after gross facility demand, with curtailment and no export revenue. The BESS output is an independent energy allowance; there is no dispatch or battery-loss deduction in the annual baseline. Direct-site WUE and grid carbon are simple factor models, not full lifecycle accounting. See [DOE metric definitions](https://www.energy.gov/cmei/femp/cooling-water-efficiency-opportunities-federal-data-centers).

## Finance and reliability

Initial capital occurs at year zero. All subsequent cash flows occur at year end. Capacity rent uses contracted kW; energy depends separately on occupied demand and draw fraction. Energy reimbursement is separately added to revenue and the full power bill remains an expense. This avoids hiding energy costs or charging them twice. Fixed OPEX and maintenance continue at low occupancy.

NPV = sum(CF_t/(1+r)^t), including CF_0. Gross lifecycle cost discounts capital, energy, maintenance, replacements and residual disposal proceeds before revenues or reimbursement. IRR is returned only for one conventional negative-to-positive sign change and a bracketed root; otherwise null. This release omits taxes, debt, depreciation, working capital, construction-period financing and market terminal capitalization. Residual value is an explicit asset-value assumption. The economic conventions are inspired by [NIST HB 135e2025](https://nvlpubs.nist.gov/nistpubs/hb/2025/NIST.HB.135e2025.pdf), not US mandated rates.

Availability = (1-q_common) × (1-q_path²). Two paths are independent conditional on a separately modeled common event. Monte Carlo samples steady-state Bernoulli states and reports a Wilson interval. It does not simulate time-to-failure, repairs, human-error sequence or outage durations. No Tier or SLA is inferred from the result.
