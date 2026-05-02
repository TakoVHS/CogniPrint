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

import type { ScanResult } from '../lib/api'

const SEVERITY_COLOR: Record<string, string> = {
  low: '#22c55e',
  medium: '#f59e0b',
  high: '#ef4444',
}

function MetricCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="metric-card">
      <span className="metric-value">{value}</span>
      <span className="metric-label">{label}</span>
    </div>
  )
}

export default function ResultPanel({ result }: { result: ScanResult }) {
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
