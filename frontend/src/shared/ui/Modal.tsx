import { useEffect, useRef, type ReactNode } from "react";
import { X } from "lucide-react";

interface ModalProps {
  open: boolean;
  title: string;
  children: ReactNode;
  actions: ReactNode;
  onClose: () => void;
}

export function Modal({ open, title, children, actions, onClose }: ModalProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (open && !dialog?.open) dialog?.showModal();
    if (!open && dialog?.open) dialog.close();
  }, [open]);

  return (
    <dialog
      ref={dialogRef}
      className="recovery-modal"
      aria-labelledby="recovery-modal-title"
      onCancel={(event) => {
        event.preventDefault();
        onClose();
      }}
    >
      <div className="modal-heading">
        <h2 id="recovery-modal-title">{title}</h2>
        <button className="icon-button" type="button" onClick={onClose} aria-label="Close dialog">
          <X aria-hidden="true" />
        </button>
      </div>
      {children}
      <div className="modal-actions">{actions}</div>
    </dialog>
  );
}