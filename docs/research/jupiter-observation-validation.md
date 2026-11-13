# Jupiter campaign observation validation (v0)

This document is a deterministic validation contract for archive ingestion. It does not assert that any archive exposure or SPICE solution has been retrieved.

## Record states
- `candidate`: campaign/date lead only; never render as a measured footprint.
- `archived`: archive identifier, product URI and exposure interval verified from MAST or PDS.
- `geometry_ready`: kernel manifest, coverage and reference-frame transforms validated for the exposure interval.
- `registered`: calibrated image has a quantified reprojection residual and documented quality gates.

## Mandatory checks before map markers
1. Stable unique archive product ID; nonempty archive source and provenance URL.
2. Parse UTC ISO-8601 with explicit Z; start <= mid <= end. Keep original time scale separately.
3. Instrument and observer must match archive metadata; never infer JWST instrument from campaign name.
4. For geometry, retain kernel names, source URLs, checksums, versions and coverage intervals. Validate SPK/CK/SCLK/IK/FK/PCK/LSK as applicable.
5. Calculate observer-target vector, attitude and instrument FOV using the appropriate frame and light-time convention; state which epoch each vector refers to.
6. Reject missing CK coverage, unknown instrument boresight, or out-of-coverage interpolation. Never substitute a zero vector or identity quaternion for unknowns.
7. Record Jupiter body-fixed frame and shape model; use consistent longitude convention and distinguish planetographic from planetocentric latitude.
8. Report projected footprint only with a tested intercept and angular/pixel uncertainty; allow a non-intersecting FOV.
9. Preserve separate products and timestamps for each instrument and filter, even during coordinated campaigns.

## Minimal fixture cases for automated tests
| Case | Input | Expected result |
| --- | --- | --- |
| Missing timestamps | candidate campaign with null times | candidate only; no map marker |
| Reversed interval | end before start | reject |
| Time-zone ambiguity | timestamp without Z or original time scale | reject until normalized |
| Missing attitude | valid SPK but no CK coverage | archive metadata accepted; footprint blocked |
| No intercept | instrument FOV misses Jupiter | valid geometry, no surface footprint |
| Missing source | product identifier without archive URI | reject archive verification |
| Mixed instruments | two filters at different UTC times | distinct observation records |
| Valid geometry | complete kernels and instrument metadata | geometry_ready only after numeric checks |

## Immediate acquisition targets
- MAST: query Jupiter observations around the 2023-09-07 and 2026-02-20–28 campaign leads; retain observation ID, product ID, instrument, filters, calibration level and exact exposure timestamps.
- PDS: retrieve Juno observation/product IDs for the corresponding perijoves; do not assume exact simultaneous exposure.
- NAIF: build a versioned kernel manifest for Juno, JWST and Jupiter with coverage and checksums.

## Release gate
A browser viewer may display **candidate campaign dates** with a conspicuous unverified label. It must not display fabricated spacecraft positions, instrument footprints or image alignment. The first merge-ready milestone is a reproducible catalogue import plus automated negative-case tests; interactive reconstruction follows separately.
