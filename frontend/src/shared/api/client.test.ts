import { describe, expect, it } from "vitest";
import { apiUrl } from "./client";

describe("apiUrl", () => {
  it("joins the backend origin and API path with one slash", () => {
    expect(apiUrl("/api/v1/session/status")).toBe(
      "https://propelexp.onrender.com/api/v1/session/status",
    );
  });
});