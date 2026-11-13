# Jupiter observation importer — test execution

Executed 2026-11-13 with Node.js v22.16.0 using `node --test scripts/jupiter-observation-import.test.mjs` against the committed source and test contents copied into an isolated local directory.

Result: **8 tests passed; 0 failed**. Tests cover accepted metadata, missing time, reversed interval, ambiguous timezone, invalid calendar date, missing source URL, duplicate product IDs and preservation of distinct products.

Limitations: these are synthetic metadata fixtures, not MAST/PDS observations. No archive exposure records have yet been retrieved or cross-matched; no SPICE kernels, positions, attitudes, image footprints or calibrated image registrations have been validated. The test was run locally, not by GitHub Actions.

Next acceptance gate: query the NASA archives, retain source product URLs and exact UTC intervals, then introduce a versioned SPICE kernel manifest and numeric geometry checks before displaying measured markers.
