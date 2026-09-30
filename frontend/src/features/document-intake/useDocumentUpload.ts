import { useState } from "react";

import { apiUrl } from "../../shared/api/client";

export interface AcceptedUpload {
  status: "extraction_ready";
  case_id: string;
  upload_id: string;
  size_bytes: number;
  page_count: number;
}

interface IntakeProblem {
  code: string;
  message: string;
}

type UploadState =
  | { status: "idle" }
  | { status: "uploading"; progress: number }
  | { status: "accepted"; result: AcceptedUpload }
  | { status: "rejected"; problem: IntakeProblem };

export function useDocumentUpload(sessionId: string) {
  const [state, setState] = useState<UploadState>({ status: "idle" });

  function upload(file: File) {
    const request = new XMLHttpRequest();
    const form = new FormData();
    form.append("file", file);
    setState({ status: "uploading", progress: 0 });

    request.upload.addEventListener("progress", (event) => {
      if (event.lengthComputable) {
        setState({
          status: "uploading",
          progress: Math.round((event.loaded / event.total) * 100),
        });
      }
    });
    request.addEventListener("load", () => {
      const body = JSON.parse(request.responseText) as AcceptedUpload | IntakeProblem;
      if (request.status === 201 && "case_id" in body) {
        setState({ status: "accepted", result: body });
        return;
      }
      const problem = "message" in body
        ? body
        : { code: "upload_failed", message: "The upload could not be completed." };
      setState({ status: "rejected", problem });
    });
    request.addEventListener("error", () => {
      setState({
        status: "rejected",
        problem: { code: "network_error", message: "The upload could not be completed." },
      });
    });
    request.open("POST", apiUrl("/api/v1/cases"));
    request.setRequestHeader("X-Session-ID", sessionId);
    request.send(form);
  }

  return { state, upload, reset: () => setState({ status: "idle" }) };
}