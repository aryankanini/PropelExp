import type { GroundedClaimContract, SupportReference } from "../../shared/api/poc";

interface GroundedClaimProps {
  claim: GroundedClaimContract;
  onNavigate?: (reference: SupportReference) => void;
}

export function GroundedClaim({ claim, onNavigate }: GroundedClaimProps) {
  return (
    <div className="grounded-claim">
      <p>{claim.text}</p>
      <span>Supported by reviewed evidence:</span>
      <ul>
        {claim.support_references.map((reference) => (
          <li key={`${reference.kind}-${reference.reference_id}`}>
            <a
              href={`#support-${reference.kind}-${encodeURIComponent(reference.reference_id)}`}
              onClick={() => onNavigate?.(reference)}
            >
              {reference.kind === "evidence_span" ? "Evidence" : "Reviewed field"}{" "}
              {reference.reference_id}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}