import { useState } from "react";
import {
  createPocApi,
  PocApiError,
  type PocApi,
  type PocDraft,
  type PocSectionName,
} from "../../shared/api/poc";
import { useSession } from "../../app/SessionContext";
import { EndSessionAction } from "../../shared/session/EndSessionAction";
import { GeneratePocAction } from "./GeneratePocAction";
import { PocDraftView } from "./PocDraftView";
import { PocValidationSummary } from "./PocValidationSummary";
import "./poc-authoring.css";

interface PocAuthoringPageProps {
  api?: PocApi;
  confirmed?: boolean;
}

export function PocAuthoringPage({ api, confirmed = true }: PocAuthoringPageProps) {
  const { sessionId, deficiencyId, caseId, navigate } = useSession();
  const resolvedDeficiencyId = deficiencyId ?? "deficiency-1";
  const resolvedApi = api ?? createPocApi(sessionId);

  const [draft, setDraft] = useState<PocDraft | null>(null);
  const [errors, setErrors] = useState<readonly string[]>([]);

  const generate = async () => {
    setErrors([]);
    try {
      setDraft(await resolvedApi.generate(resolvedDeficiencyId));
    } catch (error) {
      setDraft(null);
      setErrors([generationError(error)]);
    }
  };

  const save = async (
    expectedRevisionId: string,
    updates: Partial<Record<PocSectionName, string | null>>,
  ) => {
    const saved = await resolvedApi.save(resolvedDeficiencyId, expectedRevisionId, updates);
    setDraft(saved);
    return saved;
  };

  const reload = async () => {
    const current = await resolvedApi.load(resolvedDeficiencyId);
    setDraft(current);
    setErrors([]);
  };

  return (
    <div className="poc-shell">
      <a className="poc-skip-link" href="#poc-main">
        Skip to POC editor
      </a>
      <header className="poc-header">
        <strong>CMS Deficiency Action Planner</strong>
        <span>Compliance reviewer · Transient session</span>
      </header>
      <nav className="poc-rail" aria-label="Case workflow">
        <div className="poc-case">
          <strong>{caseId ?? "Active case"}</strong>
          <small>Current deficiency · {resolvedDeficiencyId}</small>
        </div>
        <ol>
          <li>
            <span>1</span>
            <div>
              Intake<small>Complete</small>
            </div>
          </li>
          <li>
            <span>2</span>
            <div>
              Review<small>Confirmed</small>
            </div>
          </li>
          <li aria-current="step">
            <span>3</span>
            <div>
              POC drafts<small>{draft ? "Editing" : "Available"}</small>
            </div>
          </li>
          <li>
            <span>4</span>
            <div>
              Approval and export<small>Blocked</small>
            </div>
          </li>
        </ol>
        <button
          className="rail-action"
          type="button"
          onClick={() => navigate("approval-export")}
          disabled={!draft}
        >
          Proceed to approval
        </button>
        <EndSessionAction className="button button--secondary poc-end-session" />
      </nav>
      <main id="poc-main" className="poc-main">
        {draft === null ? (
          <section className="poc-empty" aria-labelledby="poc-empty-title">
            <p className="poc-breadcrumb">POC drafts / {resolvedDeficiencyId}</p>
            <h1 id="poc-empty-title">Plan of Correction</h1>
            <p>No POC draft exists for this deficiency.</p>
            <GeneratePocAction confirmed={confirmed} onGenerate={generate} />
            <PocValidationSummary errors={errors} />
          </section>
        ) : (
          <PocDraftView draft={draft} onSave={save} onReload={reload} />
        )}
      </main>
    </div>
  );
}

function generationError(error: unknown): string {
  if (error instanceof PocApiError) {
    return `${error.problem.message} Correlation ID: ${error.problem.correlation_id}.`;
  }
  if (error instanceof Error) {
    return error.message;
  }
  return "The generated response could not be validated.";
}
