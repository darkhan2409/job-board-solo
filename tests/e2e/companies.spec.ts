import { test, expect } from '@playwright/test'

test.describe('Companies Pages', () => {
  test.describe('Companies List', () => {
    test('should display companies list', async ({ page }) => {
      await page.goto('/companies')
      
      // Check page heading
      await expect(page.getByRole('heading', { name: 'Companies' })).toBeVisible()
      
      // Check that company cards are displayed
      await expect(page.locator('.group').first()).toBeVisible()
    })

    test('should navigate to company detail', async ({ page }) => {
      await page.goto('/companies')
      
      // Click first company card
      await page.locator('.group').first().click()
      
      // Check we're on company detail page
      await expect(page).toHaveURL(/\/companies\/\d+/)
    })
  })

  test.describe('Company Detail', () => {
    test('should display company information', async ({ page }) => {
      await page.goto('/companies/1')
      
      // Check company name is displayed
      await expect(page.getByRole('heading', { level: 1 })).toBeVisible()
      
      // Check "Open Positions" section
      await expect(page.getByText(/Open Positions at/)).toBeVisible()
    })

    test('should display company jobs', async ({ page }) => {
      await page.goto('/companies/1')
      
      // Check that job cards are displayed
      const jobCards = page.locator('.group')
      const count = await jobCards.count()
      
      // Should have at least one job
      expect(count).toBeGreaterThan(0)
    })

    test('should have breadcrumb navigation', async ({ page }) => {
      await page.goto('/companies/1')
      
      // Check back link
      const backLink = page.getByRole('link', { name: /Back to companies/i })
      await expect(backLink).toBeVisible()
      
      // Click back link
      await backLink.click()
      await expect(page).toHaveURL('/companies')
    })

    test('should navigate to job from company page', async ({ page }) => {
      await page.goto('/companies/1')
      
      // Click first job card
      await page.locator('.group').first().click()
      
      // Check we're on job detail page
      await expect(page).toHaveURL(/\/jobs\/\d+/)
    })

    test('should display company website link', async ({ page }) => {
      await page.goto('/companies/1')
      
      // Check for website link
      const websiteLink = page.getByRole('link', { name: /Visit website/i })
      
      if (await websiteLink.isVisible()) {
        await expect(websiteLink).toHaveAttribute('target', '_blank')
      }
    })
  })
})
