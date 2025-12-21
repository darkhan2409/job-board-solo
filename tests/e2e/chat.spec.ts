import { test, expect } from '@playwright/test'

test.describe('Chat Widget', () => {
  test('should display chat button', async ({ page }) => {
    await page.goto('/')
    
    const chatButton = page.getByTestId('chat-button')
    await expect(chatButton).toBeVisible()
  })

  test('should open chat widget', async ({ page }) => {
    await page.goto('/')
    
    // Click chat button
    await page.getByTestId('chat-button').click()
    
    // Check chat widget is visible
    const chatWidget = page.getByTestId('chat-widget')
    await expect(chatWidget).toBeVisible()
    
    // Check title
    await expect(page.getByText('Career Assistant')).toBeVisible()
  })

  test('should display chat input', async ({ page }) => {
    await page.goto('/')
    await page.getByTestId('chat-button').click()
    
    // Check input and send button
    await expect(page.getByTestId('chat-input')).toBeVisible()
    await expect(page.getByTestId('send-button')).toBeVisible()
  })

  test('should display empty state', async ({ page }) => {
    await page.goto('/')
    await page.getByTestId('chat-button').click()
    
    // Check empty state message
    await expect(page.getByText('Start a conversation!')).toBeVisible()
    await expect(page.getByText(/Try:/)).toBeVisible()
  })

  test('should close chat widget', async ({ page }) => {
    await page.goto('/')
    await page.getByTestId('chat-button').click()
    
    // Click close button
    await page.getByTestId('close-chat').click()
    
    // Chat widget should be hidden
    const chatWidget = page.getByTestId('chat-widget')
    await expect(chatWidget).not.toBeVisible()
  })

  test('should type in chat input', async ({ page }) => {
    await page.goto('/')
    await page.getByTestId('chat-button').click()
    
    const chatInput = page.getByTestId('chat-input')
    await chatInput.fill('Hello')
    
    await expect(chatInput).toHaveValue('Hello')
  })

  test('should enable send button when input has text', async ({ page }) => {
    await page.goto('/')
    await page.getByTestId('chat-button').click()
    
    const sendButton = page.getByTestId('send-button')
    const chatInput = page.getByTestId('chat-input')
    
    // Initially disabled
    await expect(sendButton).toBeDisabled()
    
    // Type text
    await chatInput.fill('Hello')
    
    // Should be enabled
    await expect(sendButton).toBeEnabled()
  })

  // Note: Testing actual AI responses requires OpenAI API key
  // and is better suited for integration tests
  test.skip('should send message and receive response', async ({ page }) => {
    await page.goto('/')
    await page.getByTestId('chat-button').click()
    
    const chatInput = page.getByTestId('chat-input')
    const sendButton = page.getByTestId('send-button')
    
    // Type and send message
    await chatInput.fill('Hello')
    await sendButton.click()
    
    // Check user message appears
    await expect(page.getByTestId('user-message')).toBeVisible()
    
    // Wait for AI response
    await expect(page.getByTestId('ai-message')).toBeVisible({ timeout: 10000 })
  })
})
