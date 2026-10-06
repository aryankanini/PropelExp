export type SaveState =
  | { kind: "idle" }
  | { kind: "saving" }
  | { kind: "saved"; revisionId: string }
  | { kind: "failed"; message: string; correlationId?: string }
  | { kind: "conflict"; message: string };

interface PocSaveStatusProps {
  state: SaveState;
  onRetry: () => void;
  onReload: () => void;
}

export function PocSaveStatus({ state, onRetry, onReload }: PocSaveStatusProps) {
  if (state.kind === "idle") {
    return null;
  }
  if (state.kind === "saving") {
    return <p className="poc-save-status" role="status">Saving current revision.</p>;
  }
  if (state.kind === "saved") {
    return (
      <p className="poc-save-status poc-save-status--success" role="status">
        Saved as an unapproved revision.
      </p>
    );
  }
  if (state.kind === "conflict") {
    return (
      <div className="poc-save-status poc-save-status--error" role="alert">
        <strong>Newer draft available</strong>
        <p>{state.message} Your local edits have not overwritten it.</p>
        <button className="button button--secondary" type="button" onClick={onReload}>
          Reload current draft
        </button>
      </div>
    );
  }
  return (
    <div className="poc-save-status poc-save-status--error" role="alert">
      <strong>Draft was not saved</strong>
      <p>{state.message} Your local edits are retained.</p>
      <button className="button button--secondary" type="button" onClick={onRetry}>
        Retry save
      </button>
    </div>
  );
}