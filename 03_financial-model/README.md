# Facility financial model

The model is a transparent **pre-tax, unlevered screening model**, not a lender or investment banking model. Source allowances are in `cost-allowances.csv`; their total equals the scenario's 48 million USD base CAPEX. The selected equipment schedule is not a priced bill of quantities.

Capacity revenue = IT kW × occupied fraction × USD/kW-month × 12. The active draw factor affects energy but not contracted capacity charges. Energy reimbursement appears as revenue, with the power bill shown separately as cost. At 100% reimbursement, electricity-price changes do not change net operating cash flow; that is a contractual scenario, not an error or a claim about real leases.

Annual fixed OPEX covers staffing/service/insurance/admin allowance; maintenance is a separate fraction of base physical CAPEX. Avoid adding maintenance again when replacing these buckets with quotations. Replacement occurs in year eight and an explicitly assumed residual asset value is recovered in year fifteen.

NPV includes initial capital at time zero. IRR suppresses ambiguous multiple-sign-change cases. Simple payback is undiscounted first-crossing interpolation and can be reversed by later replacement outflows; inspect cumulative cash flow. Gross lifecycle cost excludes revenue/reimbursement and includes residual recovery.

The nine sensitivity cases independently vary base physical CAPEX and capacity price ±20%. Maintenance and residual values follow changed base CAPEX; replacement remains a separate allowance. Expand with construction timing, occupancy scenarios, taxes, debt and working capital before using the model for commercial decisions.
