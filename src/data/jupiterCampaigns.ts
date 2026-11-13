/**
 * Seed catalogue for the Jupiter observation explorer.
 * Dates below identify campaign windows, NOT individual exposure timestamps.
 * Scientific camera poses must be derived from archive metadata and SPICE.
 */
export type Campaign = {
  id: string;
  title: string;
  startUTC: string;
  endUTC: string;
  targets: string[];
  platforms: string[];
  sourceArchives: { label: string; url: string }[];
  geometryStatus: "unresolved" | "spice-validated";
  observationStatus: "campaign-window-only" | "exposure-verified";
};
export const jupiterCampaigns: readonly Campaign[] = [
  {
    id: "juno-pj54-jwst-2023",
    title: "Juno PJ54 / JWST coordinated Jupiter observations",
    startUTC: "2023-09-07T00:00:00Z",
    endUTC: "2023-09-08T00:00:00Z",
    targets: ["Jupiter"],
    platforms: ["Juno", "JWST"],
    sourceArchives: [
      { label: "MAST", url: "https://mast.stsci.edu/" },
      { label: "NASA PDS", url: "https://pds.nasa.gov/" },
      { label: "NAIF SPICE", url: "https://naif.jpl.nasa.gov/naif/" }
    ],
    geometryStatus: "unresolved",
    observationStatus: "campaign-window-only"
  },
  {
    id: "juno-pj81-jwst-2026",
    title: "Juno PJ81 / JWST Jupiter campaign",
    startUTC: "2026-02-20T00:00:00Z",
    endUTC: "2026-03-01T00:00:00Z",
    targets: ["Jupiter"],
    platforms: ["Juno", "JWST"],
    sourceArchives: [
      { label: "MAST", url: "https://mast.stsci.edu/" },
      { label: "NASA PDS", url: "https://pds.nasa.gov/" },
      { label: "NAIF SPICE", url: "https://naif.jpl.nasa.gov/naif/" }
    ],
    geometryStatus: "unresolved",
    observationStatus: "campaign-window-only"
  }
] as const;

export function validateCampaigns(campaigns: readonly Campaign[]): string[] {
  const errors: string[] = [];
  const ids = new Set<string>();
  for (const c of campaigns) {
    if (ids.has(c.id)) errors.push(`Duplicate campaign: ${c.id}`);
    ids.add(c.id);
    if (!Number.isFinite(Date.parse(c.startUTC)) || !Number.isFinite(Date.parse(c.endUTC)) ||
        Date.parse(c.startUTC) >= Date.parse(c.endUTC)) errors.push(`Invalid window: ${c.id}`);
    if (c.geometryStatus === "spice-validated" && c.observationStatus === "campaign-window-only")
      errors.push(`Cannot validate SPICE geometry without exposure times: ${c.id}`);
  }
  return errors;
}
