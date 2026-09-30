import { useEffect, useState } from "react";
import {
  PocApiError,
  pocSectionOrder,
  type MissingInformationContract,
  type PocContent,
  type PocDraft,
  type PocSectionName,
} from "../../shared/api/poc";
import { GroundedClaim } from "./GroundedClaim";
import { MissingInformationEditor } from "./MissingInformationEditor";
import { MissingInformationMarker } from "./MissingInformationMarker";
import { PocReadiness } from "./PocReadiness";
import { PocSaveStatus, type SaveState } from "./PocSaveStatus";
import { PocSection } from "./PocSection";
import { pocSectionLabels } from "./pocSections";

interface PocEditorProps {
  draft: PocDraft;
  onSave: (
    expectedRevisionId: string,
    updates: Partial<Record<PocSectionName, string | null>>,
  ) => Promise<PocDraft>;
  onReload: () => Promise<void>;
}

export function PocEditor({ draft, onSave, onReload }: PocEditorProps) {
  const revision = draft.revisions.at(-1);
  if (revision === undefined) {
    throw new Error("A POC draft requires a current revision.");
  }
  const [values, setValues] = useState<PocContent>(() => editableContent(draft));
  const [saveState, setSaveState] = useState<SaveState>({ kind: "idle" });

  useEffect(() => {
    setValues(editableContent(draft));
    setSaveState({ kind: "idle" });
  }, [draft, draft.current_revision_id]);

  const knownMarkers = latestMarkers(draft);
  const updates = changedValues(draft, values, knownMarkers);
  const hasChanges = Object.keys(updates).length > 0;
  const hasInvalidEmpty = pocSectionOrder.some(
    (name) => values[name].trim().length === 0 && knownMarkers[name] === undefined,
  );

  const save = async () => {
    if (!hasChanges || hasInvalidEmpty || saveState.kind === "saving") {
      return;
    }
    setSaveState({ kind: "saving" });
    try {
      const savedDraft = await onSave(draft.current_revision_id, updates);
      setSaveState({ kind: "saved", revisionId: savedDraft.current_revision_id });
    } catch (error) {
      if (error instanceof PocApiError && error.problem.code === "stale_revision") {
        setSaveState({ kind: "conflict", message: error.problem.message });
        return;
      }
      setSaveState({
        kind: "failed",
        message: error instanceof Error ? error.message : "The draft could not be saved.",
        correlationId: error instanceof PocApiError ? error.problem.correlation_id : undefined,
      });
    }
  };

  return (
    <form
      className="poc-editor"
      onSubmit={(event) => {
        event.preventDefault();
        void save();
      }}
    >
      <PocReadiness markers={revision.missing_information} />
      {pocSectionOrder.map((name, index) => {
        const marker = revision.missing_information.find((item) => item.section === name);
        const claims = revision.grounded_claims.filter((claim) => claim.section === name);
        return (
          <PocSection
            key={name}
            index={index + 1}
            name={name}
            origin={revision.section_origins[name]}
          >
            {marker ? (
              <>
                <MissingInformationMarker marker={marker} />
                <MissingInformationEditor
                  marker={marker}
                  value={values[name]}
                  disabled={saveState.kind === "saving"}
                  onChange={(value) => setValues((current) => ({ ...current, [name]: value }))}
                />
              </>
            ) : (
              <div className="poc-field">
                <label htmlFor={`poc-${name}`}>{pocSectionLabels[name]}</label>
                <textarea
                  id={`poc-${name}`}
                  value={values[name]}
                  required={knownMarkers[name] === undefined}
                  disabled={saveState.kind === "saving"}
                  onChange={(event) =>
                    setValues((current) => ({ ...current, [name]: event.target.value }))
                  }
                />
              </div>
            )}
            {claims.map((claim) => (
              <GroundedClaim key={`${name}-${claim.text}`} claim={claim} />
            ))}
          </PocSection>
        );
      })}
      {hasInvalidEmpty && (
        <p className="poc-inline-error" role="alert">
          Required sections cannot be empty.
        </p>
      )}
      <PocSaveStatus
        state={saveState}
        onRetry={() => void save()}
        onReload={() => void onReload()}
      />
      <div className="poc-actions">
        <span>{draft.revisions.length} retained revision{draft.revisions.length === 1 ? "" : "s"}</span>
        <button
          className="button"
          type="submit"
          disabled={!hasChanges || hasInvalidEmpty || saveState.kind === "saving"}
        >
          {saveState.kind === "saving" ? "Saving draft" : "Save revision"}
        </button>
      </div>
    </form>
  );
}

function editableContent(draft: PocDraft): PocContent {
  const revision = draft.revisions.at(-1);
  if (revision === undefined) {
    throw new Error("A POC draft requires a current revision.");
  }
  const markerSections = new Set(revision.missing_information.map((marker) => marker.section));
  return Object.fromEntries(
    pocSectionOrder.map((name) => [name, markerSections.has(name) ? "" : revision.content[name]]),
  ) as unknown as PocContent;
}

function latestMarkers(
  draft: PocDraft,
): Partial<Record<PocSectionName, MissingInformationContract>> {
  const markers: Partial<Record<PocSectionName, MissingInformationContract>> = {};
  for (const revision of [...draft.revisions].reverse()) {
    for (const marker of revision.missing_information) {
      markers[marker.section] ??= marker;
    }
  }
  return markers;
}

function changedValues(
  draft: PocDraft,
  values: PocContent,
  knownMarkers: Partial<Record<PocSectionName, MissingInformationContract>>,
): Partial<Record<PocSectionName, string | null>> {
  const revision = draft.revisions.at(-1);
  if (revision === undefined) {
    return {};
  }
  const currentMarkerSections = new Set(
    revision.missing_information.map((marker) => marker.section),
  );
  const updates: Partial<Record<PocSectionName, string | null>> = {};
  for (const name of pocSectionOrder) {
    const value = values[name].trim();
    if (value.length === 0 && knownMarkers[name] !== undefined) {
      if (!currentMarkerSections.has(name)) {
        updates[name] = null;
      }
    } else if (currentMarkerSections.has(name) || value !== revision.content[name]) {
      updates[name] = value;
    }
  }
  return updates;
}