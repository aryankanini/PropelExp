import { BadgeCheck, Bot, Pencil, ScanText } from "lucide-react";

import type { ContentOrigin } from "./types";

interface ProvenanceLabelProps {
  origin: ContentOrigin;
  revisionNumber: number;
  reapprovalRequired?: boolean;
}

const originIcons = {
  Extracted: ScanText,
  "AI-generated": Bot,
  "User-edited": Pencil,
  Approved: BadgeCheck,
} satisfies Record<ContentOrigin, typeof ScanText>;

export function ProvenanceLabel({
  origin,
  revisionNumber,
  reapprovalRequired = false,
}: ProvenanceLabelProps) {
  const Icon = originIcons[origin];

  return (
    <span className="provenance-label" data-origin={origin} data-uxr="UXR-103 UXR-502">
      <Icon aria-hidden="true" size={16} />
      <span>{origin}</span>
      <span>Revision {revisionNumber}</span>
      {reapprovalRequired ? <strong>Reapproval required</strong> : null}
    </span>
  );
}