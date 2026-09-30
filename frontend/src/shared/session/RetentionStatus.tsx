import { useSessionStatus } from "./useSessionStatus";

interface RetentionStatusProps {
  sessionId: string;
  active: boolean;
}

export function RetentionStatus({ sessionId, active }: RetentionStatusProps) {
  const status = useSessionStatus(sessionId, active);
  const minutes = status ? Math.ceil(status.remaining_inactivity_seconds / 60) : 60;

  return (
    <div className="retention-status" role="note" data-uxr="UXR-001">
      <strong>Session-only data.</strong>{" "}
      {active
        ? minutes > 0
          ? `This case expires after approximately ${minutes} minutes without activity.`
          : "This case is expiring now. End the session before starting another upload."
        : "Uploaded files and case work are removed when this session ends or after 60 minutes without activity."}
    </div>
  );
}