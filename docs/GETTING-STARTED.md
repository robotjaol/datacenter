# Getting Started

This project models a hypothetical 5 MW data center facility as an independent engineering portfolio. Its scope covers the building, electrical infrastructure, cooling, energy, facility economics, reliability, commissioning, and operations. It contains no internal AWS design information.

Open the PDF under `deliverables/` for the portfolio narrative. The workbook in the same directory contains assumptions, engineering sizing, energy, cash flow, sensitivity analysis, checks, and sources. Blue text identifies editable assumptions; green text identifies references to other worksheets.

Run the commands listed in the main README from the repository root. Modify `configs/tropical-5mw.json`, then create a new result set with the `--output` option. Do not combine results produced from different configurations. Weather, tariffs, costs, emissions, and site data are illustrative inputs rather than results from an Indonesian site survey.

For GitHub, upload the complete contents of the project directory, including dot-prefixed directories such as `.github`. Exclude caches, `.venv`, and `node_modules`. The intended repository is `robotjaol/datacenter`; it was empty when inspected. This package is prepared for the owner to upload.

Release 0.1 is a reproducible concept study. Validated CFD, protection coordination, structural design, permit documents, coordinated BIM, and physical commissioning require the later development stages listed in [Maturity and Release Gates](maturity.md).
