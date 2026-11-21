# Archive provenance and reproducibility gate — 2026-11-19

Status: **documentation only, review branch**. Last checked: **2026-11-19**. This file does not claim a MAST observation has been downloaded, validated, or reprojected.

## Source-verified archive facts
- [STScI JWST science data overview](https://jwst-docs.stsci.edu/accessing-jwst-data/jwst-science-data-overview): Stage 3 products include `i2d.fits` combined image products. **A filename suffix does not by itself validate WCS or scientific fitness.**
- [STScI Accessing JWST Data](https://jwst-docs.stsci.edu/accessing-jwst-data): MAST archives calibrated JWST products; calibration builds and reprocessing change products over time. Preserve `CAL_VER` from the FITS primary header, along with retrieval date, rather than assuming a stable archive file.
- [MAST JWST mission archive](https://archive.stsci.edu/missions-and-data/jwst): official discovery and data access entry point.

## Required per-observation registry record
`archive=MAST`; mission/instrument/filter; proposal/observation identifiers; product filename and `dataURI`; retrieval UTC; file SHA-256; FITS `CAL_VER` and calibration/reference context where available; exposure start/end and time scale; celestial WCS and coordinate frame; BUNIT; processing stage; DQ/footprint coverage; observer ephemeris source and validity interval; independently reproduced astrometric residuals with tolerance; reference links. Unknown fields must be explicitly `unverified`, never silently inferred.

## Execution gates
1. Run synthetic CI and inspect logs; absence of PR-triggered workflow runs is **not** a pass.
2. Run MAST metadata discovery; save exact candidate identifiers and discovery timestamp.
3. Download one public `i2d.fits` product; record immutable checksum and `CAL_VER`, inspect SCI extension.
4. Validate WCS, pixel masks, observation epoch and provenance; reproject onto independently sourced reference WCS; quantify overlap and residuals.
5. Separately reconstruct JWST observer position using mission-appropriate ephemerides/SPICE. Do not equate L2 nominal position with the telescope trajectory.
6. Roman: document compatibility until actual observations are available; no simulated data labeled as measured.

## Cross-project navigation boundary
Astronomy/Universe Atlas: [repository](https://github.com/mardukasoka/universe); matter, games, engineering and historical computing entries remain **deployment URL unverified** until independently requested. AI Evolution Matrix [repository](https://github.com/mardukasoka/lattice-ai-evolution) is deliberately standalone and must not receive reciprocal Atlas navigation links without approval. Universal Transpiler [repository](https://github.com/mardukasoka/transpiler) optionally uses [SIMH](https://github.com/mardukasoka/simh) for historical-machine execution validation; SIMH is **not** vendored or merged. A public GitHub repository does not prove a live application.

## Evidence and status
- Connected GitHub read, 2026-11-19: `scripts/discover_webb_mast.py` remains discovery-only; no downloaded observation is established.
- Connected GitHub workflow lookup for earlier audit commit `5c566a9` returned **zero associated pull-request runs** (limited to that commit and query type). This cannot establish CI success or failure for the branch overall.
- Public STScI/MAST documentation was accessed 2026-11-19. Deployed project URLs were **not successfully verified** in this check; none are classified broken.
- This record is a review-branch evidence snapshot, not a public-page deployment.
