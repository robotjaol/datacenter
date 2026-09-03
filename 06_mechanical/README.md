# Mechanical concept package

The original `cooling-loop-concept.svg` separates air terminals and liquid CDUs while retaining a shared central chilled-water plant. The equipment schedule gives N+1 chiller capacity and N+1 CDU capacity per hall. Pumps are represented by an energy allowance; hydraulic pump selection is not claimed.

At design load, the air path removes 3.5 MW of IT heat plus terminal-fan heat, and the liquid path 1.5 MW of IT heat. UPS/distribution losses and envelope gains are added to total plant heat. Water density/heat capacity are approximated as constant; actual coolant mixture and temperatures change these properties.

The system concept must resolve isolation valves, strainers, bypasses, expansion/pressurization, treatment, metering, balancing, relief, drainage and drain-down areas. N+1 plant alone does not make shared headers maintainable. Define sectional isolation, simultaneous-maintenance rules and independent control-power supplies.

At the CDU boundary, obtain supplier flow/pressure/temperature/chemistry limits and condensation requirements. The [OCP liquid-distribution guidance](https://www.opencompute.org/documents/ocp-acf-reference-design-guidance-white-paper-pdf-1) informs the interface questions, not a copied pipe design.

Cooling ride-through remains unresolved: IT power continuity may continue after cooling power interruption. Validate thermal storage, rotating-machine restart, valve behavior, pump support, generator load sequencing and room/coolant thermal response before finalizing battery runtime or acceptance bands.
