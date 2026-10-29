import { useEffect, useState } from "react";

import { apiUrl } from "../../shared/api/client";
import { useSession } from "../../app/SessionContext";
import { EndSessionDialog } from "../../shared/session/EndSessionDialog";
import { useEndSession } from "../../shared/session/useEndSession";
import {
  createPocApi,
  PocApiError,
  type PocDraft,
  type PocSectionName,
} from "../../shared/api/poc";
import { PocDraftView } from "../poc-authoring/PocDraftView";
import { SodDocumentOverview } from "./SodDocumentOverview";
import type { ReviewField } from "./types";
import { projectReviewField } from "./types";
import "./extraction-review.css";

type LoadState = "loading" | "ready" | "error";

export function ExtractionReviewPage() {
  const {
    sessionId,
    caseId,
    navigate,
    setDeficiencyId,
    reset: resetSession,
  } = useSession();
  const cleanup = useEndSession(sessionId, caseId);
  const pocApi = createPocApi(sessionId);

  const [loadState, setLoadState] = useState<LoadState>("loading");
  const [fields, setFields] = useState<ReviewField[]>([]);
  const [selectedFieldIndex, setSelectedFieldIndex] = useState(0);
  const [endSessionOpen, setEndSessionOpen] = useState(false);
  const [draft, setDraft] = useState<PocDraft | null>(null);
  const [confirmationState, setConfirmationState] = useState<
    "idle" | "pending" | "error"
  >("idle");
  const [confirmationError, setConfirmationError] = useState("");

  useEffect(() => {
    if (!sessionId) return;

    const controller = new AbortController();

    fetch(apiUrl(`/sessions/${encodeURIComponent(sessionId)}/review`), {
      headers: { "X-Session-ID": sessionId },
      signal: controller.signal,
    })
      .then(async (res) => {
        if (!res.ok) throw new Error("Failed to load review fields");

        const raw = (await res.json()) as unknown[];
        const projected = raw.map(projectReviewField);

        setFields(projected);

        setLoadState("ready");
      })
      .catch((error) => {
        if (error instanceof DOMException && error.name === "AbortError") {
          return;
        }

        setLoadState("error");
      });

    return () => controller.abort();
  }, [sessionId]);

  const providerFields = fields.filter((item) => item.fieldType === "provider");
  const deficiencyFields = fields.filter((item) => item.fieldType === "sod");
  const field = deficiencyFields[selectedFieldIndex] ?? null;

  function selectField(fieldIndex: number) {
    const nextField = deficiencyFields[fieldIndex];
    if (!nextField) return;
    setSelectedFieldIndex(fieldIndex);
  }

  async function handleStartOver() {
    const cleanedUp = await cleanup.endSession();

    if (!cleanedUp) {
      return;
    }

    resetSession();
    navigate("intake");
  }

  async function confirmEndSession() {
    if (await cleanup.endSession()) {
      resetSession();
      setEndSessionOpen(false);
      navigate("intake");
    }
  }

  async function confirmAndContinue() {
    if (!field || deficiencyFields.some((item) => item.unresolved)) return;
    setConfirmationState("pending");
    setConfirmationError("");

    try {
      const deficiencyIds = [
        ...new Set(deficiencyFields.map((item) => item.deficiencyId)),
      ];
      for (const deficiencyId of deficiencyIds) {
        const matchingFields = deficiencyFields.filter(
          (item) => item.deficiencyId === deficiencyId,
        );
        const response = await fetch(
          apiUrl(
            `/sessions/${encodeURIComponent(sessionId)}/deficiencies/${encodeURIComponent(
              deficiencyId,
            )}/confirmation`,
          ),
          {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              deficiency_id: deficiencyId,
              expected_revisions: matchingFields.map((item) => ({
                field_id: item.fieldId,
                revision_id: item.currentRevisionId,
              })),
            }),
          },
        );
        if (!response.ok) {
          const problem = await response.json() as {
            detail?: { message?: string };
            message?: string;
          };
          throw new Error(
            problem.detail?.message
              ?? problem.message
              ?? "The extracted values could not be confirmed.",
          );
        }
      }
      setDeficiencyId(field.deficiencyId);
      try {
        setDraft(await pocApi.generate(field.deficiencyId));
      } catch (error) {
        throw new Error(
          error instanceof PocApiError
            ? `${error.problem.message} Your confirmations were saved; retry generation.`
            : "POC generation failed. Your confirmations were saved; retry generation.",
        );
      }
      setConfirmationState("idle");
    } catch (error) {
      setConfirmationError(
        error instanceof Error
          ? error.message
          : "The document could not be generated.",
      );
      setConfirmationState("error");
    }
  }

  async function savePoc(
    deficiencyId: string,
    expectedRevisionId: string,
    updates: Partial<Record<PocSectionName, string | null>>,
  ) {
    const saved = await pocApi.save(deficiencyId, expectedRevisionId, updates);
    setDraft(saved);
    return saved;
  }

  if (loadState === "loading") {
    return (
      <div className="review-shell">
        <main className="review-main" id="review-main" aria-busy="true">
          <p>Loading extraction results…</p>
        </main>
      </div>
    );
  }

  if (loadState === "error" || !field) {
    return (
      <div className="review-shell">
        <main className="review-main" id="review-main">
          <p role="alert">
            {loadState === "error"
              ? "Could not load review fields. Please try again."
              : "No deficiencies were found in this document."}
          </p>

          <button
            className="button"
            type="button"
            onClick={() => void handleStartOver()}
            disabled={cleanup.status === "ending"}
          >
            {cleanup.status === "ending"
              ? "Removing data..."
              : "Start over"}
          </button>

          {cleanup.status === "failed" && (
            <p className="dialog-error" role="alert">
              Cleanup could not be verified. The case remains available. Try
              again.
            </p>
          )}
        </main>
      </div>
    );
  }

  return (
    <div className="review-shell">
      <a className="skip-link" href="#review-main">
        Skip to review
      </a>

      <header className="app-header">
        <strong>CMS Deficiency Action Planner</strong>
        <span>Review</span>
      </header>

      <nav className="workflow-rail" aria-label="Case workflow">
        <div className="session-label">
          <strong>Active case</strong>
          <span>
            {fields.filter((f) => f.unresolved).length} values need review
          </span>
        </div>

        <ol>
          <li>
            <span>1</span>
            <div>
              Intake
              <small>Complete</small>
            </div>
          </li>

          <li aria-current="step">
            <span>2</span>
            <div>
              Review
              <small>Current</small>
            </div>
          </li>

          <li>
            <span>3</span>
            <div>
              POC drafts
              <small>
                {field.unresolved ? "Blocked" : "Pending confirmation"}
              </small>
            </div>
          </li>

          <li>
            <span>4</span>
            <div>
              Approval and export
              <small>Unavailable</small>
            </div>
          </li>
        </ol>

        {deficiencyFields.length > 1 && (
          <div className="deficiency-index" aria-label="Extracted deficiency tags">
            {deficiencyFields.map((f, i) => (
              <button
                key={f.fieldId}
                className={`button button--secondary${
                  i === selectedFieldIndex ? " button--active" : ""
                }`}
                type="button"
                aria-pressed={i === selectedFieldIndex}
                onClick={() => selectField(i)}
              >
                {f.label}
              </button>
            ))}
          </div>
        )}

        <button
          className="rail-action"
          type="button"
          onClick={() => setEndSessionOpen(true)}
        >
          End session
        </button>
      </nav>

      <main className="review-main" id="review-main">
        {providerFields.length > 0 && (
          <section className="provider-summary" aria-labelledby="provider-summary-title">
            <h2 id="provider-summary-title">Provider</h2>
            <dl>
              {providerFields.map((providerField) => (
                <div key={providerField.fieldId}>
                  <dt>{providerField.label}</dt>
                  <dd>
                    {providerField.revisions.find((revision) => revision.current)?.value ?? "Not extracted"}
                  </dd>
                </div>
              ))}
            </dl>
          </section>
        )}

        <div className="review-heading">
          <div>
            <p className="breadcrumb">Review / Extracted document</p>
            <h1>Extracted deficiencies</h1>
            <p>Review every F-tag and its complete Statement of Deficiency.</p>
          </div>
          <button
            className="button"
            type="button"
            disabled={
              deficiencyFields.some((item) => item.unresolved)
              || confirmationState === "pending"
              || draft !== null
            }
            onClick={() => void confirmAndContinue()}
          >
            {confirmationState === "pending"
              ? "Generating one combined POC..."
              : draft
                ? "POC generated below"
                : "Confirm all SODs and generate POC"}
          </button>
        </div>

        {confirmationState === "error" && (
          <p className="dialog-error" role="alert">
            {confirmationError}
          </p>
        )}

        <SodDocumentOverview
          fields={deficiencyFields}
          selectedFieldId={field.fieldId}
        />
        {draft && (
          <>
            <PocDraftView
              draft={draft}
              onSave={savePoc}
              onReload={async () => setDraft(await pocApi.load(field.deficiencyId))}
            />
            <button
              className="button"
              type="button"
              onClick={() => navigate("poc-authoring")}
            >
              Continue to POC draft
            </button>
          </>
        )}
      </main>

      <EndSessionDialog
        open={endSessionOpen}
        pending={cleanup.status === "ending"}
        failed={cleanup.status === "failed"}
        onCancel={() => setEndSessionOpen(false)}
        onConfirm={() => void confirmEndSession()}
      />
    </div>
  );
}