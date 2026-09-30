import { useEffect, useRef, useState } from "react";

import { apiUrl } from "../../shared/api/client";
import { EndSessionDialog } from "../../shared/session/EndSessionDialog";
import { RetentionStatus } from "../../shared/session/RetentionStatus";
import { useEndSession } from "../../shared/session/useEndSession";
import { useSessionStatus } from "../../shared/session/useSessionStatus";
import { useExtractionJob } from "../../shared/hooks/useExtractionJob";
import { useSession } from "../../app/SessionContext";
import { ChooseAnotherFileButton } from "./ChooseAnotherFileButton";
import { DocumentValidationStatus } from "./DocumentValidationStatus";
import { StageTimeline, type TimelineStage } from "./StageTimeline";
import { useDocumentUpload } from "./useDocumentUpload";
import "./document-intake.css";

const MAX_BYTES = 50 * 1024 * 1024;
const ACCEPTED_TYPES = [
  "application/pdf",
  "image/png",
  "image/jpeg",
  "image/tiff",
];

export function DocumentIntakePage() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [localError, setLocalError] = useState<string | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [jobId, setJobId] = useState<string | null>(null);
  const [noDeficienciesFound, setNoDeficienciesFound] = useState(false);

  const {
    sessionId,
    caseId,
    navigate,
    setCaseId,
    setJobId: setCtxJobId,
    reset: resetSession,
  } = useSession();

  const { state, upload, reset } = useDocumentUpload(sessionId);
  const sessionStatus = useSessionStatus(sessionId);
  const uploadedCaseId =
    state.status === "accepted"
      ? state.result.case_id
      : sessionStatus?.active_case_id ?? caseId;

  const cleanup = useEndSession(sessionId, uploadedCaseId);
  const jobState = useExtractionJob(jobId);

  useEffect(() => {
    if (!sessionStatus) return;
    if (sessionStatus.active_case_id && sessionStatus.active_case_id !== caseId) {
      setCaseId(sessionStatus.active_case_id);
    } else if (!sessionStatus.active_case_id && caseId) {
      resetSession();
    }
  }, [caseId, resetSession, sessionStatus, setCaseId]);

  useEffect(() => {
    if (jobState.status !== "completed" || !uploadedCaseId) return;

    const controller = new AbortController();
    fetch(apiUrl(`/api/v1/cases/${encodeURIComponent(uploadedCaseId)}`), {
      headers: { "X-Session-ID": sessionId },
      signal: controller.signal,
    })
      .then(async (response) => {
        if (!response.ok) throw new Error("Case projection unavailable");
        return response.json() as Promise<{ review_fields_count: number }>;
      })
      .then((projection) => {
        if (projection.review_fields_count > 0) {
          navigate("extraction-review");
        } else {
          setNoDeficienciesFound(true);
        }
      })
      .catch((error) => {
        if (!(error instanceof DOMException && error.name === "AbortError")) {
          setNoDeficienciesFound(true);
        }
      });

    return () => controller.abort();
  }, [jobState.status, navigate, sessionId, uploadedCaseId]);

  async function startExtractionJob(resolvedCaseId: string) {
    try {
      const response = await fetch(
        apiUrl(
          `/api/v1/cases/${encodeURIComponent(
            resolvedCaseId,
          )}/extraction-jobs`,
        ),
        {
          method: "POST",
          headers: {
            "X-Session-ID": sessionId,
          },
        },
      );

      if (response.ok) {
        const body = (await response.json()) as { job_id: string };
        setJobId(body.job_id);
        setCtxJobId(body.job_id);
      }
    } catch {
      // Extraction job start failed — user can retry.
    }
  }

  // After upload is accepted, start exactly one extraction job.
  useEffect(() => {
    if (state.status !== "accepted" || jobId) {
      return;
    }

    const resolvedCaseId = state.result.case_id;

    setCaseId(resolvedCaseId);
    void startExtractionJob(resolvedCaseId);
  }, [
    state.status,
    state.status === "accepted" ? state.result.case_id : null,
    jobId,
  ]);

  function selectFile(selected: File | null) {
    if (!selected) return;

    setFile(selected);
    reset();

    if (!ACCEPTED_TYPES.includes(selected.type)) {
      setLocalError("Select a PDF, PNG, JPEG, or TIFF document.");
      return;
    }

    if (selected.size > MAX_BYTES) {
      setLocalError("The file exceeds the 50 MB upload limit.");
      return;
    }

    setLocalError(null);
  }

  function chooseAnother() {
    setFile(null);
    setLocalError(null);
    setJobId(null);
    reset();

    if (inputRef.current) {
      inputRef.current.value = "";
    }

    inputRef.current?.focus();
  }

  async function handleUpload() {
    if (!file) return;
    upload(file);
  }

  async function confirmEndSession() {
    if (await cleanup.endSession()) {
      resetSession();
      chooseAnother();
      setDialogOpen(false);
    }
  }

  const rejection =
    localError ??
    (state.status === "rejected" ? state.problem.message : undefined);

  const stages: TimelineStage[] = [
    {
      id: "upload",
      label: "Upload",
      detail: "Document received and validated",
      status:
        state.status === "accepted" || jobId
          ? "complete"
          : state.status === "uploading"
            ? "active"
            : "pending",
    },
    {
      id: "extraction",
      label: "Extraction",
      detail: "Reading pages and identifying deficiencies",
      status:
        jobState.status === "completed"
          ? "complete"
          : jobState.status === "failed"
            ? "failed"
            : jobState.status === "running"
              ? "active"
              : "pending",
    },
    {
      id: "review",
      label: "Review ready",
      detail: "Deficiency candidates available for review",
      status: jobState.status === "completed" ? "complete" : "pending",
    },
  ];

  return (
    <div className="workspace-shell">
      <a className="skip-link" href="#document-intake">
        Skip to main content
      </a>

      <header className="app-header">
        <strong>CMS Deficiency Action Planner</strong>
        <span>Compliance reviewer</span>
      </header>

      <nav className="workflow-rail" aria-label="Case workflow">
        <div className="session-label">
          <strong>
            {uploadedCaseId ? "Active case" : "New working session"}
          </strong>
          <span>Session-only storage</span>
        </div>

        <ol>
          <li aria-current="step">
            <span>1</span>
            <div>
              Intake
              <small>Current</small>
            </div>
          </li>

          <li>
            <span>2</span>
            <div>
              Review
              <small>Unavailable</small>
            </div>
          </li>

          <li>
            <span>3</span>
            <div>
              POC drafts
              <small>Unavailable</small>
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

        {uploadedCaseId && (
          <button
            className="rail-action"
            type="button"
            onClick={() => setDialogOpen(true)}
          >
            End session
          </button>
        )}
      </nav>

      <main
        className="intake-content"
        id="document-intake"
        data-uxr="UXR-001 UXR-602"
      >
        <h1>Upload CMS-2567</h1>

        <p className="lede">
          Start one transient case by selecting a readable CMS-2567 PDF or
          image-based document.
        </p>

        <RetentionStatus
          sessionId={sessionId}
          active={uploadedCaseId !== null}
        />

        <DocumentValidationStatus
          accepted={state.status === "accepted" ? state.result : undefined}
          rejection={rejection}
          extractionStarted={jobState.status !== "idle"}
        />

        {jobId && (
          <section aria-label="Extraction progress">
            <StageTimeline stages={stages} />

            {jobState.status === "running" && (
              <p role="status">
                {jobState.stage === "generation"
                  ? "Generating structured results"
                  : jobState.stage === "ocr"
                    ? "Recognizing scanned pages"
                    : "Extracting document"}
                … {jobState.percent}% estimated
              </p>
            )}

            {jobState.status === "failed" && (
              <div role="alert">
                <p className="error-message">
                  {jobState.stage === "generation"
                    ? "AI processing failed. The uploaded case was retained."
                    : jobState.stage === "ocr"
                      ? "OCR failed. The uploaded case was retained."
                      : "Document extraction failed. The uploaded case was retained."}
                </p>
                <button
                  className="button button--secondary"
                  type="button"
                  onClick={async () => {
                    const caseToDelete = uploadedCaseId;
                    chooseAnother();
                    if (caseToDelete) {
                      await fetch(apiUrl(`/api/v1/cases/${caseToDelete}`), {
                        method: "DELETE",
                        headers: { "X-Session-ID": sessionId },
                      });
                    }
                  }}
                >
                  Start over
                </button>
              </div>
            )}

            {jobState.status === "completed" && noDeficienciesFound && (
              <p className="error-message" role="status">
                Extraction completed, but no deficiency records were found. End this session to upload another document.
              </p>
            )}
          </section>
        )}

        {!jobId && (
          <>
            {state.status === "uploading" ? (
              <section className="upload-progress" role="status">
                <strong>Uploading {file?.name}</strong>

                <progress value={state.progress} max="100">
                  {state.progress}%
                </progress>

                <span>{state.progress}%</span>
              </section>
            ) : null}

            <section
              className="upload-control"
              aria-labelledby="upload-title"
            >
              <h2 id="upload-title">Select survey document</h2>

              <p id="file-help">
                PDF, PNG, JPEG, or TIFF · up to 50 MB and 200 pages
              </p>

              <label className="button" htmlFor="cms-file">
                Select CMS-2567
              </label>

              <input
                ref={inputRef}
                id="cms-file"
                className="visually-hidden"
                type="file"
                accept=".pdf,.png,.jpg,.jpeg,.tif,.tiff"
                aria-describedby={`file-help${
                  rejection ? " file-error" : ""
                }`}
                onChange={(event) =>
                  selectFile(event.target.files?.[0] ?? null)
                }
              />

              {rejection ? (
                <span className="visually-hidden" id="file-error">
                  {rejection}
                </span>
              ) : null}
            </section>

            {file ? (
              <section
                className="selected-file"
                aria-label="Selected file"
              >
                <div>
                  <strong>{file.name}</strong>
                  <span>
                    {(file.size / 1048576).toFixed(1)} MB · Ready to validate
                  </span>
                </div>

                <div className="file-actions">
                  {rejection ? (
                    <ChooseAnotherFileButton onChoose={chooseAnother} />
                  ) : (
                    <button
                      className="button button--secondary"
                      type="button"
                      onClick={chooseAnother}
                    >
                      Remove
                    </button>
                  )}

                  <button
                    className="button"
                    type="button"
                    disabled={
                      state.status === "uploading" ||
                      Boolean(rejection) ||
                      state.status === "accepted"
                    }
                    onClick={() => void handleUpload()}
                  >
                    Upload CMS-2567
                  </button>
                </div>
              </section>
            ) : null}

            <section className="limits" aria-label="Upload limits">
              <div>
                <strong>Supported formats</strong>
                <span>PDF and image-based documents</span>
              </div>

              <div>
                <strong>Maximum size</strong>
                <span>50 MB per working session</span>
              </div>

              <div>
                <strong>Maximum length</strong>
                <span>200 pages before extraction</span>
              </div>
            </section>
          </>
        )}
      </main>

      <EndSessionDialog
        open={dialogOpen}
        pending={cleanup.status === "ending"}
        failed={cleanup.status === "failed"}
        onCancel={() => setDialogOpen(false)}
        onConfirm={() => void confirmEndSession()}
      />
    </div>
  );
}