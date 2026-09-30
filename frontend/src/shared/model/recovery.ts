export type RecoveryAction =
  | { kind: "retry"; label: "Retry failed operation" }
  | { kind: "replace"; label: "Replace document" }
  | { kind: "retry-later"; label: "Retry later" }
  | { kind: "return"; label: "Return to reviewed work" };

export interface RecoveryContext {
  retryable: boolean;
  replacementRequired: boolean;
  providerExhausted: boolean;
}

export function selectRecoveryAction(context: RecoveryContext): RecoveryAction {
  if (context.replacementRequired) {
    return { kind: "replace", label: "Replace document" };
  }
  if (context.retryable && !context.providerExhausted) {
    return { kind: "retry", label: "Retry failed operation" };
  }
  if (context.retryable) {
    return { kind: "retry-later", label: "Retry later" };
  }
  return { kind: "return", label: "Return to reviewed work" };
}