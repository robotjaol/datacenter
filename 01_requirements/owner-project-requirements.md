# Owner project requirements

| ID | Requirement | Acceptance evidence |
|---|---|---|
| OPR-001 | Ultimate 5,000 kW design IT; hall/rack totals reconcile | Input validation; capacity test |
| OPR-002 | Distinguish design, occupied and actual demand | Scenario, hourly output and annual cash flow |
| OPR-003 | Two electrical paths; each supports full required load with one unit unavailable | Per-path capacity check; later routing/maintenance review |
| OPR-004 | Central cooling retains required steady-state capacity after one chiller loss | Chiller sizing; later hydraulic and transient validation |
| OPR-005 | Annual energy metrics use consistent boundaries and calendar | Hourly/monthly energy reconciliation |
| OPR-006 | Facility economics expose assumptions and energy recovery | Cash-flow reconciliation and sensitivity |
| OPR-007 | Asset IDs agree between geometry and telemetry | Generated rack identity checks |
| OPR-008 | Loss of telemetry cannot produce an asserted known supply state | IST-005 software case |
| OPR-009 | Define physical commissioning gates and evidence ownership | Commissioning plan and test records |
| OPR-010 | Public core can run without commercial simulation products | Standard-library test/CLI commands |

The listed requirements are portfolio requirements proposed by the author, not a real owner's signed brief. Maintainability, safety and environmental requirements need quantitative acceptance bands agreed with equipment suppliers and reviewers before execution on a facility.
