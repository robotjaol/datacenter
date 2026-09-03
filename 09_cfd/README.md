# CFD validation specification

This release includes a **bulk heat-balance airflow calculation**, not a CFD solver or CFD result. The airflow figure gives a first-order total supply requirement; it cannot predict rack inlet hot spots or recirculation. No simulated temperature heatmap is presented as evidence.

Before a CFD study, obtain room/containment geometry, perforation/leakage areas, rack heat and flow curves, terminal fan curves, buoyancy settings, wall/envelope conditions and reference sensor locations. Use the asset IDs from the rack schedule for all boundary-condition mappings.

Run baseline/full load, partial occupancy, terminal loss, containment-door opening and restart scenarios. Compare at least three mesh resolutions; report cells, quality, residual histories, mass/energy imbalance and sensitivity of the decision metrics. Convergence tolerances must be selected and justified for the solver and decision, rather than borrowed without context.

Acceptance evidence must include solver/version, mesh/configuration hashes, boundary assumptions, residual plots, rack inlet distributions, conservation checks and comparison against independent measurements or a validated benchmark. Keep numerical verification separate from physical validation. NVIDIA DSX is an optional interoperability reference; no DSX CFD run is claimed.
