import { test as setup, expect } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('authenticate as superadmin', async ({ page }) => {
  // Use baseURL from config
  await page.goto('/login');
  
  // Fill credentials for krojas (Superadmin)
  await page.getByTestId('login-username').fill('krojas');
  await page.getByTestId('login-password').fill('krojas');
  await page.getByTestId('login-submit').click();

  // Wait for login to complete
  await page.waitForURL(/\/($|dashboard\/(admin|manager))/, { timeout: 30000 });
  
  // Verify session is active - checking for user name in the navbar
  await expect(page.getByTestId('navbar-user-name')).toBeVisible();

  // End of setup: result is a JSON file with cookies and local storage
  await page.context().storageState({ path: authFile });
});
