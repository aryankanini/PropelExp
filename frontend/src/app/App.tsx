import { lazy, Suspense } from "react";
import { SessionProvider, useSession } from "./SessionContext";
import { DocumentIntakePage } from "../features/document-intake/DocumentIntakePage";
import { ProcessingFailurePage } from "../features/document-intake/ProcessingFailurePage";
import { ExtractionReviewPage } from "../features/extraction-review/ExtractionReviewPage";
import { ApprovalExportPage } from "../features/approval-export/ApprovalExportPage";

const PocAuthoringPage = lazy(() =>
  import("../features/poc-authoring/PocAuthoringPage").then((m) => ({
    default: m.PocAuthoringPage,
  })),
);

function Router() {
  const { page } = useSession();

  if (page === "processing") {
    return <ProcessingFailurePage />;
  }
  if (page === "extraction-review") {
    return <ExtractionReviewPage />;
  }
  if (page === "poc-authoring") {
    return (
      <Suspense fallback={<main aria-busy="true">Loading POC authoring workspace.</main>}>
        <PocAuthoringPage />
      </Suspense>
    );
  }
  if (page === "approval-export") {
    return <ApprovalExportPage />;
  }
  return <DocumentIntakePage />;
}

export function App() {
  return (
    <SessionProvider>
      <Router />
    </SessionProvider>
  );
}
