# Earth God's-eye observation viewer — architecture proposal

Status: design only; no satellite observations imported or viewer changes deployed.

## Shared temporal observation model
Use the same provenance-aware record contract as the Juno/JWST spike: archive product ID, observer/instrument, original and normalized acquisition intervals, target, wavelength/band, calibration, source URL, reference frame, ephemeris and attitude/kernel coverage, geometry status, footprint and uncertainty. Keep unknown geometry null.

## Three distinct spatial layers
1. **Earth-fixed imagery:** WGS84 georeferenced raster or vector tiles with acquisition timestamp, sensor and cloud/quality mask (e.g., Sentinel-2, Landsat, NASA Earthdata). Never present historical imagery as live.
2. **Satellite orbital state and swath:** timestamped spacecraft position, pointing, instrument field of view and derived ground footprint; distinguish public TLE/SGP4 approximate orbit tracks from precision ephemerides.
3. **Celestial background:** a sky sphere centered on the observer, projected in ICRS/equatorial coordinates with appropriate Earth orientation and observation epoch. SPHEREx full-sky infrared products may serve as wavelength-selectable background when suitable public mosaics exist; do not treat SPHEREx as an Earth-imaging satellite or attach its sky pixels to Earth's surface.

## Candidate open data providers
- Copernicus Data Space Ecosystem — Sentinel imagery: https://dataspace.copernicus.eu/
- USGS Landsat: https://www.usgs.gov/landsat-missions
- NASA Earthdata: https://www.earthdata.nasa.gov/
- NASA CelesTrak? No: CelesTrak is an independent orbital-data provider; https://celestrak.org/ (TLE/GP data, not measured imagery).
- NASA SPHEREx mission: https://science.nasa.gov/mission/spherex/ ; check actual public archive products, release dates and spectral band coverage before promising a full-sky panorama.

## First vertical slice
Choose one Sentinel-2 or Landsat image with a verifiable acquisition interval and footprint. Display its historical coverage on the existing Earth globe, with a time slider and an explicit source link. Next add orbital track at acquisition time and optional SPHEREx celestial shell. Include frame conversions (ITRF/ECEF vs ICRS), Earth rotation, UTC/TAI/TDB distinctions and accuracy labels.

## Integration constraints
Separate Earth surface imagery, spacecraft trajectories and background sky; use on-demand tiles/low-resolution previews for mobile performance. No merges, deployments or paid data without review.
