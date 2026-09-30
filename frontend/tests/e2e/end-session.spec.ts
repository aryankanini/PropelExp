import { expect, test } from "@playwright/test";

test.describe("End session", () => {
  test("cancel, failed cleanup, and retry preserve truthful state", async ({ page }) => {
    let cleanupAttempts = 0;
    await page.route("**/api/v1/session/status", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ storage: "session_only", remaining_inactivity_seconds: 3000 }),
      });
    });
    await page.route("**/api/v1/cases", async (route) => {
      await route.fulfill({
        status: 201,
        contentType: "application/json",
        body: JSON.stringify({
          status: "extraction_ready",
          case_id: "case-1",
          upload_id: "upload-1",
          size_bytes: 7,
          page_count: 1,
        }),
      });
    });
    await page.route("**/api/v1/cases/case-1", async (route) => {
      cleanupAttempts += 1;
      await route.fulfill({
        status: cleanupAttempts === 1 ? 503 : 200,
        contentType: "application/json",
        body: JSON.stringify({
          outcome: cleanupAttempts === 1 ? "failed" : "completed",
          remaining_files: cleanupAttempts === 1 ? 1 : 0,
          failed_stores: cleanupAttempts === 1 ? ["workspace"] : [],
        }),
      });
    });
    await page.goto("/");
    await page.getByLabel("Select CMS-2567").setInputFiles({
      name: "cms-2567.pdf",
      mimeType: "application/pdf",
      buffer: Buffer.from("content"),
    });
    await page.getByRole("button", { name: "Upload CMS-2567" }).click();
    await expect(page.getByText("Document is extraction-ready.")).toBeVisible();

    await page.getByRole("button", { name: "End session" }).click();
    await page.getByRole("button", { name: "Cancel" }).click();
    await expect(page.getByText("Document is extraction-ready.")).toBeVisible();

    await page.getByRole("button", { name: "End session" }).click();
    await page.getByRole("button", { name: "End session and remove data" }).click();
    await expect(page.getByRole("alert")).toContainText("case remains available");
    await expect(page.getByText("Document is extraction-ready.")).toBeVisible();

    await page.getByRole("button", { name: "Try cleanup again" }).click();
    await expect(page.getByText("Document is extraction-ready.")).toBeHidden();
    await expect(page.getByRole("heading", { name: "Upload CMS-2567" })).toBeVisible();
  });
});