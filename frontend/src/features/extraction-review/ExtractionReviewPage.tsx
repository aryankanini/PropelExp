import { useEffect, useState } from "react";

import { apiUrl } from "../../shared/api/client";
import { useSession } from "../../app/SessionContext";
import { EndSessionDialog } from "../../shared/session/EndSessionDialog";
import { useEndSession } from "../../shared/session/useEndSession";
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

  const [loadState, setLoadState] = useState<LoadState>("loading");
  const [fields, setFields] = useState<ReviewField[]>([]);
  const [selectedFieldIndex, setSelectedFieldIndex] = useState(0);
  const [endSessionOpen, setEndSessionOpen] = useState(false);
  const [confirmationState, setConfirmationState] = useState<
    "idle" | "pending" | "error"
  >("idle");

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
    if (!field) return;
    setConfirmationState("pending");
    const selectedDeficiencyFields = deficiencyFields.filter(
      (item) => item.deficiencyId === field.deficiencyId,
    );

    try {
      const response = await fetch(
        apiUrl(
          `/sessions/${encodeURIComponent(sessionId)}/deficiencies/${encodeURIComponent(
            field.deficiencyId,
          )}/confirmation`,
        ),
        {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            deficiency_id: field.deficiencyId,
            expected_revisions: selectedDeficiencyFields.map((item) => ({
              field_id: item.fieldId,
              revision_id: item.currentRevisionId,
            })),
          }),
        },
      );
      if (!response.ok) throw new Error("Confirmation failed");
      const outcome = (await response.json()) as {
        poc_generation_eligible: boolean;
      };
      if (!outcome.poc_generation_eligible) {
        setConfirmationState("error");
        return;
      }
      setDeficiencyId(field.deficiencyId);
      navigate("poc-authoring");
    } catch {
      setConfirmationState("error");
    }
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
            disabled={field.unresolved || confirmationState === "pending"}
            onClick={() => void confirmAndContinue()}
          >
            {confirmationState === "pending"
              ? "Confirming..."
              : "Confirm and continue to POC"}
          </button>
        </div>

        {confirmationState === "error" && (
          <p className="dialog-error" role="alert">
            This deficiency could not be confirmed. Resolve incomplete values and try again.
          </p>
        )}

        <SodDocumentOverview
          fields={deficiencyFields}
          selectedFieldId={field.fieldId}
        />
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