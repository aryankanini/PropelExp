import type { ReactNode } from "react";

import styles from "./recovery.module.css";

interface AlertProps {
  title: string;
  children: ReactNode;
  correlationId?: string;
  action?: ReactNode;
  assertive?: boolean;
}

export function Alert({
  title,
  children,
  correlationId,
  action,
  assertive = false,
}: AlertProps) {
  return (
    <section
      className={styles.alert}
      role={assertive ? "alert" : "status"}
      data-uxr="UXR-601"
    >
      <h2 className={styles.title}>{title}</h2>
      <div className={styles.body}>{children}</div>
      {correlationId ? (
        <p className={styles.meta}>Correlation ID: {correlationId}</p>
      ) : null}
      {action ? <div className={styles.actions}>{action}</div> : null}
    </section>
  );
}