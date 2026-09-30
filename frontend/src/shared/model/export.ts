export type ExportFormat = "copy" | "download";

export interface ExportResult {
  format: ExportFormat;
  content: string;
  media_type: string;
  filename: string | null;
}

export interface ExportFailure {
  code: "formatting_failed";
  message: string;
  retry_available: true;
  copy_available: true;
}