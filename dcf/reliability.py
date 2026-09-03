"""Illustrative steady-state availability, not an outage-duration or Tier model."""
import math
import random

def evaluate(path_unavailability: float, common_cause: float, samples: int, seed: int) -> dict:
    if not 0 <= path_unavailability <= 1 or not 0 <= common_cause <= 1 or samples < 1:
        raise ValueError("Invalid availability parameters")
    # The common event is independent of the two independent path events.
    exact = (1-common_cause)*(1-path_unavailability**2)
    rng = random.Random(seed)
    available = 0
    for _ in range(samples):
        common, a, b = rng.random(), rng.random(), rng.random()
        available += common >= common_cause and (a >= path_unavailability or b >= path_unavailability)
    observed = available/samples
    z = 1.96
    center = (observed+z*z/(2*samples))/(1+z*z/samples)
    half = z*math.sqrt(observed*(1-observed)/samples+z*z/(4*samples*samples))/(1+z*z/samples)
    return {"exact_availability": exact, "sample_availability": observed,
            "wilson_95_low": center-half, "wilson_95_high": center+half,
            "samples": samples, "seed": seed, "common_cause_unavailability": common_cause,
            "boundary": "two aggregate paths plus one independent common event; no repair chronology"}
