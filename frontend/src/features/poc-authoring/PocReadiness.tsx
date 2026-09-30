import type { MissingInformationContract } from "../../shared/api/poc";

interface PocReadinessProps {
  markers: readonly MissingInformationContract[];
}

export function PocReadiness({ markers }: PocReadinessProps) {
  const ready = markers.length === 0;
  return (
    <section
      className={ready ? "poc-readiness poc-readiness--ready" : "poc-readiness"}
      aria-labelledby="poc-readiness-title"
      role="status"
    >
      <h2 id="poc-readiness-title">
        {ready ? "Ready for approval review" : "Approval readiness blocked"}
      </h2>
      {ready ? (
        <p>All required POC information is present. Approval is still required.</p>
      ) : (
        <>
          <p>Resolve {markers.length} named information gap{markers.length === 1 ? "" : "s"}.</p>
          <ul>
            {markers.map((marker) => (
              <li key={marker.marker_id}>{marker.required_fact}</li>
            ))}
          </ul>
        </>
      )}
    </section>
  );
}