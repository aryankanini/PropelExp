import type { ReactNode } from "react";
import type { PocSectionName, SectionOrigin } from "../../shared/api/poc";
import { pocSectionLabels } from "./pocSections";

interface PocSectionProps {
  index: number;
  name: PocSectionName;
  origin: SectionOrigin;
  children: ReactNode;
}

export function PocSection({ index, name, origin, children }: PocSectionProps) {
  const headingId = `poc-section-${name}`;
  return (
    <section className="poc-section" aria-labelledby={headingId}>
      <div className="poc-section__heading">
        <h2 id={headingId}>{index}. {pocSectionLabels[name]}</h2>
        <span className={`poc-origin poc-origin--${origin}`}>
          {origin === "user_edited" ? "User-edited" : "AI-generated"}
        </span>
      </div>
      {children}
    </section>
  );
}