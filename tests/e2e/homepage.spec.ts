import { test, expect } from '@playwright/test'

test.describe('Homepage', () => {
  test('should display hero section', async ({ page }) => {
    await page.goto('/')
    
    // Check hero heading
    await expect(page.getByRole('heading', { name: 'Find Your Dream Tech Job' })).toBeVisible()
    
    // Check CTA buttons
    await expect(page.getByRole('link', { name: 'Browse Jobs' })).toBeVisible()
    await expect(page.getByRole('link', { name: 'View Companies' })).toBeVisible()
  })

  test('should display features section', async ({ page }) => {
    await page.goto('/')
    
    // Check feature cards
    await expect(page.getByText('Latest Opportunities')).toBeVisible()
    await expect(page.getByText('Smart Filtering')).toBeVisible()
    await expect(page.getByText('Top Companies')).toBeVisible()
  })

  test('should navigate to jobs page', async ({ page }) => {
    await page.goto('/')
    
    await page.getByRole('link', { name: 'Browse Jobs' }).first().click()
    
    await expect(page).toHaveURL('/jobs')
    await expect(page.getByRole('heading', { name: 'Find Your Next Job' })).toBeVisible()
  })

  test('should navigate to companies page', async ({ page }) => {
    await page.goto('/')
    
    await page.getByRole('link', { name: 'View Companies' }).first().click()
    
    await expect(page).toHaveURL('/companies')
    await expect(page.getByRole('heading', { name: 'Companies' })).toBeVisible()
  })

  test('should display chat button', async ({ page }) => {
    await page.goto('/')
    
    // Check chat widget button
    const chatButton = page.getByTestId('chat-button')
    await expect(chatButton).toBeVisible()
  })
})
