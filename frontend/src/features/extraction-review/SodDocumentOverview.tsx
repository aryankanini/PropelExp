import { pointLevelFromLabel, structureSodText } from "./sodStructure";
import type { ReviewField } from "./types";

interface PocPoint {
  label: string;
  text: string;
  poc: string;
}

function parsePocPoints(value: string | null): readonly PocPoint[] | null {
  if (!value) return null;

  try {
    const parsed: unknown = JSON.parse(value);
    if (!Array.isArray(parsed)) return null;

    const points = parsed.filter(
      (item): item is PocPoint =>
        typeof item === "object" &&
        item !== null &&
        typeof item.label === "string" &&
        typeof item.text === "string" &&
        typeof item.poc === "string",
    );
    return points.length === parsed.length ? points : null;
  } catch {
    return null;
  }
}

interface SodDocumentOverviewProps {
  fields: readonly ReviewField[];
  selectedFieldId: string;
}

export function SodDocumentOverview({
  fields,
  selectedFieldId,
}: SodDocumentOverviewProps) {
  const field = fields.find((item) => item.fieldId === selectedFieldId) ?? fields[0];
  const current = field.revisions.find((revision) => revision.current);
  const sodBlocks = structureSodText(current?.value ?? "");
  const pocPoints = parsePocPoints(field.pocSuggestion);
  const pointCount = sodBlocks.filter((block) => block.kind === "point").length;

  return (
    <section className="deficiency-document" aria-labelledby="deficiency-document-title">
      <header className="deficiency-document__header">
        <div>
          <p className="eyebrow">Complete extraction</p>
          <h2 id="deficiency-document-title">
            {fields.length} {fields.length === 1 ? "deficiency" : "deficiencies"} found
          </h2>
        </div>
        <p>Select a tag from the case navigation to review its complete extraction.</p>
      </header>

      <article className="deficiency-record" aria-labelledby={`${field.fieldId}-overview-title`}>
        <header className="deficiency-record__header">
          <div>
            <span>ID tag</span>
            <h3 id={`${field.fieldId}-overview-title`}>{field.label}</h3>
          </div>
          <p>{field.evidenceItems.length} source {field.evidenceItems.length === 1 ? "page" : "pages"}</p>
        </header>

        <div className="deficiency-record__body">
          <section className="deficiency-record__sod" aria-labelledby={`${field.fieldId}-sod-title`}>
            <div className="deficiency-record__section-heading">
              <h4 id={`${field.fieldId}-sod-title`}>Statement of Deficiency</h4>
              {pointCount > 0 && <span>{pointCount} structured {pointCount === 1 ? "point" : "points"}</span>}
            </div>
            <div className="structured-sod">
              {sodBlocks.map((block, blockIndex) => {
                if (block.kind === "heading") {
                  return <h5 key={`${block.kind}-${blockIndex}`}>{block.text}</h5>;
                }
                if (block.kind === "point") {
                  return (
                    <div
                      key={`${block.kind}-${blockIndex}`}
                      className={`structured-sod__point structured-sod__point--level-${block.level}`}
                    >
                      <strong aria-hidden="true">{block.marker}</strong>
                      <p>{block.text}</p>
                    </div>
                  );
                }
                return <p key={`${block.kind}-${blockIndex}`}>{block.text}</p>;
              })}
            </div>
          </section>

          <section className="deficiency-record__poc" aria-labelledby={`${field.fieldId}-poc-title`}>
            <div className="deficiency-record__section-heading">
              <h4 id={`${field.fieldId}-poc-title`}>Suggested plan of correction</h4>
              <span>Draft</span>
            </div>
            {pocPoints ? (
              <div className="structured-sod">
                {pocPoints.map((point, pointIndex) => (
                  <div
                    key={`${point.label}-${pointIndex}`}
                    className={`structured-sod__point structured-sod__point--level-${pointLevelFromLabel(point.label)}`}
                  >
                    <strong aria-hidden="true">{point.label}</strong>
                    <p>{point.poc || "No corrective action needed."}</p>
                  </div>
                ))}
              </div>
            ) : field.pocSuggestion ? (
              <p>{field.pocSuggestion}</p>
            ) : (
              <p className="deficiency-record__empty">No POC extracted.</p>
            )}
          </section>
        </div>

        {field.evidenceItems.length > 0 && (
          <details className="extracted-evidence">
            <summary>View source evidence ({field.evidenceItems.length})</summary>
            <div className="extracted-evidence__list">
              {field.evidenceItems.map((evidence, evidenceIndex) => (
                <article key={`${evidence.pageNumber}-${evidenceIndex}`} className="extracted-evidence__item">
                  <span className="extracted-evidence__tag">Page {evidence.pageNumber}</span>
                  <p>{evidence.fullSnippet}</p>
                </article>
              ))}
            </div>
          </details>
        )}
      </article>
    </section>
  );
}