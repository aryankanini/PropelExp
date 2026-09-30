import type { PocSectionName } from "../../shared/api/poc";

export const pocSectionLabels: Readonly<Record<PocSectionName, string>> = {
  affected_residents: "Affected residents",
  others_at_risk: "Other residents at risk",
  corrective_measures: "Corrective measures",
  monitoring: "Monitoring",
  completion_date: "Completion date",
};