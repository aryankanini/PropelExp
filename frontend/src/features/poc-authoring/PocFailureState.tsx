import { mapTerminalFailure } from "../../shared/model/problem";
import { RecoveryError } from "../../shared/ui/RecoveryError";

interface PocFailureStateProps {
  correlationId: string;
  retainedRevision: string;
  providerExhausted?: boolean;
  onRecovery: () => Promise<void> | void;
}

export function PocFailureState({
  correlationId,
  retainedRevision,
  providerExhausted = false,
  onRecovery,
}: PocFailureStateProps) {
  const error = mapTerminalFailure(
    {
      operation: "POC generation",
      retainedWork: retainedRevision,
      correlationId,
      retryable: true,
      providerExhausted,
    },
    "The five-section response could not be completed. Reviewed deficiency data remains unchanged.",
  );

  return <RecoveryError error={error} onAction={onRecovery} />;
}