# Jupiter observation archive discovery — verified entry points

Status: archive interfaces verified; **zero individual JWST or Juno exposure records validated**. Do not describe campaign dates as measured exposure times.

## JWST / MAST
- Mission and instrument catalogue: https://archive.stsci.edu/missions-and-data/jwst
- MAST portal: https://mast.stsci.edu/portal/Mashup/Clients/Mast/Portal.html
- MAST documents JWST calibrated Stage 0–3 products and program/target/instrument search. For moving Jupiter, filter by target name rather than fixed sky coordinates.
- Candidate fields to retain from actual archive responses: proposal/program ID, observation ID, product ID, target, instrument, filter, start/end UTC, calibration level, product URI and archive citation. Derive midpoint only after validating the time interval.

## Juno / PDS
- Obtain perijove-linked instrument product identifiers from the NASA Planetary Data System, not from the perijove number alone.
- For each PDS product capture LID/LIDVID or archive identifier, instrument, observation start/stop and native time scale, source URL, product label and relevant spacecraft clock conversion.

## Cross-mission validation gates
1. Retrieve and retain the raw MAST/PDS query responses with access date and query parameters.
2. Reject missing IDs, ambiguous UTC conversion, incomplete intervals, and inconsistent target/instrument identifiers.
3. Pair observations by validated interval overlap or a documented maximum separation, **not** by shared perijove label.
4. Fetch NAIF SPICE kernels, test SPK/CK coverage and instrument frames, then compute light-time-aware geometry; leave vectors, pointing and footprints null until verified.
5. Keep 2023-09-07 (PJ54) and 2026-02-20–28 (PJ81) as discovery leads pending exposure-level verification.

## Current blocker
The cited public MAST documentation establishes search capability, not individual observation IDs or timestamps. No fabricated catalogue entries are permitted.
