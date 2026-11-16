"""Read-only metadata quality gate for a local calibrated JWST FITS image.

Usage: python scripts/validate_webb_fits.py jwst_i2d.fits --output validation.json
Passing metadata checks is NOT astrometric, photometric or SPICE validation.
"""
import argparse
import json
from pathlib import Path


def validate(path):
    import numpy as np
    from astropy.io import fits
    from astropy.wcs import WCS

    path = Path(path)
    with fits.open(path, memmap=True) as hdus:
        primary = hdus[0].header
        science = next((h for h in hdus if h.name == "SCI" and h.data is not None), None)
        if science is None:
            raise ValueError("Missing SCI image extension")
        if science.data.ndim != 2:
            raise ValueError("SCI extension must contain a 2-D image")
        wcs = WCS(science.header, hdus)
        if not wcs.has_celestial or wcs.pixel_n_dim != 2:
            raise ValueError("SCI extension lacks a usable 2-D celestial WCS")
        data = np.asarray(science.data)
        finite_count = int(np.count_nonzero(np.isfinite(data)))
        if not finite_count:
            raise ValueError("SCI image has no finite pixels")
        bunit = science.header.get("BUNIT") or primary.get("BUNIT")
        if not bunit:
            raise ValueError("Missing BUNIT; pixel values cannot be interpreted")
        date_obs = primary.get("DATE-OBS") or science.header.get("DATE-OBS")
        mjd_avg = primary.get("MJD-AVG") or science.header.get("MJD-AVG")
        if date_obs is None and mjd_avg is None:
            raise ValueError("Missing DATE-OBS and MJD-AVG")
        return {
            "file": path.name,
            "status": "metadata_gate_passed_not_astrometrically_validated",
            "telescope": primary.get("TELESCOP"),
            "instrument": primary.get("INSTRUME"),
            "filter": primary.get("FILTER"),
            "pupil": primary.get("PUPIL"),
            "date_obs": date_obs,
            "mjd_avg": mjd_avg,
            "bunit": str(bunit),
            "shape_yx": list(data.shape),
            "finite_pixels": finite_count,
            "wcs_ctype": list(wcs.wcs.ctype),
            "wcs_crval": [float(x) for x in wcs.wcs.crval],
            "warnings": [
                "No independent astrometric residual check performed",
                "No spacecraft SPICE geometry or light-time correction performed",
                "No photometric or PSF cross-calibration performed",
            ],
        }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("fits_path", type=Path)
    p.add_argument("--output", type=Path)
    a = p.parse_args()
    payload = json.dumps(validate(a.fits_path), indent=2) + "\n"
    if a.output:
        a.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
