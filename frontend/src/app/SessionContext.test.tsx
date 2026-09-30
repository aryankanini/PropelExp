import { act, renderHook } from "@testing-library/react";
import type { ReactNode } from "react";
import { beforeEach, describe, expect, it } from "vitest";

import { SessionProvider, useSession } from "./SessionContext";

function wrapper({ children }: { children: ReactNode }) {
	return <SessionProvider>{children}</SessionProvider>;
}

describe("SessionProvider", () => {
	beforeEach(() => sessionStorage.clear());

	it("restores the active case after refresh and clears it on reset", () => {
		const first = renderHook(() => useSession(), { wrapper });

		act(() => first.result.current.setCaseId("case-1"));
		first.unmount();

		const refreshed = renderHook(() => useSession(), { wrapper });
		expect(refreshed.result.current.caseId).toBe("case-1");

		act(() => refreshed.result.current.reset());
		expect(sessionStorage.getItem("cms-planner-active-case")).toBeNull();
	});
});
