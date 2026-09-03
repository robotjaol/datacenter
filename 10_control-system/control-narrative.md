# Supervisory controls narrative

This package defines offline observations and alarm expectations. It cannot write to PLCs, BMS or EPMS. Actual breaker transfer, interlocks, emergency shutdown and equipment protections remain in approved local controls.

States: UTILITY when the utility is healthy; GENERATOR when utility is lost and generator is proven ready; BATTERY when supply is lost and energy support is available; UNSERVED when neither supply nor battery is available; UNKNOWN when essential telemetry is stale. Stale data takes priority over an apparently healthy signal.

Alarm examples: utility lost; liquid leak; inlet temperature at or above the illustrative 30 C threshold; telemetry stale. In actual design, define threshold, delay, deadband, hysteresis, latching, acknowledgement, escalation and restoration separately. The simple offline evaluator does not implement timers or contact bounce.

Time synchronization, point quality, sequence-of-events resolution, local/manual authority and independent control-power arrangements belong in the controls specification. Retain raw events and acknowledgements. Never allow a dashboard's estimate of state to override protective logic.

The six numbered scenarios in `dcf.controls` are acceptance examples for this supervisory model. Factory/hardware tests, cause-and-effect approval and integrated facility tests remain separate evidence gates.
