/// <reference types="vite/client" />

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export interface ScanResult {
  disclaimer: string
  plan: 'free' | 'pro'
  quota_remaining_today: number | null
  metrics: {
    char_count: number
    word_count: number
    unique_word_count: number
    [key: string]: number
  }
  fingerprint: Record<string, number>
  fingerprint_vector: number[]
  content_hash: string
  insight_cards: Array<{
    title: string
    value: number
    severity: 'low' | 'medium' | 'high'
  }>
}

export interface CheckoutResponse {
  url: string
}

export async function scanText(text: string, userId = 'anonymous'): Promise<ScanResult> {
  const res = await fetch(`${API_BASE}/scan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, user_id: userId }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw Object.assign(new Error(err.detail ?? 'Scan failed'), { status: res.status })
  }
  return res.json()
}

export async function createCheckoutSession(userId = 'anonymous', email?: string): Promise<string> {
  const res = await fetch(`${API_BASE}/billing/create-checkout-session`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, email }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail ?? 'Checkout failed')
  }
  const data: CheckoutResponse = await res.json()
  return data.url
}
