# Energy and metering

`dcf.energy` produces an auditable hour-by-hour table and monthly rollup. Gross facility energy includes IT, power-conversion/distribution losses, fans, chillers, pumps and other loads. The annual reference is fully leased; occupancy-specific finance energy is recomputed separately.

Meter plan: utility import/export, PV production, each A/B intake, UPS input/output, cooling feeders, major auxiliaries and IT final distribution. Sum both rack feeds once for each rack; align timestamps and meter boundaries. Reconcile parent meters against children, investigate gaps, and keep calibration records.

Never average hourly PUE values to claim annual PUE. Aggregate energy first. Track missing samples and interval duration; this release requires exactly 8,760 hourly samples and uses a synthetic non-leap year. A production meter adapter must reject duplicate timestamps, reconcile daylight-saving behavior and report completeness.

PV defaults to zero. The optional sinusoidal solar input has no shading, irradiance or weather evidence and clips generation to demand. BESS sizing is a separate energy screen with efficiency, usable fraction and end-of-life allowance; dispatch, recharge, tariff arbitrage, cycle degradation and fire siting are not implemented. Replacing either with a physical design needs data and validation.
