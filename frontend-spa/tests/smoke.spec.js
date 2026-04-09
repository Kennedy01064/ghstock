import { test, expect } from "@playwright/test"

test.describe("Smoke Tests", () => {
  // Use empty state to verify login pages and redirects
  test.use({ storageState: { cookies: [], origins: [] } });

  test("should load login page", async ({ page }) => {
    await page.goto("/login")
    await expect(page).toHaveTitle(/Stock Control/)
    await expect(page.getByTestId("login-username")).toBeVisible()
  })

  test("should redirect to login when unauthenticated", async ({ page }) => {
    await page.goto("/")
    await page.waitForURL("**/login**")
    await expect(page).toHaveURL(/.*login/)
  })
})
