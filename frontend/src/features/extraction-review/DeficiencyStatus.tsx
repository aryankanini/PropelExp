import { AlertTriangle, CheckCircle2, FilePenLine } from "lucide-react";

type DeficiencyState = "blocked" | "ready" | "confirmed";

interface DeficiencyStatusProps {
  state: DeficiencyState;
}

const statusContent = {
  blocked: { icon: AlertTriangle, label: "Confirmation blocked", detail: "POC generation unavailable" },
  ready: { icon: FilePenLine, label: "Ready to confirm", detail: "POC generation pending confirmation" },
  confirmed: { icon: CheckCircle2, label: "Confirmed", detail: "POC generation available" },
} satisfies Record<DeficiencyState, { icon: typeof AlertTriangle; label: string; detail: string }>;

export function DeficiencyStatus({ state }: DeficiencyStatusProps) {
  const content = statusContent[state];
  const Icon = content.icon;
  return (
    <div className={`deficiency-status deficiency-status--${state}`} data-uxr="UXR-502">
      <Icon aria-hidden="true" size={18} />
      <strong>{content.label}</strong>
      <span>{content.detail}</span>
    </div>
  );
}