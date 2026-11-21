"""Reproject a calibrated celestial FITS image onto a reference FITS WCS.

Inputs must be actual 2-D celestial images with valid WCS headers.
This is an image-geometry proof of concept, NOT a spacecraft SPICE solution.
Usage:
  python scripts/reproject_sky_fits.py webb_calibrated.fits reference_sky.fits aligned.fits
"""
import argparse
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from reproject import reproject_interp


def read_celestial_image(path):
    with fits.open(path, memmap=False) as hdul:
        for hdu in hdul:
            if hdu.data is None or np.ndim(hdu.data) != 2:
                continue
            wcs = WCS(hdu.header)
            if not wcs.has_celestial or wcs.pixel_n_dim != 2:
                continue
            return np.asarray(hdu.data, dtype=float), wcs.celestial
    raise ValueError(f"No 2D celestial image with usable WCS: {path}")


def align(source, reference, output):
    src_data, src_wcs = read_celestial_image(source)
    ref_data, ref_wcs = read_celestial_image(reference)
    aligned, footprint = reproject_interp(
        (src_data, src_wcs), ref_wcs, shape_out=ref_data.shape,
        return_footprint=True,
    )
    valid = (footprint > 0) & np.isfinite(aligned)
    if not np.any(valid):
        raise ValueError("Images have no overlapping sky coverage")
    header = ref_wcs.to_header()
    header["HISTORY"] = "Reprojected source image to reference celestial WCS"
    header["HISTORY"] = f"Source: {Path(source).name}"
    header["HISTORY"] = f"Reference: {Path(reference).name}"
    fits.HDUList([
        fits.PrimaryHDU(data=aligned.astype("float32"), header=header),
        fits.ImageHDU(data=footprint.astype("float32"), name="FOOTPRINT"),
    ]).writeto(output, overwrite=False)
    return {"covered_pixels": int(valid.sum()), "total_pixels": int(valid.size)}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source")
    p.add_argument("reference")
    p.add_argument("output")
    a = p.parse_args()
    print(align(a.source, a.reference, a.output))
