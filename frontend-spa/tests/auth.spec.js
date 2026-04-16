import { test, expect } from "@playwright/test"
import { login } from "./helpers/auth"

test.describe("Authentication Flow", () => {
  // Always start unauthenticated to test login mechanics
  test.use({ storageState: { cookies: [], origins: [] } });

  test("should login successfully as superadmin", async ({ page }) => {
    // These credentials are based on the actual stock_local.db
    await login(page, "krojas", "krojas")
    
    // Verify dashboard access (lands on / for superadmin)
    await expect(page).toHaveURL("/")
    // Target the profile name in the navbar via testId
    await expect(page.getByTestId('navbar-user-name')).toBeVisible()
  })

  test("should login successfully as admin", async ({ page }) => {
    await login(page, "eguzman", "eguzman")
    await expect(page).toHaveURL("/dashboard/admin")
    // Use regex to allow for the comma in "Resumen Operativo,"
    await expect(page.getByText(/Resumen Operativo/i)).toBeVisible()
  })

  test("should login successfully as manager", async ({ page }) => {
    await login(page, "mgomez", "mgomez")
    await expect(page).toHaveURL("/dashboard/manager")
    await expect(page.getByText(/Tablero Logístico/i).first()).toBeVisible()
  })

  test("should show error on invalid credentials", async ({ page }) => {
    await page.goto("/login")
    await page.getByTestId("login-username").fill("wronguser")
    await page.getByTestId("login-password").fill("wrongpass")
    await page.getByTestId("login-submit").click()
    
    // Check for error message (based on LoginView.vue error div)
    await expect(page.getByTestId("login-error")).toBeVisible()
  })
})
