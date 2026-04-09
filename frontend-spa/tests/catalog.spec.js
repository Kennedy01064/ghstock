import { test, expect } from "@playwright/test"
import { login } from "./helpers/auth"

test.describe("Catalog Management", () => {
  test.beforeEach(async ({ page }) => {
    // Superadmin has access to create products
    await login(page, "krojas", "krojas")
  })

  test("should create a new product", async ({ page }) => {
    await page.goto("/catalog/products/create")
    
    const sku = `E2E-${Date.now()}`
    
    await page.getByTestId("product-name").fill("Product E2E Test")
    await page.getByTestId("product-sku").fill(sku)
    await page.getByTestId("product-price").fill("45.50")
    
    await page.getByTestId("product-submit").click()
    
    // Should redirect back to warehouse and show success
    await page.waitForURL("**/catalog/warehouse", { timeout: 15000 })
    
    // Ensure loading is finished
    await page.getByTestId("warehouse-loading").waitFor({ state: "hidden", timeout: 15000 })
    
    // Search for the new SKU to bring it to the top/viewport
    await page.fill('input[placeholder="Filtrar por SKU o Nombre..."]', sku)
    
    const title = page.getByTestId("warehouse-page-title")
    await expect(title).toBeVisible()
    await expect(page.getByText("Product E2E Test")).toBeVisible()
    await expect(page.getByText(sku)).toBeVisible()
  })
})
