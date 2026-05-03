import { lazy, Suspense } from 'react'

import type { ScanResult } from '../lib/api'
import type { FingerprintRadarDatum } from './FingerprintRadarChart'
import type { InsightBarDatum } from './InsightBarChart'

const FingerprintRadarChart = lazy(() => import('./FingerprintRadarChart'))
const InsightBarChart = lazy(() => import('./InsightBarChart'))

function MetricCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="metric-card">
      <span className="metric-value">{value}</span>
      <span className="metric-label">{label}</span>
    </div>
  )
}

export default function ResultPanel({ result }: { result: ScanResult }) {
  const radarData: FingerprintRadarDatum[] = Object.entries(result.fingerprint)
    .slice(0, 6)
    .map(([key, val]) => ({
      subject: key.replace(/_/g, ' '),
      value: Math.min(Math.abs(Number(val)) * 100, 100),
    }))

  const barData: InsightBarDatum[] = result.insight_cards.map(c => ({
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
          <Suspense fallback={<div className="chart-loading-state">Loading radar chart…</div>}>
            <FingerprintRadarChart data={radarData} />
          </Suspense>
        </div>

        <div className="chart-card">
          <h3 className="chart-title">Insight Signals</h3>
          <Suspense fallback={<div className="chart-loading-state">Loading signal chart…</div>}>
            <InsightBarChart data={barData} />
          </Suspense>
        </div>
      </div>

      <div className="disclaimer-box">
        <strong>⚠ Research signal disclaimer:</strong> {result.disclaimer}
      </div>
    </section>
  )
}
