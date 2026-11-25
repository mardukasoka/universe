# Cross-project public navigation verification — 2026-11-18

This is a **review-branch inventory**, not a deployed navigation page. Repository existence is not evidence of a working public application. Do not add reciprocal links to deliberately isolated pages.

| Area | Repository/source | Verified 2026-11-18 | Public application URL |
| --- | --- | --- | --- |
| Astronomy / Universe Atlas | https://github.com/mardukasoka/universe | GitHub API: public, not archived; default branch `main` | Not verified |
| Historical computing / SIMH | https://github.com/mardukasoka/simh | GitHub API: public, not archived; default branch `master` | Not verified |
| Universal Transpiler | https://github.com/mardukasoka/transpiler | GitHub API: public, not archived; default branch `master` | Not verified |
| AI Evolution Matrix | https://github.com/mardukasoka/lattice-ai-evolution | GitHub API: public, not archived; default branch `main` | Not verified; standalone-page isolation must be preserved |
| Games / Chess Atlas | https://github.com/mardukasoka/chess-atlas | GitHub API: public, not archived; default branch `main` | Not verified |

## Relationship without repository duplication

`mardukasoka/transpiler` → **optional emulation / runtime-validation dependency** → `mardukasoka/simh`.

SIMH provides historical-machine simulation for testing generated or preserved programs. It is **not** a source-to-source translator, nor is it copied, vendored or merged into Transpiler. An executable compatibility test must identify the exact machine model, operating system and input/output expectations. Repository existence alone does not prove an emulator-based test is implemented.

## Scientific pipeline navigation

- Webb FITS discovery: `scripts/discover_webb_mast.py` in Universe draft PR #4; source catalog is NASA MAST. **Discovery script committed; actual MAST query results not verified.**
- Webb FITS metadata validation: `scripts/validate_webb_fits.py` in draft PR #4; real exposure validation not verified.
- Image reprojection: `scripts/reproject_sky_fits.py`; synthetic CI passed in [run 45106994567](https://github.com/mardukasoka/universe/actions/runs/45106994567) (reported 2026-11-24); real-image accuracy remains unverified.
- SPICE observer geometry, Jupiter/Juno reconstruction and Roman compatibility: requirements/design only, not validated implementations.
- SPHEREx reference data: DR1 and QR3 are now available; individual overlapping products and alignment remain unverified. See update below.

## URL verification discipline

1. Read deployment configuration (`pages` settings, workflows, custom domains, Workers config) before assigning a public URL.
2. Independently request the exact URL and capture timestamp, HTTP response, redirect destination and page title.
3. Test key navigation targets and distinguish HTTP failure from JS runtime failure.
4. Mark as **unverified**, not **broken**, whenever direct HTTP testing is unavailable.
5. Record scientific dataset identifiers, observation epochs, coordinate frames and citations independently from deployment status.
6. Keep the isolated AI Matrix and other explicitly standalone pages unlinked from the main Atlas unless authorized.

**Verification provenance:** Connected GitHub repository search, 2026-11-18. This run did not establish a successful direct HTTP check for any deployed application. Do not infer a live website from a repository URL.

## Verification update — 2026-11-25

- [SPHEREx DR1 overview](https://irsa.ipac.caltech.edu/data/SPHEREx/docs/overview_dr1.html) and [release guide](https://irsa.ipac.caltech.edu/spherex-archive-documentation/spherex-data-releases/) accessed 2026-11-25. DR1 covers surveys 1–2 and includes a 102-channel all-sky cube. Use DR1 and QR3 together; do not silently mix older QR2 calibration with these releases.
- Dataset provenance: spectral images DOI `10.26131/IRSA678`; all-sky cube DOI `10.26131/IRSA679`. Select a bounded overlapping field through the [IRSA access guide](https://irsa.ipac.caltech.edu/spherex-archive-documentation/spherex-data-access/), retaining wavelength, PSF, flags, variance and product identifiers. No FITS bytes retrieved in this update.
- [Application CI job](https://github.com/mardukasoka/universe/actions/runs/45106994571/job/137470454436) logs inspected 2026-11-25: Prettier reported five research files, including this inventory; typecheck/build in the checks job was skipped. Visual job passed. Do not bypass the formatting gate.
- Candidate URL `https://mardukasoka.github.io/universe/` could not be retrieved by the web client on 2026-11-25. Deployment configuration and HTTP status remain unverified; this is not a confirmed broken page.
