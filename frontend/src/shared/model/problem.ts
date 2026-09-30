import { selectRecoveryAction, type RecoveryAction } from "./recovery";

export interface SafeProblem {
  code: string;
  message: string;
  correlation_id: string;
  retryable: boolean;
}

export interface TerminalFailure {
  operation: string;
  retainedWork: string;
  correlationId: string;
  retryable: boolean;
  replacementRequired?: boolean;
  providerExhausted?: boolean;
}

export interface RecoveryErrorViewModel {
  title: string;
  message: string;
  operation: string;
  retainedWork: string;
  correlationId: string;
  retryable: boolean;
  action: RecoveryAction;
}

export function mapTerminalFailure(
  failure: TerminalFailure,
  message: string,
): RecoveryErrorViewModel {
  return {
    title: `${failure.operation} failed`,
    message,
    operation: failure.operation,
    retainedWork: failure.retainedWork,
    correlationId: failure.correlationId,
    retryable: failure.retryable,
    action: selectRecoveryAction({
      retryable: failure.retryable,
      replacementRequired: failure.replacementRequired ?? false,
      providerExhausted: failure.providerExhausted ?? false,
    }),
  };
}

export function mapSafeProblem(
  problem: SafeProblem,
  operation: string,
  retainedWork: string,
): RecoveryErrorViewModel {
  return mapTerminalFailure(
    {
      operation,
      retainedWork,
      correlationId: problem.correlation_id,
      retryable: problem.retryable,
    },
    problem.message,
  );
}