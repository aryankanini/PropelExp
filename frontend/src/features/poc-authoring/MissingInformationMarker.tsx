import type { MissingInformationContract } from "../../shared/api/poc";

interface MissingInformationMarkerProps {
  marker: MissingInformationContract;
}

export function MissingInformationMarker({ marker }: MissingInformationMarkerProps) {
  return (
    <aside className="missing-marker" aria-labelledby={`marker-${marker.marker_id}`}>
      <strong id={`marker-${marker.marker_id}`}>Information needed</strong>
      <p>{marker.required_fact}</p>
      <small>This is a required fact, not a generated facility claim.</small>
    </aside>
  );
}