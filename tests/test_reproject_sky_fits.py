"""Synthetic WCS reprojection smoke tests; not a substitute for real JWST data."""
import importlib.util
from pathlib import Path
import numpy as np
import pytest
from astropy.io import fits
from astropy.wcs import WCS

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "reproject_sky_fits.py"
spec = importlib.util.spec_from_file_location("sky_reproject", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def make_image(path, ra=120.0, dec=-20.0, n=32):
    w = WCS(naxis=2)
    w.wcs.crpix = [n / 2, n / 2]
    w.wcs.cdelt = [-0.001, 0.001]
    w.wcs.crval = [ra, dec]
    w.wcs.ctype = ["RA---TAN", "DEC--TAN"]
    data = np.ones((n, n), dtype=np.float32)
    fits.PrimaryHDU(data=data, header=w.to_header()).writeto(path)


def test_identical_wcs_preserves_constant_image(tmp_path):
    source, reference, output = [tmp_path / x for x in ("src.fits", "ref.fits", "out.fits")]
    make_image(source)
    make_image(reference)
    stats = module.align(source, reference, output)
    with fits.open(output) as h:
        covered = h["FOOTPRINT"].data > 0
        assert np.any(covered)
        np.testing.assert_allclose(h[0].data[covered], 1, atol=1e-5)
        assert stats["covered_pixels"] > 0


def test_nonoverlap_fails(tmp_path):
    source, reference, output = [tmp_path / x for x in ("src.fits", "ref.fits", "out.fits")]
    make_image(source, ra=120)
    make_image(reference, ra=220)
    with pytest.raises(ValueError, match="(?i)no overlapping sky coverage"):
        module.align(source, reference, output)


def test_shifted_wcs_preserves_constant_flux_surface_brightness(tmp_path):
    source, reference, output = [tmp_path / x for x in ("src.fits", "ref.fits", "out.fits")]
    make_image(source, ra=120.0)
    make_image(reference, ra=120.01)
    stats = module.align(source, reference, output)
    with fits.open(output) as h:
        valid = (h["FOOTPRINT"].data > 0) & np.isfinite(h[0].data)
        assert 0 < stats["covered_pixels"] < stats["total_pixels"]
        np.testing.assert_allclose(h[0].data[valid], 1.0, atol=1e-5)


def test_missing_celestial_wcs_rejected(tmp_path):
    source = tmp_path / "invalid.fits"
    fits.PrimaryHDU(data=np.ones((16, 16))).writeto(source)
    with pytest.raises(ValueError, match="No 2D celestial image"):
        module.read_celestial_image(source)
