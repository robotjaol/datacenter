# Maintainability objective and certification boundary

The design objective is planned maintenance without interrupting the critical load. [Uptime's public Tier overview](https://connect.uptimeinstitute.com/tier-certification) distinguishes this objective from fault tolerance and separates certification stages. This project has no Tier certification or independently demonstrated topology compliance.

N+1 answers a capacity question; it does not prove that valves, breakers, control power, cables, headers and physical routes can be safely isolated while operating. The shared CHW system and common upstream services are explicit unresolved risks.

For every maintainable item, identify the isolation boundary, unaffected path, remaining capacity, controls dependencies, permitted concurrent work, rollback and evidence owner. Record the result in the maintenance matrix. Any case with unknown path independence remains open, even when arithmetic passes.
