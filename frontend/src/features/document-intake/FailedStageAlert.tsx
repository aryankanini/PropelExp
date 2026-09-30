import { mapTerminalFailure } from "../../shared/model/problem";
import { RecoveryError } from "../../shared/ui/RecoveryError";

interface FailedStageAlertProps {
  stage: string;
  pageNumbers?: readonly number[];
  retainedWork: string;
  correlationId: string;
  retryable: boolean;
  onRecovery: () => Promise<void> | void;
}

export function FailedStageAlert({
  stage,
  pageNumbers = [],
  retainedWork,
  correlationId,
  retryable,
  onRecovery,
}: FailedStageAlertProps) {
  const affectedPages =
    pageNumbers.length > 0 ? ` on pages ${pageNumbers.join("-")}` : "";
  const error = mapTerminalFailure(
    {
      operation: `${stage}${affectedPages}`,
      retainedWork,
      correlationId,
      retryable,
    },
    "The failed operation remains incomplete. Confirmed work has not changed.",
  );

  return <RecoveryError error={error} onAction={onRecovery} />;
}