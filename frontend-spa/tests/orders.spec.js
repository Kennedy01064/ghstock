import { test, expect } from "@playwright/test"
import { login } from "./helpers/auth"

test.describe("Orders Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Admin login (eguzman)
    await login(page, "eguzman", "eguzman")
  })

  test("should view order history", async ({ page }) => {
    await page.goto("/orders/my-orders")
    
    // Breadcrumbs or title
    await expect(page.getByTestId("orders-page-title")).toBeVisible()
    
    // Check if list container is present
    await expect(page.getByTestId("orders-list")).toBeVisible()
  })

  test("should navigate to new order view", async ({ page }) => {
    await page.goto("/orders/buildings")
    const title = page.getByTestId("buildings-page-title")
    await title.waitFor({ state: "visible", timeout: 10000 })
    await expect(title).toBeVisible()
  })
})
