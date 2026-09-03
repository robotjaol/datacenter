# Optional simulation integrations

These are interface specifications and review steps, not executed adapters. The portable core does not import external solvers, vendor assets or ML frameworks.

| Integration | Transfer from this project | Expected external evidence |
|---|---|---|
| NVIDIA DSX / OpenUSD | Rack IDs, original USD massing, design kW and geometry units | Validated asset mapping, scene/version, solver configuration and results |
| MathWorks Simscape | Rack load, path capacity, efficiencies and disturbance cases | Time-domain voltage/power/thermal traces and conservation comparison |
| HPE SustainDC | External IT profile, weather/carbon inputs, cooling/storage assumptions | Calibration, component boundaries and controlled baseline comparison |

Before importing: pin the upstream commit/version, review current license/dependencies, use a separate environment, check data/asset terms and record hashes. Match gross/net energy definitions and unit conversions; compare a common simple operating point before more complex scenarios.

Do not claim output parity until a reproducible comparison is recorded. Follow [source access and license notes](../research/source-register.md). Any future adapter should include its own smoke test, input validation, provenance record and explicit solver-not-installed failure.
