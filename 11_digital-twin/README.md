# Digital twin contract

The release provides rack-only OpenUSD massing and a synthetic telemetry batch, joined by `asset_id`. It demonstrates an information contract, not a live digital twin. No historian, sensor or external account is connected.

Each telemetry record contains offset-aware timestamp, asset ID, metric, typed value, unit, quality and source. Use asset identity as a stable key; geometry names may replace punctuation for OpenUSD prim naming. Never infer identity from display order or coordinates.

The example records all racks at the configured mean demand as a separate steady snapshot; they are not the first hour of the annual sinusoidal profile. For live ingestion, validate ID membership, timestamp ordering, duplicate handling, unit conversion, value bounds and quality. Preserve raw measurements alongside any estimate.

An Omniverse adapter should open the project's original USD, map IDs, and display source/age/quality before overlaying telemetry. Refer to NVIDIA's current terms and hardware requirements. No NVIDIA scene, simulation dataset or asset is redistributed here.
