/**
 * Helper to perform login in E2E tests.
 * @param {import('@playwright/test').Page} page 
 * @param {string} username 
 * @param {string} password 
 */
export async function login(page, username, password) {
  await page.goto("/login")
  await page.getByTestId("login-username").fill(username)
  await page.getByTestId("login-password").fill(password)
  await page.getByTestId("login-submit").click()
  
  // Wait for login to complete – can land on / or specific dashboards
  // Wait for login to complete – can land on / for superadmin or specific dashboards for others
  // Stricter regex to avoid partial matches on /login
  await page.waitForURL(/\/($|dashboard\/(admin|manager))/, { timeout: 30000 })
}
