// Archive metadata normalizer. No network calls or synthetic geometry.
export function normalizeObservation(row) {
  if (!row || typeof row !== "object") throw Error("record must be an object");
  const id = String(row.product_id ?? "").trim();
  const uri = String(row.product_uri ?? "").trim();
  const archive = String(row.archive ?? "").trim().toUpperCase();
  if (!id || !/^https:\/\//.test(uri) || !["MAST", "PDS"].includes(archive)) throw Error("verified archive ID, HTTPS URI and MAST/PDS required");
  const times = ["start_utc", "mid_utc", "end_utc"].map(k => {
    const v = row[k];
    if (typeof v !== "string" || !/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z$/.test(v)) throw Error(k + " requires ISO UTC with Z");
    const ms = Date.parse(v);
    if (!Number.isFinite(ms) || new Date(ms).toISOString().slice(0,19) !== v.slice(0,19)) throw Error("invalid " + k);
    return ms;
  });
  if (!(times[0] <= times[1] && times[1] <= times[2])) throw Error("exposure interval out of order");
  if (!row.observer || !row.instrument || !row.source_url || !/^https:\/\//.test(row.source_url)) throw Error("observer, instrument and source URL required");
  return {
    id, archive, product_uri: uri, target: "JUPITER",
    observer: String(row.observer), instrument: String(row.instrument),
    start_utc: row.start_utc, mid_utc: row.mid_utc, end_utc: row.end_utc,
    time_scale: "UTC", original_time_scale: row.original_time_scale ?? "UTC",
    filter: row.filter ?? null, wavelength_um: row.wavelength_um ?? null,
    geometry_status: "unverified", calibration_status: "unverified",
    observer_position_km: null, target_position_km: null,
    camera_quaternion: null, field_of_view_deg: null,
    spice_kernel_manifest: [], provenance: [{source: row.source_url, archive}]
  };
}
export function importCatalogue(rows) {
  if (!Array.isArray(rows)) throw Error("expected array");
  const seen = new Set();
  return rows.map(row => {
    const item = normalizeObservation(row);
    const key = item.archive + ":" + item.id;
    if (seen.has(key)) throw Error("duplicate product " + key);
    seen.add(key); return item;
  });
}
