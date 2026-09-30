export type StageStatus = "complete" | "active" | "failed" | "pending";

export interface TimelineStage {
  id: string;
  label: string;
  detail: string;
  status: StageStatus;
}

interface StageTimelineProps {
  stages: readonly TimelineStage[];
}

const statusLabels: Record<StageStatus, string> = {
  complete: "Complete",
  active: "Active",
  failed: "Failed",
  pending: "Pending",
};

export function StageTimeline({ stages }: StageTimelineProps) {
  return (
    <ol className="stage-timeline" aria-label="Processing stages" data-uxr="UXR-601">
      {stages.map((stage, index) => (
        <li
          className={`stage-timeline__item stage-timeline__item--${stage.status}`}
          key={stage.id}
          aria-current={stage.status === "active" ? "step" : undefined}
        >
          <span className="stage-timeline__marker" aria-hidden="true">{index + 1}</span>
          <div className="stage-timeline__copy">
            <strong>{stage.label}</strong>
            <p>{stage.detail}</p>
          </div>
          <span className="stage-timeline__status">{statusLabels[stage.status]}</span>
        </li>
      ))}
    </ol>
  );
}