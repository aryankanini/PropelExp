import { useRef, useState } from "react";

interface GeneratePocActionProps {
  confirmed: boolean;
  onGenerate: () => Promise<void>;
}

export function GeneratePocAction({
  confirmed,
  onGenerate,
}: GeneratePocActionProps) {
  const pendingRequest = useRef<Promise<void> | null>(null);
  const [pending, setPending] = useState(false);

  const generate = () => {
    if (!confirmed || pendingRequest.current !== null) {
      return;
    }
    setPending(true);
    const request = onGenerate().finally(() => {
      pendingRequest.current = null;
      setPending(false);
    });
    pendingRequest.current = request;
  };

  return (
    <div className="poc-generate">
      <button
        className="button"
        type="button"
        disabled={!confirmed || pending}
        onClick={generate}
        aria-describedby={!confirmed ? "generation-blocked-reason" : undefined}
      >
        {pending ? "Generating POC" : "Generate POC"}
      </button>
      {!confirmed && (
        <p id="generation-blocked-reason" className="poc-help" role="note">
          Confirm the current deficiency revision before generating a draft.
        </p>
      )}
      <span className="visually-hidden" role="status" aria-live="polite">
        {pending ? "Generating the five-part POC draft." : ""}
      </span>
    </div>
  );
}