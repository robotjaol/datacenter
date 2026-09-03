# Facility architecture and interfaces

The building accommodates four halls, separate electrical A/B rooms, CHW distribution, CDU service zones, operations/security functions and logistics. External plant includes generation, transformers and chillers. Room area allowances appear in the accommodation schedule; detailed siting and fire separation are open.

Power paths terminate at the rack inlet; the workload supplies an external heat profile. Cooling boundaries are ambient/heat rejection, facility water system (FWS), CDU heat exchanger, technology cooling system (TCS), and IT cold plate. Meter boundaries separate gross facility power from IT energy and grid imports.

| Interface | Owner | Required handoff |
|---|---|---|
| Utility → intake | Utility/electrical engineer | Voltage, firm capacity, fault level, protection, earthing |
| Building → rack | Facility/IT interface | Dual feeds, design kW, weight, dimensions, inlet envelope |
| FWS → CDU | Mechanical/vendor | Flow, temperature, pressure, chemistry, isolation |
| CDU → TCS | IT/vendor | Fluid compatibility, dew point, pressure, quality, leak response |
| EPMS/BMS → historian | Controls/operations | Asset ID, time, units, quality, alarm priorities |
| Contractor → operations | Commissioning authority | Approved as-builts, manuals, spares, witnessed tests |

Shared controls, upstream grid, cooling headers, fuel logistics and human actions are possible common causes. Physical separation and concurrent maintenance remain review tasks rather than assumed properties of duplicated equipment.
