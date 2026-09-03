# Publication deliverables

`facility-portfolio.pdf` is the ten-page review dossier. `facility-model.xlsx` contains Overview, Inputs, Engineering, Energy, CashFlow, Sensitivity, Checks and Sources.

The dossier uses embedded Latin Modern Roman fonts to reproduce the serif typography implied by the supplied LaTeX references. See the [PDF publication style](../docs/publication-style.md) and bundled GUST Font License.

The workbook is an editable publication companion. Engineering sizing and financial schedules contain formulas. The 21-row occupancy energy table is imported from the Python model; tariff calculations remain editable. Physical-input changes trigger a rebuild status rather than silently retaining trusted headline results. Occupancy must match a listed 5% step. IRR is suppressed for non-conventional cash-flow signs.

To refresh energy manually: run the Python hourly/annual model for the required occupancy cases, update the Energy table and the Inputs baseline column together, then repeat the Checks and compare key totals against Python. Baseline columns preserve the provenance of the imported coefficients; changing them without regenerating energy invalidates the check.

The public core remains dependency-free. The optional PDF publication workflow uses ReportLab and pypdf (`python -m pip install reportlab pypdf`, `python scripts/build_dossier.py`, then `python scripts/verify_pdf_typography.py`). The Excel file is provided with embedded formulas and cached results; it is not required by the CLI or tests. Keep the workbook as a separate scenario when editing it; changes are not automatically written back to the JSON configuration.

Use source Markdown and configuration files to update the study. These publication files reflect release 0.1.0; third-party integrations and physical engineering validation are not represented as complete.
