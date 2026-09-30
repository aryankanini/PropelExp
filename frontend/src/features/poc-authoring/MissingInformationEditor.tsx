import type { MissingInformationContract } from "../../shared/api/poc";
import { pocSectionLabels } from "./pocSections";

interface MissingInformationEditorProps {
  marker: MissingInformationContract;
  value: string;
  disabled?: boolean;
  onChange: (value: string) => void;
}

export function MissingInformationEditor({
  marker,
  value,
  disabled = false,
  onChange,
}: MissingInformationEditorProps) {
  const inputId = `missing-information-${marker.marker_id}`;
  const helpId = `${inputId}-help`;
  return (
    <div className="missing-editor">
      <label htmlFor={inputId}>
        Supported replacement for {pocSectionLabels[marker.section]}
      </label>
      <textarea
        id={inputId}
        value={value}
        disabled={disabled}
        aria-describedby={helpId}
        onChange={(event) => onChange(event.target.value)}
      />
      <small id={helpId}>
        Enter only a fact supported by reviewed records. Clear this field to restore the marker.
      </small>
    </div>
  );
}