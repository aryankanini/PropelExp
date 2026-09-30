import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

export type AppPage =
  | "intake"
  | "processing"
  | "extraction-review"
  | "poc-authoring"
  | "approval-export";

export interface SessionState {
  sessionId: string;
  caseId: string | null;
  jobId: string | null;
  deficiencyId: string | null;
  page: AppPage;
}

interface SessionContextValue extends SessionState {
  navigate: (page: AppPage, updates?: Partial<Omit<SessionState, "page">>) => void;
  setCaseId: (caseId: string) => void;
  setJobId: (jobId: string) => void;
  setDeficiencyId: (deficiencyId: string) => void;
  reset: () => void;
}

const SESSION_ID = "local-session";
const ACTIVE_CASE_KEY = "cms-planner-active-case";

const defaultState: SessionState = {
  sessionId: SESSION_ID,
  caseId: null,
  jobId: null,
  deficiencyId: null,
  page: "intake",
};

const SessionContext = createContext<SessionContextValue | null>(null);

export function SessionProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<SessionState>(() => ({
    ...defaultState,
    caseId: sessionStorage.getItem(ACTIVE_CASE_KEY),
  }));

  useEffect(() => {
    if (state.caseId) {
      sessionStorage.setItem(ACTIVE_CASE_KEY, state.caseId);
    } else {
      sessionStorage.removeItem(ACTIVE_CASE_KEY);
    }
  }, [state.caseId]);

  function navigate(page: AppPage, updates?: Partial<Omit<SessionState, "page">>) {
    setState((current) => ({ ...current, ...updates, page }));
  }

  function setCaseId(caseId: string) {
    setState((current) => ({ ...current, caseId }));
  }

  function setJobId(jobId: string) {
    setState((current) => ({ ...current, jobId }));
  }

  function setDeficiencyId(deficiencyId: string) {
    setState((current) => ({ ...current, deficiencyId }));
  }

  function reset() {
    sessionStorage.removeItem(ACTIVE_CASE_KEY);
    setState(defaultState);
  }

  return (
    <SessionContext.Provider
      value={{ ...state, navigate, setCaseId, setJobId, setDeficiencyId, reset }}
    >
      {children}
    </SessionContext.Provider>
  );
}

export function useSession(): SessionContextValue {
  const ctx = useContext(SessionContext);
  if (!ctx) throw new Error("useSession must be used inside SessionProvider");
  return ctx;
}
