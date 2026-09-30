import { StatusBadge } from "../../shared/ui/StatusBadge";

interface ReapprovalStatusProps {
  status: "editing" | "unapproved" | "reapproval_required" | "approved";
}

export function ReapprovalStatus({ status }: ReapprovalStatusProps) {
  if (status === "approved") return <StatusBadge status="approved" label="Approved" />;
  if (status === "reapproval_required") return <StatusBadge status="reapproval" label="Reapproval required" />;
  return <StatusBadge status="awaiting" label={status === "editing" ? "Editing" : "Awaiting approval"} />;
}