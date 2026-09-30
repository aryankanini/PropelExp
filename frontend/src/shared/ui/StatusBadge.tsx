import { AlertTriangle, CheckCircle2, CircleDashed, RotateCcw } from "lucide-react";

type Status = "approved" | "awaiting" | "blocked" | "reapproval";

interface StatusBadgeProps {
  status: Status;
  label: string;
}

const icons = {
  approved: CheckCircle2,
  awaiting: CircleDashed,
  blocked: AlertTriangle,
  reapproval: RotateCcw,
};

export function StatusBadge({ status, label }: StatusBadgeProps) {
  const Icon = icons[status];
  return (
    <span className={`status-badge status-badge--${status}`}>
      <Icon aria-hidden="true" size={16} />
      {label}
    </span>
  );
}