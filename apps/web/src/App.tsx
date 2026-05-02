import { lazy, Suspense, useState, useCallback, useEffect, useMemo } from 'react'
import {
  scanText,
  createCheckoutSession,
  createPortalSession,
  getAccountStatus,
  getRuntimeStatus,
  AccountStatus,
  RuntimeStatus,
  ScanResult,
} from './lib/api'

const ResultPanel = lazy(() => import('./components/ResultPanel'))

// ─────────────────────────── components ───────────────────────────────────────

function NavBar() {
  return (
    <nav className="navbar">
      <span className="navbar-brand">
        <span className="brand-accent">Cogni</span>Print
      </span>
      <div className="navbar-links">
        <a href="#scanner">Scanner</a>
        <a href="#pricing">Pricing</a>
        <a href="mailto:enterprise@cogniprint.org">Enterprise</a>
      </div>
    </nav>
  )
}

const USER_ID_STORAGE_KEY = 'cogniprint.content_scanner.user_id'
const EMAIL_STORAGE_KEY = 'cogniprint.content_scanner.email'

function getOrCreateUserId() {
  const existing = window.localStorage.getItem(USER_ID_STORAGE_KEY)
  if (existing) {
    return existing
  }
  const generated =
    typeof crypto !== 'undefined' && 'randomUUID' in crypto
      ? crypto.randomUUID()
      : `cp_${Math.random().toString(36).slice(2)}${Date.now().toString(36)}`
  window.localStorage.setItem(USER_ID_STORAGE_KEY, generated)
  return generated
}

function Hero({ onStart }: { onStart: () => void }) {
  return (
    <section className="hero">
      <div className="hero-inner">
        <div className="hero-badge">Statistical Content Profiling</div>
        <h1 className="hero-title">
          Know your text's<br />
          <span className="gradient-text">cognitive fingerprint</span>
        </h1>
        <p className="hero-sub">
          CogniPrint profiles lexical diversity, structural cadence, and stylistic
          consistency as a hosted convenience layer around the research workstation.
          The commercial surface is meant for managed empirical reports and workflow access,
          not stronger scientific claims.
        </p>
        <div className="hero-cta-row">
          <button className="btn-primary" onClick={onStart}>
            Scan Text Free
          </button>
          <a className="btn-ghost" href="#pricing">See Pro Plans →</a>
        </div>
        <p className="hero-disclaimer">
          Outputs are research-oriented statistical signals only — not legal proof,
          authorship guarantee, or detector verdict.
        </p>
      </div>
    </section>
  )
}

function ScannerForm({
  onResult,
  loading,
  setLoading,
  quota,
  userId,
}: {
  onResult: (r: ScanResult) => void
  loading: boolean
  setLoading: (v: boolean) => void
  quota: number | null
  userId: string
}) {
  const [text, setText] = useState('')
  const [error, setError] = useState<string | null>(null)

  const handleScan = useCallback(async () => {
    if (!text.trim()) return
    setError(null)
    setLoading(true)
    try {
      const result = await scanText(text, userId)
      onResult(result)
    } catch (err: unknown) {
      const e = err as { status?: number; message?: string }
      if (e.status === 402) {
        setError('Free daily limit reached. Upgrade to Pro for unlimited scans.')
      } else {
        setError(e.message ?? 'Scan failed. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }, [text, onResult, setLoading, userId])

  return (
    <section id="scanner" className="scanner-section">
      <h2 className="section-title">Content Scanner</h2>
      {quota !== null && (
        <p className="quota-badge">
          Free scans remaining today: <strong>{quota}</strong>
        </p>
      )}
      <div className="scanner-card">
        <div className="account-inline">
          <span className="account-inline-label">Browser account</span>
          <code>{userId.slice(0, 8)}…{userId.slice(-6)}</code>
        </div>
        <textarea
          className="scanner-textarea"
          placeholder="Paste your text here (min 10 words)…"
          value={text}
          onChange={e => setText(e.target.value)}
          rows={10}
        />
        <div className="scanner-footer">
          <span className="char-count">{text.length.toLocaleString()} chars</span>
          <button
            className="btn-primary"
            onClick={handleScan}
            disabled={loading || !text.trim()}
          >
            {loading ? 'Scanning…' : 'Scan →'}
          </button>
        </div>
        {error && <p className="scanner-error">{error}</p>}
      </div>
    </section>
  )
}

function PricingSection({
  userId,
  email,
  setEmail,
  checkoutEnabled,
}: {
  userId: string
  email: string
  setEmail: (value: string) => void
  checkoutEnabled: boolean
}) {
  const handleUpgrade = async () => {
    try {
      const url = await createCheckoutSession(userId, email || undefined)
      window.location.href = url
    } catch {
      alert('Stripe checkout is not available in this environment.')
    }
  }

  return (
    <section id="pricing" className="pricing-section">
      <h2 className="section-title">Plans</h2>
      <p className="pricing-sub">Hosted access for research workflow convenience, not stronger conclusions.</p>
      <div className="pricing-grid">
        <div className="pricing-card">
          <div className="plan-name">Starter</div>
          <div className="plan-price">$0<span>/month</span></div>
          <ul className="plan-features">
            <li>3 scans per day</li>
            <li>Fingerprint radar</li>
            <li>Insight signal cards</li>
            <li>Content hash</li>
          </ul>
          <button className="btn-ghost-full" onClick={() => document.getElementById('scanner')?.scrollIntoView({ behavior: 'smooth' })}>
            Start free
          </button>
        </div>

        <div className="pricing-card pricing-card--featured">
          <div className="plan-badge-top">Most popular</div>
          <div className="plan-name">Research Pro</div>
          <div className="plan-price">$199<span>/month (test-mode prep)</span></div>
          <label className="plan-field">
            <span>Billing email</span>
            <input
              className="plan-input"
              type="email"
              placeholder="you@company.com"
              value={email}
              onChange={e => setEmail(e.target.value)}
            />
          </label>
          <ul className="plan-features">
            <li>Higher hosted analysis usage</li>
            <li>Extended text (120k chars)</li>
            <li>Managed empirical report flow</li>
            <li>Review-oriented exports</li>
          </ul>
          <button className="btn-primary-full" onClick={handleUpgrade} disabled={!checkoutEnabled || !email.trim()}>
            Subscribe Research Pro →
          </button>
          {!checkoutEnabled && <p className="plan-note">Stripe checkout is not configured in this environment yet.</p>}
          {checkoutEnabled && !email.trim() && <p className="plan-note">Enter a billing email before starting checkout.</p>}
        </div>

        <div className="pricing-card">
          <div className="plan-name">Institution</div>
          <div className="plan-price">Custom</div>
          <ul className="plan-features">
            <li>Audit-friendly workflows</li>
            <li>Private project workspace</li>
            <li>Custom support review</li>
            <li>Manual contact</li>
          </ul>
          <a className="btn-ghost-full" href="mailto:enterprise@cogniprint.org">
            Contact for Institution
          </a>
        </div>
      </div>
    </section>
  )
}

function AccountSection({ account, userId }: { account: AccountStatus | null; userId: string }) {
  const [portalError, setPortalError] = useState<string | null>(null)
  const [portalLoading, setPortalLoading] = useState(false)

  const openPortal = useCallback(async () => {
    setPortalError(null)
    setPortalLoading(true)
    try {
      const url = await createPortalSession(userId)
      window.location.href = url
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Customer portal is unavailable.'
      setPortalError(message)
    } finally {
      setPortalLoading(false)
    }
  }, [userId])

  return (
    <section id="account" className="scanner-section">
      <h2 className="section-title">Billing Status</h2>
      <div className="scanner-card">
        <p><strong>Current plan:</strong> {account?.plan ?? 'free'}</p>
        <p><strong>Subscription status:</strong> {account?.subscription_status ?? 'none'}</p>
        <p><strong>Billing mode:</strong> {account?.billing_mode ?? 'test'}</p>
        <button className="btn-ghost-full" onClick={openPortal} disabled={portalLoading}>
          {portalLoading ? 'Opening portal…' : 'Open customer portal'}
        </button>
        {portalError && <p className="scanner-error">{portalError}</p>}
      </div>
    </section>
  )
}

function Footer() {
  return (
    <footer className="footer">
      <p>
        © {new Date().getFullYear()} CogniPrint — Statistical research signals only.
        Not legal proof. Not authorship guarantee. Not an AI detector verdict.
      </p>
      <p className="footer-links">
        <a href="https://github.com/TakoVHS/CogniPrint" target="_blank" rel="noreferrer">GitHub</a>
        {' · '}
        <a href="mailto:enterprise@cogniprint.org">Enterprise</a>
      </p>
    </footer>
  )
}

// ─────────────────────────── app shell ────────────────────────────────────────

export default function App() {
  const [result, setResult] = useState<ScanResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [quota, setQuota] = useState<number | null>(null)
  const [account, setAccount] = useState<AccountStatus | null>(null)
  const [runtimeStatus, setRuntimeStatus] = useState<RuntimeStatus | null>(null)
  const [accountError, setAccountError] = useState<string | null>(null)
  const [email, setEmail] = useState('')
  const [statusMessage, setStatusMessage] = useState<string | null>(null)
  const userId = useMemo(() => getOrCreateUserId(), [])

  const loadAccount = useCallback(async (nextEmail?: string) => {
    try {
      const resolvedEmail = nextEmail ?? email
      const status = await getAccountStatus(userId, resolvedEmail || undefined)
      setAccount(status)
      setQuota(status.quota_remaining_today)
      setAccountError(null)
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to load account status.'
      setAccountError(message)
    }
  }, [email, userId])

  const loadRuntimeStatus = useCallback(async () => {
    try {
      const status = await getRuntimeStatus()
      setRuntimeStatus(status)
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to load runtime readiness.'
      setAccountError(message)
    }
  }, [])

  useEffect(() => {
    const savedEmail = window.localStorage.getItem(EMAIL_STORAGE_KEY) ?? ''
    void loadRuntimeStatus()
    if (savedEmail) {
      setEmail(savedEmail)
      void loadAccount(savedEmail)
    } else {
      void loadAccount()
    }
    const params = new URLSearchParams(window.location.search)
    const checkout = params.get('checkout')
    if (checkout === 'success') {
      setStatusMessage('Checkout completed. Refreshing plan status for this browser account.')
      void loadAccount(savedEmail)
    } else if (checkout === 'cancelled') {
      setStatusMessage('Checkout was cancelled. Your free access remains active.')
    }
  }, [loadAccount, loadRuntimeStatus])

  useEffect(() => {
    window.localStorage.setItem(EMAIL_STORAGE_KEY, email)
  }, [email])

  const handleResult = useCallback((r: ScanResult) => {
    setResult(r)
    if (r.quota_remaining_today !== null) {
      setQuota(r.quota_remaining_today)
    }
    void loadAccount()
    setTimeout(() => {
      document.getElementById('results')?.scrollIntoView({ behavior: 'smooth' })
    }, 100)
  }, [loadAccount])

  const scrollToScanner = useCallback(() => {
    document.getElementById('scanner')?.scrollIntoView({ behavior: 'smooth' })
  }, [])

  return (
    <div className="app">
      <NavBar />
      <Hero onStart={scrollToScanner} />
      <section className="status-strip">
        <div>
          <strong>Plan:</strong> {account?.plan?.toUpperCase() ?? 'FREE'}
          {' · '}
          <strong>Browser account:</strong> <code>{userId.slice(0, 8)}…{userId.slice(-6)}</code>
        </div>
        <div>
          <strong>Checkout:</strong> {account?.checkout_enabled ? 'enabled' : 'not configured'}
          {' · '}
          <strong>Runtime:</strong> {runtimeStatus?.ok ? `${runtimeStatus.database}/${runtimeStatus.analysis_backend}` : 'unavailable'}
        </div>
      </section>
      {statusMessage && <section className="status-banner">{statusMessage}</section>}
      {accountError && <section className="status-banner status-banner-error">{accountError}</section>}
      <ScannerForm
        onResult={handleResult}
        loading={loading}
        setLoading={setLoading}
        quota={quota}
        userId={userId}
      />
      {result && (
        <div id="results">
          <Suspense
            fallback={
              <section className="result-section">
                <div className="scanner-card result-loading-card">
                  Loading chart bundle…
                </div>
              </section>
            }
          >
            <ResultPanel result={result} />
          </Suspense>
        </div>
      )}
      <PricingSection
        userId={userId}
        email={email}
        setEmail={setEmail}
        checkoutEnabled={account?.checkout_enabled ?? false}
      />
      <AccountSection account={account} userId={userId} />
      <Footer />
    </div>
  )
}
