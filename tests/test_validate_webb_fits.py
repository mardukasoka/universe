"""Offline metadata-gate regression tests using synthetic FITS, not real JWST data.

Run: python -m pytest -q tests/test_validate_webb_fits.py
"""
import importlib.util
from pathlib import Path

import numpy as np
import pytest
from astropy.io import fits
from astropy.wcs import WCS

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_webb_fits.py"
spec = importlib.util.spec_from_file_location("validate_webb_fits", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def fixture(path, *, celestial=True, finite=True, units=True, timestamp=True):
    primary = fits.PrimaryHDU()
    primary.header["TELESCOP"] = "JWST"
    primary.header["CAL_VER"] = "test-only"
    if timestamp:
        primary.header["DATE-OBS"] = "2026-01-01"
    wcs = WCS(naxis=2)
    wcs.wcs.crpix = [8, 8]
    wcs.wcs.cdelt = [-0.001, 0.001]
    wcs.wcs.crval = [83.8, -5.4]
    wcs.wcs.ctype = ["RA---TAN", "DEC--TAN"] if celestial else ["LINEAR", "LINEAR"]
    data = np.ones((16, 16), dtype=np.float32) if finite else np.full((16, 16), np.nan, dtype=np.float32)
    sci = fits.ImageHDU(data=data, header=wcs.to_header(), name="SCI")
    if units:
        sci.header["BUNIT"] = "MJy/sr"
    fits.HDUList([primary, sci]).writeto(path)


def test_metadata_and_checksum(tmp_path):
    path = tmp_path / "synthetic_i2d.fits"
    fixture(path)
    result = validator.validate(path)
    assert result["status"] == "metadata_gate_passed_not_astrometrically_validated"
    assert result["cal_ver"] == "test-only"
    assert len(result["sha256"]) == 64
    assert result["file_size_bytes"] == path.stat().st_size
    assert result["finite_pixels"] == 256
    assert result["shape_yx"] == [16, 16]


@pytest.mark.parametrize("changes,expected", [
    ({"celestial": False}, "celestial WCS"),
    ({"finite": False}, "no finite pixels"),
    ({"units": False}, "Missing BUNIT"),
    ({"timestamp": False}, "Missing DATE-OBS"),
])
def test_reject_invalid_metadata(tmp_path, changes, expected):
    path = tmp_path / "invalid.fits"
    fixture(path, **changes)
    with pytest.raises(ValueError, match=expected):
        validator.validate(path)


def test_reject_missing_science_extension(tmp_path):
    path = tmp_path / "missing_sci.fits"
    fits.PrimaryHDU().writeto(path)
    with pytest.raises(ValueError, match="Missing SCI image extension"):
        validator.validate(path)


def test_reject_three_dimensional_science_image(tmp_path):
    path = tmp_path / "cube.fits"
    fixture(path)
    with fits.open(path, mode="update") as hdus:
        hdus["SCI"].data = np.ones((2, 16, 16), dtype=np.float32)
        hdus.flush()
    with pytest.raises(ValueError, match="2-D image"):
        validator.validate(path)


def test_accept_mjd_avg_without_date_obs(tmp_path):
    path = tmp_path / "mjd_only.fits"
    fixture(path, timestamp=False)
    with fits.open(path, mode="update") as hdus:
        hdus[0].header["MJD-AVG"] = 61041.0
        hdus.flush()
    result = validator.validate(path)
    assert result["date_obs"] is None
    assert result["mjd_avg"] == 61041.0
    assert result["status"] == "metadata_gate_passed_not_astrometrically_validated"
