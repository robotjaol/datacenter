# Electrical concept package

See the original `single-line-concept.svg` and generated equipment schedule. Each path is sized against full facility demand after design margin, with one local capacity unit unavailable. UPS protects the modeled IT load; the battery screen excludes compressor and pump ride-through. Supporting controls/auxiliary UPS must be added in detailed design.

The transformer and generator allowances are checked against complete facility demand, including cooling. UPS counts refer only to the UPS-backed IT distribution. Do not add A and B nameplates to the actual utility demand. The capacity numbers intentionally favor reviewable conservative allowances over optimized bus utilization.

## Studies required for detailed design

Short-circuit study inputs: utility maximum/minimum fault contribution, X/R, transformer impedance/tap, generator transient/subtransient data, cable geometry, motors and grounding. Evaluate normal, islanded, maintenance and tie configurations. Record fault duty at every bus and compare with verified ratings.

Protection coordination inputs: one-line revision, equipment curves, relay/fuse settings, CT ratios, clearing-time requirements, selectivity objectives and critical-load tolerances. Deliver time-current plots, setting files, exception log and independent review. No relay settings are supplied by this concept.

Cable sizing must check ampacity installation method, grouping/ambient derating, voltage drop, short-circuit withstand, protective conductor sizing, fire performance and termination conditions. Earthing, lightning, arc-flash and emergency power-off interfaces remain separate studies. Battery procurement requires discharge curves and thermal/fire review; the kWh figure alone cannot specify strings.
