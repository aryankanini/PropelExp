import { History } from "lucide-react";

import type { RevisionEntry } from "../../shared/model/approval";

export function RevisionHistory({ entries }: { entries: RevisionEntry[] }) {
  return (
    <aside className="revision-history" aria-labelledby="revision-history-title">
      <h2 id="revision-history-title"><History aria-hidden="true" /> Revision history</h2>
      <ol>
        {entries.map((entry) => (
          <li key={entry.revisionId}>
            <div><strong>{entry.revisionId}</strong>{entry.current ? <span>Current</span> : null}</div>
            <p>{entry.summary}</p>
            <small>{entry.author} · {entry.timestamp}</small>
          </li>
        ))}
      </ol>
    </aside>
  );
}