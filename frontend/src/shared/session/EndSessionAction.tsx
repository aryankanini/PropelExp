import { useState } from "react";

import { useSession } from "../../app/SessionContext";
import { EndSessionDialog } from "./EndSessionDialog";
import { useEndSession } from "./useEndSession";

interface EndSessionActionProps {
  className?: string;
}

export function EndSessionAction({ className = "rail-action" }: EndSessionActionProps) {
  const { sessionId, caseId, navigate, reset } = useSession();
  const cleanup = useEndSession(sessionId, caseId);
  const [dialogOpen, setDialogOpen] = useState(false);

  if (!caseId) return null;

  async function confirmEndSession() {
    if (await cleanup.endSession()) {
      reset();
      setDialogOpen(false);
      navigate("intake");
    }
  }

  return (
    <>
      <button className={className} type="button" onClick={() => setDialogOpen(true)}>
        End session
      </button>
      <EndSessionDialog
        open={dialogOpen}
        pending={cleanup.status === "ending"}
        failed={cleanup.status === "failed"}
        onCancel={() => setDialogOpen(false)}
        onConfirm={() => void confirmEndSession()}
      />
    </>
  );
}