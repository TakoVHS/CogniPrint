import { useState, useCallback } from 'react'
import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
} from 'recharts'
import { scanText, createCheckoutSession, ScanResult } from './lib/api'

// ─────────────────────────── helpers ──────────────────────────────────────────

const SEVERITY_COLOR: Record<string, string> = {
  low: '#22c55e',
  medium: '#f59e0b',
  high: '#ef4444',
}

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
          consistency — giving editorial teams measurable signals for content QA and
          drift detection.
        </p>
        <div className="hero-cta-row">
          <button className="btn-primary" onClick={onStart}>
            Scan Text Free
          </button>
          <a className="btn-ghost" href="#pricing">See Pro Plans →</a>
        </div>
        <p className="hero-disclaimer">
          Outputs are statistical signals only — not legal proof, authorship
          guarantee, or AI detector verdict.
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
}: {
  onResult: (r: ScanResult) => void
  loading: boolean
  setLoading: (v: boolean) => void
  quota: number | null
}) {
  const [text, setText] = useState('')
  const [error, setError] = useState<string | null>(null)

  const handleScan = useCallback(async () => {
    if (!text.trim()) return
    setError(null)
    setLoading(true)
    try {
      const result = await scanText(text)
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
  }, [text, onResult, setLoading])

  return (
    <section id="scanner" className="scanner-section">
      <h2 className="section-title">Content Scanner</h2>
      {quota !== null && (
        <p className="quota-badge">
          Free scans remaining today: <strong>{quota}</strong>
        </p>
      )}
      <div className="scanner-card">
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

function MetricCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="metric-card">
      <span className="metric-value">{value}</span>
      <span className="metric-label">{label}</span>
    </div>
  )
}

function ResultPanel({ result }: { result: ScanResult }) {
  const radarData = Object.entries(result.fingerprint)
    .slice(0, 6)
    .map(([key, val]) => ({
      subject: key.replace(/_/g, ' '),
      value: Math.min(Math.abs(Number(val)) * 100, 100),
    }))

  const barData = result.insight_cards.map(c => ({
    name: c.title,
    value: typeof c.value === 'number' ? Math.round(c.value * 100) / 100 : c.value,
    severity: c.severity,
  }))

  return (
    <section className="result-section">
      <div className="result-header">
        <h2 className="section-title">Scan Results</h2>
        <span className={`plan-badge plan-${result.plan}`}>
          {result.plan.toUpperCase()} plan
        </span>
      </div>

      <div className="metrics-grid">
        <MetricCard label="Characters" value={result.metrics.char_count?.toLocaleString()} />
        <MetricCard label="Words" value={result.metrics.word_count?.toLocaleString()} />
        <MetricCard label="Unique words" value={result.metrics.unique_word_count?.toLocaleString()} />
        <MetricCard
          label="Content hash"
          value={result.content_hash.slice(0, 12) + '…'}
        />
      </div>

      <div className="charts-row">
        <div className="chart-card">
          <h3 className="chart-title">Fingerprint Radar</h3>
          <ResponsiveContainer width="100%" height={260}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="#334155" />
              <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 11 }} />
              <Radar
                name="signal"
                dataKey="value"
                stroke="#6366f1"
                fill="#6366f1"
                fillOpacity={0.25}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3 className="chart-title">Insight Signals</h3>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={barData} layout="vertical">
              <XAxis type="number" tick={{ fill: '#94a3b8', fontSize: 11 }} />
              <YAxis dataKey="name" type="category" width={130} tick={{ fill: '#94a3b8', fontSize: 11 }} />
              <Tooltip
                contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
                labelStyle={{ color: '#e2e8f0' }}
              />
              <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                {barData.map((entry, idx) => (
                  <Cell key={idx} fill={SEVERITY_COLOR[entry.severity] ?? '#6366f1'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="disclaimer-box">
        <strong>⚠ Research signal disclaimer:</strong> {result.disclaimer}
      </div>
    </section>
  )
}

function PricingSection() {
  const handleUpgrade = async () => {
    try {
      const url = await createCheckoutSession()
      window.location.href = url
    } catch {
      alert('Stripe checkout is not available in this environment.')
    }
  }

  return (
    <section id="pricing" className="pricing-section">
      <h2 className="section-title">Plans</h2>
      <p className="pricing-sub">Statistical content profiling for every team size.</p>
      <div className="pricing-grid">
        <div className="pricing-card">
          <div className="plan-name">Free</div>
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
          <div className="plan-name">Pro</div>
          <div className="plan-price">$199<span>/month</span></div>
          <ul className="plan-features">
            <li>Unlimited scans</li>
            <li>Extended text (120k chars)</li>
            <li>Priority support</li>
            <li>All Free features</li>
          </ul>
          <button className="btn-primary-full" onClick={handleUpgrade}>
            Upgrade to Pro →
          </button>
        </div>

        <div className="pricing-card">
          <div className="plan-name">Enterprise</div>
          <div className="plan-price">Custom</div>
          <ul className="plan-features">
            <li>Volume pricing</li>
            <li>SSO &amp; audit logs</li>
            <li>Dedicated support</li>
            <li>SLA guarantee</li>
          </ul>
          <a className="btn-ghost-full" href="mailto:enterprise@cogniprint.org">
            Contact sales
          </a>
        </div>
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

  const handleResult = useCallback((r: ScanResult) => {
    setResult(r)
    if (r.quota_remaining_today !== null) {
      setQuota(r.quota_remaining_today)
    }
    setTimeout(() => {
      document.getElementById('results')?.scrollIntoView({ behavior: 'smooth' })
    }, 100)
  }, [])

  const scrollToScanner = useCallback(() => {
    document.getElementById('scanner')?.scrollIntoView({ behavior: 'smooth' })
  }, [])

  return (
    <div className="app">
      <NavBar />
      <Hero onStart={scrollToScanner} />
      <ScannerForm
        onResult={handleResult}
        loading={loading}
        setLoading={setLoading}
        quota={quota}
      />
      {result && (
        <div id="results">
          <ResultPanel result={result} />
        </div>
      )}
      <PricingSection />
      <Footer />
    </div>
  )
}
