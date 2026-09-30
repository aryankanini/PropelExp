import { Copy, RotateCw } from "lucide-react";

import { Modal } from "../../shared/ui/Modal";

interface ExportFailureModalProps {
  open: boolean;
  onClose: () => void;
  onRetry: () => void;
  onCopy: () => void;
}

export function ExportFailureModal({ open, onClose, onRetry, onCopy }: ExportFailureModalProps) {
  return (
    <Modal open={open} title="Download formatting failed" onClose={onClose} actions={<><button className="button button--secondary" type="button" onClick={onCopy}><Copy aria-hidden="true" /> Copy draft</button><button className="button" type="button" onClick={onRetry}><RotateCw aria-hidden="true" /> Retry download</button></>}>
      <p>Your approval remains valid. Retry the local download or copy the labeled draft instead.</p>
    </Modal>
  );
}