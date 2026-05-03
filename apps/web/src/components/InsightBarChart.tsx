const SEVERITY_COLOR: Record<string, string> = {
  low: '#22c55e',
  medium: '#f59e0b',
  high: '#ef4444',
}

export interface InsightBarDatum {
  name: string
  value: number | string
  severity: 'low' | 'medium' | 'high'
}

export default function InsightBarChart({
  data,
}: {
  data: InsightBarDatum[]
}) {
  const normalized = data.map(entry => {
    const numericValue = typeof entry.value === 'number' ? entry.value : Number(entry.value)
    return {
      ...entry,
      numericValue: Number.isFinite(numericValue) ? numericValue : 0,
      displayValue: typeof entry.value === 'number' ? entry.value.toFixed(2).replace(/\.00$/, '') : entry.value,
    }
  })

  const maxValue = Math.max(...normalized.map(entry => entry.numericValue), 1)

  return (
    <div className="signal-chart-shell" aria-label="Insight signals chart">
      <div className="signal-chart-list">
        {normalized.map(entry => {
          const width = `${Math.max((entry.numericValue / maxValue) * 100, entry.numericValue > 0 ? 6 : 0)}%`
          return (
            <div key={entry.name} className="signal-chart-row">
              <div className="signal-chart-meta">
                <span className="signal-chart-name">{entry.name}</span>
                <span className="signal-chart-value">{entry.displayValue}</span>
              </div>
              <div className="signal-chart-track" aria-hidden="true">
                <div
                  className="signal-chart-fill"
                  style={{
                    width,
                    backgroundColor: SEVERITY_COLOR[entry.severity] ?? '#6366f1',
                  }}
                />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
