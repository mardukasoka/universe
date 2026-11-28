# Observer-aware imaging: Roman, New Horizons and Jupiter

## Two views for every observation
1. **Sky-aligned view:** Calibrated FITS image on a declared celestial WCS/projection; preserve native product, filter/bandpass, units, distortion, footprint and provenance.
2. **Physical observer view:** Observer position and velocity, instrument attitude and field of view, target state, exposure time interval, light-time convention, aberration correction and reference frame. Derive a line-of-sight geometry from ephemerides rather than treating a common RA/Dec as identical viewing rays.

## Observer registry
Include JWST (Sun–Earth L2 halo orbit), Euclid (L2), Gaia (L2 mission), Nancy Grace Roman Space Telescope (planned L2 operations; do not claim observations before launch), Hubble (low Earth orbit), ground observatories (site coordinates and Earth orientation), Juno (Jupiter), and New Horizons (heliocentric trajectory). Obtain mission-specific ephemeris and attitude coverage from authoritative SPICE kernels or other validated mission data; don't approximate all L2 missions as a single point.

## Validation experiments
- **New Horizons parallax:** Reproduce a published near-star parallax demonstration from New Horizons versus Earth observations, with observation epochs, actual spacecraft baseline, source distance, predicted angular offset and measured offset. Distinguish this large-baseline parallax from annual parallax and from image alignment residuals.
- **Jupiter:** Pair actual Webb and Juno observations where temporal coverage allows; compute positions, apparent limb/feature geometry and viewing directions independently, with time/light-time corrections.
- **Roman compatibility:** Test expected FITS/WCS/footprint ingestion against documented Roman data conventions or simulated products until real public observations exist; mark simulation clearly.
- **Distant sources:** Demonstrate negligible baseline parallax for Little Red Dots while preserving different filters, PSFs and observation times.

## Required checks
Record coordinate frame, time scale (UTC/TDB as applicable), time interval, ephemeris source/kernel versions, target/observer IDs, units, light-time and stellar aberration policy, image WCS, photometric calibration, error budget, and distance uncertainty. Compare numerical output against independent mission reference products; include explicit pass/fail tolerances. No invented mission pointing or distance reconstruction.

## Scope and performance
Astropy + reproject perform 2-D image registration; SPICE geometry is a separate pipeline. Use cached, progressive HiPS/HEALPix tiles for mobile rendering, while retaining a native high-resolution image path. Never infer 3-D object depths from a 2-D image alone.

This is a design/validation specification, not a claim that the data or reconstruction has been implemented.
