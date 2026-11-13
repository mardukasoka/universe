# Jupiter observation campaigns — geometry-first spike

Status: research prototype specification; no live ephemeris or image registration has been verified.

## Goal
Display a historical observation at the spacecraft's **actual** position and pointing, with Jupiter's orientation and the observing instrument's field of view, before attempting NeRF or Gaussian splat reconstruction.

## Initial campaigns
- 2023-09-07: JWST/Juno PJ54 coordinated observations.
- 2026-02-20 through 2026-02-28: JWST/Juno PJ81 campaign.

These dates are discovery leads, **not validated exposure timestamps**. Obtain exposure start/mid/end UTC from MAST and PDS before generating markers.

## Canonical observation record (v0)
```json
{
  "id": "archive-product-id",
  "target": "JUPITER",
  "observer": "JWST",
  "instrument": "NIRSpec",
  "archive": "MAST",
  "product_uri": null,
  "start_utc": null,
  "mid_utc": null,
  "end_utc": null,
  "time_scale": "UTC",
  "spice_kernel_manifest": [],
  "reference_frame": "J2000",
  "observer_position_km": null,
  "target_position_km": null,
  "camera_quaternion": null,
  "field_of_view_deg": null,
  "wavelength_um": null,
  "geometry_status": "unverified",
  "calibration_status": "unverified",
  "provenance": []
}
```

Null means **unknown**, not zero. Do not render a supposedly measured marker until timestamps and geometry are validated.

## Processing stages
1. Inventory MAST and PDS products, retaining original identifiers and metadata.
2. Normalize times to UTC, retain original time standard and exposure interval.
3. Fetch SPICE kernels (SPK, CK, FK, IK, SCLK, LSK, PCK as required); verify coverage and kernel provenance.
4. Use SPICE geometry for spacecraft positions, camera pointing, Jupiter rotation, light-time correction and projected footprint. Distinguish emission, reception and spacecraft event times.
5. Render planet-centered and heliocentric views. Expose uncertainty, missing attitude data and source links.
6. Register calibrated images by physical footprint, filter and acquisition time.
7. Only then test small-region multi-view splatting or NeRF; compare with withheld exposures and independent geometry.

## Acceptance tests
- No invented or extrapolated ephemerides outside kernel coverage.
- Every observation marker links to a source archive product.
- Reprojected limb / known feature alignment is quantified in pixels or angular error.
- Multi-instrument observations preserve separate time intervals and wavelengths.
- Dataset partitioning prevents near-duplicate exposures from leaking between training and evaluation.
- Synthetic detections report injection/recovery and false-positive rates.
- A static browser build works without GPU training or paid services.

## Repository integration boundary
Keep this spike isolated from the existing scale-navigation code. Prefer an importable observation catalogue and an optional campaign viewer. No merge, deployment, purchase or external agent runs without explicit review.
