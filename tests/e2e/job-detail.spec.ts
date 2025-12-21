import { test, expect } from '@playwright/test'

test.describe('Job Detail Page', () => {
  test('should display job details', async ({ page }) => {
    await page.goto('/jobs/1')
    
    // Check all required elements
    await expect(page.getByTestId('job-title')).toBeVisible()
    await expect(page.getByTestId('company-name')).toBeVisible()
    await expect(page.getByTestId('job-description')).toBeVisible()
    await expect(page.getByTestId('apply-button')).toBeVisible()
  })

  test('should display company information', async ({ page }) => {
    await page.goto('/jobs/1')
    
    // Check company section
    await expect(page.getByText('About the Company')).toBeVisible()
  })

  test('should have breadcrumb navigation', async ({ page }) => {
    await page.goto('/jobs/1')
    
    // Check back link
    const backLink = page.getByRole('link', { name: /Back to jobs/i })
    await expect(backLink).toBeVisible()
    
    // Click back link
    await backLink.click()
    await expect(page).toHaveURL('/jobs')
  })

  test('should navigate to company page', async ({ page }) => {
    await page.goto('/jobs/1')
    
    // Click company name
    const companyLink = page.getByTestId('company-name')
    await companyLink.click()
    
    // Check we're on company page
    await expect(page).toHaveURL(/\/companies\/\d+/)
  })

  test('should display apply button', async ({ page }) => {
    await page.goto('/jobs/1')
    
    const applyButton = page.getByTestId('apply-button')
    await expect(applyButton).toBeVisible()
    await expect(applyButton).toHaveText('Apply for this position')
  })

  test('should handle non-existent job', async ({ page }) => {
    const response = await page.goto('/jobs/99999')
    
    // Should show 404 or error page
    expect(response?.status()).toBe(404)
  })
})
