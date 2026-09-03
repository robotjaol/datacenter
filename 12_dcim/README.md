# DCIM and asset lifecycle

The generated rack and equipment schedules are the initial concept registers. Rack records include hall, coordinates, dimensions, design kW and A/B supply associations. Equipment has a persistent ID, system, path, nameplate, unit, derating and concept status.

Asset states progress through planned, procured, installed, tested, commissioned, in-service, maintenance and retired. Promotion requires evidence; never change status simply because a purchase order exists. Record manufacturer/model/serial, warranty, maintenance class, test certificate and drawing revision after procurement.

Capacity reconciliation should compare commissioned supply capacity, reserved kW, contracted kW, measured demand and margin. Installed redundant nameplates do not equal saleable IT capacity. A dashboard should surface bottlenecks across power, cooling, space and weight simultaneously.

Future integrations may export this schema to a selected DCIM system. No third-party DCIM is bundled or claimed operational. Imports must preserve identifiers, units and evidence references; changes to supply associations require topology review.
