# Geometry and BIM basis

`dcf.geometry` generates original hall rectangles and rack placements in metres. SVG is the readable concept; DXF stores hall/rack outlines; OpenUSD stores rack massing and stable asset IDs. The generated drawing covers white space only. It is not an as-built, surveyed site plan, structural design or coordinated BIM deliverable.

Rack footprint is an illustrative 0.6 × 1.2 m, 2.2 m high; pitch is 1.2 m across and 3 m between rows. These are layout assumptions, not an access/egress compliance determination. Hall geometry grows with the rack count. No claimed floor loading is inferred from rack kW.

The accommodation schedule reserves functional areas for A/B rooms, battery zones, cooling interfaces, operations, logistics and external plant. Site-specific floor load, fire compartments, evacuation, access, equipment replacement routes, drainage and seismic restraint remain open.

BIM next gate: approved survey coordinates; authored discipline models; agreed classification and naming; asset properties; clash rules; issue ownership; reference-origin/georeferencing checks; export validation. Do not rename the massing file to IFC or declare an LOD based on visual appearance.
