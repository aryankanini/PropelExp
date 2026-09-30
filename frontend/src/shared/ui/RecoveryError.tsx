import type { RecoveryErrorViewModel } from "../model/problem";
import { Alert } from "./Alert";
import { RecoveryAction } from "./RecoveryAction";

interface RecoveryErrorProps {
  error: RecoveryErrorViewModel;
  onAction: () => Promise<void> | void;
}

export function RecoveryError({ error, onAction }: RecoveryErrorProps) {
  return (
    <Alert
      assertive
      title={error.title}
      correlationId={error.correlationId}
      action={
        <RecoveryAction action={error.action} onAction={onAction} />
      }
    >
      <p>{error.message}</p>
      <p>
        <strong>Affected operation:</strong> {error.operation}
      </p>
      <p>
        <strong>Retained work:</strong> {error.retainedWork}
      </p>
      <p>
        <strong>Retryable:</strong> {error.retryable ? "Yes" : "No"}
      </p>
    </Alert>
  );
}