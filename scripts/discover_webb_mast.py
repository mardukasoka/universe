"""Discover public JWST calibrated 2-D image products in MAST.

Read-only metadata discovery; does not download or alter any observation.
Requires: pip install astroquery
Example:
  python scripts/discover_webb_mast.py --ra 83.82 --dec -5.39 --radius-arcmin 2 --limit 10 --output jwst_candidates.json

The returned list is a candidate inventory, not validated image ingestion.
"""
import argparse
import json
from pathlib import Path


def discover(ra, dec, radius_arcmin, limit):
    if not (0 <= ra < 360 and -90 <= dec <= 90):
        raise ValueError("RA/Dec out of range")
    if not (0 < radius_arcmin <= 60):
        raise ValueError("Radius must be in (0, 60] arcmin")
    if limit < 1:
        raise ValueError("Limit must be positive")
    from astroquery.mast import Observations
    from astropy.coordinates import SkyCoord
    import astropy.units as u

    center = SkyCoord(ra=ra * u.deg, dec=dec * u.deg, frame="icrs")
    observations = Observations.query_region(center, radius=radius_arcmin * u.arcmin)
    # Filter by the actual mission/collection metadata, not product filenames alone.
    obs = observations[observations["obs_collection"] == "JWST"]
    if len(obs) == 0:
        return []
    products = Observations.get_product_list(obs)
    candidates = Observations.filter_products(
        products, productType="SCIENCE", extension="fits",
        calib_level=[3],
    )
    results = []
    for row in candidates:
        name = str(row["productFilename"])
        # _i2d.fits is the JWST level-3 rectified 2-D science image.
        if not name.lower().endswith("_i2d.fits"):
            continue
        results.append({
            "obs_id": str(row["obs_id"]) if "obs_id" in row.colnames else None,
            "obsID": int(row["obsID"]) if "obsID" in row.colnames else None,
            "productFilename": name,
            "dataURI": str(row["dataURI"]),
            "calib_level": int(row["calib_level"]),
            "productType": str(row["productType"]),
            "source": "MAST JWST public product catalog",
            "validation": "discovery_only",
        })
        if len(results) >= limit:
            break
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ra", type=float, required=True, help="ICRS RA degrees")
    parser.add_argument("--dec", type=float, required=True, help="ICRS Dec degrees")
    parser.add_argument("--radius-arcmin", type=float, default=2)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = discover(args.ra, args.dec, args.radius_arcmin, args.limit)
    args.output.write_text(json.dumps({
        "query": {"ra_deg": args.ra, "dec_deg": args.dec,
                  "radius_arcmin": args.radius_arcmin},
        "products": rows,
        "note": "Candidates only: inspect SCI extension WCS, units, DQ, time and provenance before reprojection",
    }, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} candidate JWST i2d products to {args.output}")


if __name__ == "__main__":
    main()
