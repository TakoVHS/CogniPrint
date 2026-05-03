import { chromium } from 'playwright'
import { mkdir } from 'node:fs/promises'
import path from 'node:path'

const baseUrl = process.argv[2]
const screenshotPath = process.argv[3]

if (!baseUrl) {
  throw new Error('Usage: node apps/web/scripts/browser_verify.mjs <base-url> [screenshot-path]')
}

const consoleErrors = []
const pageErrors = []

const browser = await chromium.launch({ headless: true })
const page = await browser.newPage({ viewport: { width: 1440, height: 1600 } })

page.on('console', msg => {
  if (msg.type() === 'error') {
    consoleErrors.push(msg.text())
  }
})

page.on('pageerror', err => {
  pageErrors.push(String(err))
})

try {
  const readyResponse = page.waitForResponse(
    response => response.url().includes('/ready') && response.status() === 200,
  )
  const accountResponse = page.waitForResponse(
    response => response.url().includes('/account/status') && response.status() === 200,
  )

  await page.goto(baseUrl, { waitUntil: 'domcontentloaded' })
  await Promise.all([readyResponse, accountResponse])
  await page.waitForLoadState('networkidle')

  await page.waitForSelector('text=Statistical Content Profiling')
  await page.waitForSelector('textarea.scanner-textarea')
  await page.waitForSelector('text=Billing Status')

  const bodyText = await page.locator('body').innerText()
  if (!bodyText.includes('CogniPrint')) {
    throw new Error('App shell loaded without CogniPrint content')
  }

  const errorBanner = page.locator('.status-banner-error')
  if (await errorBanner.count()) {
    const message = await errorBanner.first().innerText()
    throw new Error(`Runtime error banner detected: ${message}`)
  }

  const scanResponse = page.waitForResponse(
    response => response.url().includes('/scan') && response.status() === 200,
  )
  await page.locator('textarea.scanner-textarea').fill(
    'CogniPrint browser verification text checks the hosted scanner flow after the Vite 8 upgrade with a stable local runtime.',
  )
  await page.getByRole('button', { name: 'Scan →' }).click()
  await scanResponse

  await page.waitForSelector('text=Scan Results')
  await page.waitForSelector('text=Characters')
  await page.waitForSelector('text=Words')
  await page.waitForSelector('text=Content hash')
  await page.waitForSelector('text=FREE plan')

  await page.locator('input[type="email"]').fill('reviewer@example.com')
  const subscribeButton = page.getByRole('button', { name: 'Subscribe Research Pro →' })
  if (!(await subscribeButton.isDisabled())) {
    throw new Error('Checkout button should stay disabled when billing is not configured')
  }
  await page.waitForSelector('text=Stripe checkout is not configured in this environment yet.')

  if (pageErrors.length) {
    throw new Error(`Page errors detected: ${pageErrors.join(' | ')}`)
  }

  if (consoleErrors.length) {
    throw new Error(`Console errors detected: ${consoleErrors.join(' | ')}`)
  }

  if (screenshotPath) {
    await mkdir(path.dirname(screenshotPath), { recursive: true })
    await page.screenshot({ path: screenshotPath, fullPage: true })
  }

  console.log(`Browser verification passed: ${baseUrl}`)
} catch (error) {
  if (screenshotPath) {
    try {
      await mkdir(path.dirname(screenshotPath), { recursive: true })
      await page.screenshot({ path: screenshotPath, fullPage: true })
    } catch {
      // Keep the original verification error when artifact capture fails.
    }
  }
  throw error
} finally {
  await browser.close()
}
