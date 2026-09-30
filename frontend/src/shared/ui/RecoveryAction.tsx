import { useState } from "react";

import type { RecoveryAction as RecoveryActionModel } from "../model/recovery";
import styles from "./recovery.module.css";

interface RecoveryActionProps {
  action: RecoveryActionModel;
  onAction: (action: RecoveryActionModel) => Promise<void> | void;
}

export function RecoveryAction({ action, onAction }: RecoveryActionProps) {
  const [isActive, setIsActive] = useState(false);

  async function submitAction() {
    if (isActive) {
      return;
    }
    setIsActive(true);
    try {
      await onAction(action);
    } finally {
      setIsActive(false);
    }
  }

  return (
    <button
      className={styles.action}
      disabled={isActive}
      type="button"
      onClick={submitAction}
    >
      {isActive ? "Recovery in progress" : action.label}
    </button>
  );
}