export interface FingerprintRadarDatum {
  subject: string
  value: number
}

const CHART_SIZE = 320
const CENTER = CHART_SIZE / 2
const MAX_RADIUS = 96
const GRID_LEVELS = [0.25, 0.5, 0.75, 1]

function polarToCartesian(angle: number, radius: number) {
  return {
    x: CENTER + Math.cos(angle) * radius,
    y: CENTER + Math.sin(angle) * radius,
  }
}

function toPolygonPoints(data: FingerprintRadarDatum[], radiusScale = 1) {
  return data
    .map((point, index) => {
      const angle = -Math.PI / 2 + (index / data.length) * Math.PI * 2
      const radius = MAX_RADIUS * radiusScale * Math.max(0, Math.min(point.value / 100, 1))
      const { x, y } = polarToCartesian(angle, radius)
      return `${x},${y}`
    })
    .join(' ')
}

export default function FingerprintRadarChart({
  data,
}: {
  data: FingerprintRadarDatum[]
}) {
  const safeData = data.length ? data : [{ subject: 'signal', value: 0 }]
  const polygonPoints = toPolygonPoints(safeData)

  return (
    <div className="radar-chart-shell" aria-label="Fingerprint radar chart">
      <svg
        className="radar-chart-svg"
        viewBox={`0 0 ${CHART_SIZE} ${CHART_SIZE}`}
        role="img"
        aria-label="Fingerprint radar"
      >
        {GRID_LEVELS.map(level => (
          <polygon
            key={level}
            points={toPolygonPoints(
              safeData.map(point => ({ ...point, value: level * 100 })),
              1,
            )}
            className="radar-chart-grid"
          />
        ))}

        {safeData.map((point, index) => {
          const angle = -Math.PI / 2 + (index / safeData.length) * Math.PI * 2
          const axis = polarToCartesian(angle, MAX_RADIUS)
          const label = polarToCartesian(angle, MAX_RADIUS + 26)
          const anchor =
            Math.abs(label.x - CENTER) < 12 ? 'middle' : label.x < CENTER ? 'end' : 'start'

          return (
            <g key={point.subject}>
              <line
                x1={CENTER}
                y1={CENTER}
                x2={axis.x}
                y2={axis.y}
                className="radar-chart-axis"
              />
              <text
                x={label.x}
                y={label.y}
                textAnchor={anchor}
                className="radar-chart-label"
              >
                <tspan x={label.x} dy="0">
                  {point.subject}
                </tspan>
                <tspan x={label.x} dy="13" className="radar-chart-label-value">
                  {Math.round(point.value)}
                </tspan>
              </text>
            </g>
          )
        })}

        <polygon points={polygonPoints} className="radar-chart-area" />

        {safeData.map((point, index) => {
          const angle = -Math.PI / 2 + (index / safeData.length) * Math.PI * 2
          const radius = MAX_RADIUS * Math.max(0, Math.min(point.value / 100, 1))
          const { x, y } = polarToCartesian(angle, radius)

          return <circle key={`${point.subject}-dot`} cx={x} cy={y} r="4" className="radar-chart-dot" />
        })}
      </svg>
    </div>
  )
}
