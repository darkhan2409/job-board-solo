import { test, expect } from '@playwright/test'

test.describe('Jobs List Page', () => {
  test('should display jobs list', async ({ page }) => {
    await page.goto('/jobs')
    
    // Check page heading
    await expect(page.getByRole('heading', { name: 'Find Your Next Job' })).toBeVisible()
    
    // Check that job cards are displayed
    const jobCards = page.getByTestId('job-card')
    await expect(jobCards.first()).toBeVisible()
    
    // Check job count is displayed
    await expect(page.getByText(/\d+ jobs? found/)).toBeVisible()
  })

  test('should display filters', async ({ page }) => {
    await page.goto('/jobs')
    
    // Check filter elements
    await expect(page.getByText('Filters')).toBeVisible()
    await expect(page.getByTestId('search-input')).toBeVisible()
    await expect(page.getByTestId('location-filter')).toBeVisible()
    
    // Check level checkboxes
    await expect(page.getByTestId('level-junior')).toBeVisible()
    await expect(page.getByTestId('level-middle')).toBeVisible()
    await expect(page.getByTestId('level-senior')).toBeVisible()
    await expect(page.getByTestId('level-lead')).toBeVisible()
  })

  test('should filter by search', async ({ page }) => {
    await page.goto('/jobs')
    
    // Type in search
    const searchInput = page.getByTestId('search-input')
    await searchInput.fill('React')
    
    // Wait for debounce and URL update
    await page.waitForTimeout(600)
    
    // Check URL contains search param
    await expect(page).toHaveURL(/search=React/)
  })

  test('should filter by location', async ({ page }) => {
    await page.goto('/jobs')
    
    // Select location
    const locationFilter = page.getByTestId('location-filter')
    await locationFilter.selectOption('Remote')
    
    // Check URL contains location param
    await expect(page).toHaveURL(/location=Remote/)
  })

  test('should filter by level', async ({ page }) => {
    await page.goto('/jobs')
    
    // Check senior level
    const seniorCheckbox = page.getByTestId('level-senior')
    await seniorCheckbox.check()
    
    // Check URL contains level param
    await expect(page).toHaveURL(/level=senior/)
  })

  test('should clear all filters', async ({ page }) => {
    await page.goto('/jobs?search=React&location=Remote&level=senior')
    
    // Click clear all button
    await page.getByRole('button', { name: /Clear all/i }).click()
    
    // Check URL is clean
    await expect(page).toHaveURL('/jobs')
  })

  test('should navigate to job detail', async ({ page }) => {
    await page.goto('/jobs')
    
    // Click first job card
    const firstJobCard = page.getByTestId('job-card').first()
    await firstJobCard.click()
    
    // Check we're on job detail page
    await expect(page).toHaveURL(/\/jobs\/\d+/)
    await expect(page.getByTestId('job-title')).toBeVisible()
  })
})
