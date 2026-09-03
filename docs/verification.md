# Verification record — release 0.1.0

Verified locally on Windows with CPython 3.12, 3 September 2026. This record concerns the repository's software and publication artifacts, not a real facility.

- **14 unit tests passed:** configuration/domain errors, rack-capacity consistency, power conservation, N+1/zero-duty sizing, heat/flow units, calendar/energy/PUE, PV curtailment and zero IT, climate/load response, financial roots and sign patterns, cash-flow accounting, controls, reliability seeds/common causes, geometry bounds/identity and site gates.
- **Six offline supervisory cases passed:** normal, utility loss, generator ready, no support, stale telemetry, leak/high-temperature. These are not physical IST records.
- **Reference regeneration passed:** stored artifact hashes, numerically equivalent fresh results, schema agreement, cost allowance reconciliation, asset/telemetry identities and local Markdown links. Cross-platform numeric tolerance is 1e-10 relative or 1e-6 absolute; committed file integrity uses exact SHA-256.
- **Workbook:** eight sheets, no scanned formula errors, seven status checks OK; NPV, lifecycle cost and facility input agree with Python. Perturbation checks confirm physical-change invalidation, 100% energy recovery invariance and suppression of ambiguous IRR. Formula results are cached in the delivered file.
- **Publication QA:** all ten PDF pages and all eight workbook sheets received a layout review through rendered previews; critical diagrams and calculation areas received enlarged review. Original SVG and generated layout identity checks passed. DXF/USD files received structural/content checks, not native CAD/USD application validation.
- **PDF typography:** all extractable text uses embedded Latin Modern Roman regular or bold faces, matching the Computer Modern-style serif hierarchy implied by the supplied LaTeX references. All ten pages were rendered again after the typography change and inspected for clipping, overlap, and broken tables.

Remote GitHub Actions have not run because the package is prepared for user upload. CI is configured for Windows/Linux and Python 3.11/3.12. NVIDIA DSX, MATLAB/Simscape, CFD, live controls, physical commissioning and real-site engineering were not executed.

Reproduce the core checks from the repository root:

```bash
python -m unittest discover -s tests -v
python -m dcf.cli validate
python -m dcf.cli run --output build/reference
python scripts/verify_repository.py
python scripts/compare_scenarios.py
python scripts/verify_pdf_typography.py
```

Scenario comparisons retain fixed CAPEX unless stated. For example, the optional PV energy case does not include PV investment cost and must not be read as a PV investment recommendation.
