# Commissioning plan

Commissioning authority owns the integrated plan; design discipline leads approve technical criteria; vendors support equipment tests; operations accepts turnover. All roles are proposed and unassigned for this portfolio.

| Gate | Required evidence | Release condition |
|---|---|---|
| Design review | OPR/BOD trace, sequences, testability and isolation review | Open blockers assigned |
| FAT | Approved vendor procedures, calibrated instruments, factory results | Material exceptions resolved |
| Installation/SAT | Installation/earthing/pressure/flush records, functional checks | Safe and approved test readiness |
| Integrated tests | Approved scenarios, risks, acceptance bands and rollback | Witnessed evidence meets criteria |
| Handover | As-builts, O&M manuals, spares, training and issue log | Operations sign-off |

For each test record: identifier, objective, requirement, configuration and software revision, prerequisites, instrument IDs/calibration, expected signals, recorded values, timestamps, deviations, reviewer and final disposition. Retain failed results alongside corrective retests.

The six IST-labelled software cases validate only the offline supervisory logic: normal supply, utility loss, generator ready, exhausted support, stale telemetry and leak/high-temperature alarms. They are not physical integrated systems tests. Their results are automatically exported to `commissioning-results.json`.

Physical acceptance bands must address continuity, voltage/frequency quality, thermal envelope, pressure/flow, alarm timing and recovery, and must be approved before testing. This portfolio intentionally supplies no live switching sequence or unreviewed protection settings.
