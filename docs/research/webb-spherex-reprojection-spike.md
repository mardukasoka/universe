# Webb-to-survey image alignment spike

## Implemented
`scripts/reproject_sky_fits.py` accepts a calibrated 2-D celestial FITS image, a reference celestial FITS image, and an output path. It reads each WCS, resamples the source pixels onto the reference grid with `reproject_interp`, and writes both the aligned image and a footprint extension. It rejects non-overlapping inputs.

## Run
Install `numpy astropy reproject` in an isolated Python environment, then:
```bash
python scripts/reproject_sky_fits.py jwst_calibrated.fits survey_reference.fits aligned.fits
```

## Required validation before claiming scientific alignment
- Obtain a real calibrated JWST 2-D FITS product with celestial WCS from MAST; record product identifier, observation timestamp, instrument, filter, release/license and archive URL.
- Obtain a *publicly released* SPHEREx FITS image/map with celestial WCS covering the same sky region; verify availability first. A different public survey may serve as the initial reference if SPHEREx maps are not released.
- Compare footprint corners and several common reference sources against independent astrometric coordinates; record angular residuals and units.
- Inspect flux and surface-brightness units, pixel-area differences, distortion and PSF; interpolation alone is **not** photometric cross-calibration.
- Store provenance for both source inputs; keep native image data unchanged. Never interpret wavelength differences as temporal variability.
- Verify dependency versions and execute tests in CI. No real observations have been ingested or validated by this commit.

## Architecture boundary
This script performs 2-D sky reprojection only. Observer ephemerides, attitude, parallax, aberration, light-time and moving-target geometry require separate SPICE/astrometry work. HEALPix/HiPS tiling, Aladin Lite browser overlays, and the Uranometria integration remain separate follow-up stages.
