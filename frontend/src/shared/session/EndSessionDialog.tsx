import { useEffect, useRef } from "react";

interface EndSessionDialogProps {
  open: boolean;
  pending: boolean;
  failed: boolean;
  onCancel: () => void;
  onConfirm: () => void;
}

export function EndSessionDialog({
  open,
  pending,
  failed,
  onCancel,
  onConfirm,
}: EndSessionDialogProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (open && !dialog?.open) dialog?.showModal();
    if (!open && dialog?.open) dialog.close();
  }, [open]);

  return (
    <dialog
      ref={dialogRef}
      className="end-session-dialog"
      aria-labelledby="end-session-title"
      aria-describedby="end-session-description"
      onCancel={(event) => {
        event.preventDefault();
        onCancel();
      }}
      data-uxr="UXR-602"
    >
      <h2 id="end-session-title">End transient session?</h2>
      <p id="end-session-description">
        The uploaded document, extraction results, edits, drafts, and approvals
        will be permanently removed from this device.
      </p>
      {failed ? (
        <p className="dialog-error" role="alert">
          Cleanup could not be verified. The case remains available. Try again.
        </p>
      ) : null}
      <div className="dialog-actions">
        <button className="button button--secondary" type="button" onClick={onCancel} disabled={pending}>
          Cancel
        </button>
        <button className="button" type="button" onClick={onConfirm} disabled={pending}>
          {pending ? "Removing data..." : failed ? "Try cleanup again" : "End session and remove data"}
        </button>
      </div>
    </dialog>
  );
}