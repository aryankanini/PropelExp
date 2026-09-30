import type { ApprovalState } from "./approval";

export interface ReapprovalState {
  approval: ApprovalState;
  workflow_state: "editing" | "reapproval_required";
  export_enabled: false;
}