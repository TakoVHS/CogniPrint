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

export interface PortalResponse {
  url: string
}

export interface BillingConfig {
  billing_enabled: boolean
  configured: boolean
  mode: string
  app_public_url: string
  plans: Record<string, { label: string; price_id?: string | null; contact_only?: boolean }>
}

export interface AccountStatus {
  user_id: string
  email: string | null
  plan: 'free' | 'starter' | 'research_pro' | 'institution'
  subscription_status: string
  quota_remaining_today: number | null
  free_daily_scan_limit: number
  max_text_chars: number
  checkout_enabled: boolean
  billing_mode?: string
  price_ids?: {
    starter: string | null
    research_pro: string | null
  }
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
  const res = await fetch(`${API_BASE}/api/billing/create-checkout-session`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, email, plan: 'research_pro' }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail ?? 'Checkout failed')
  }
  const data: CheckoutResponse = await res.json()
  return data.url
}

export async function getAccountStatus(userId: string, email?: string): Promise<AccountStatus> {
  const params = new URLSearchParams({ user_id: userId })
  if (email) {
    params.set('email', email)
  }
  const res = await fetch(`${API_BASE}/account/status?${params.toString()}`)
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail ?? 'Failed to load account status')
  }
  return res.json()
}

export async function getBillingConfig(): Promise<BillingConfig> {
  const res = await fetch(`${API_BASE}/api/billing/config`)
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail ?? 'Failed to load billing config')
  }
  return res.json()
}

export async function createPortalSession(userId: string): Promise<string> {
  const res = await fetch(`${API_BASE}/api/billing/create-portal-session`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail ?? 'Customer portal failed')
  }
  const data: PortalResponse = await res.json()
  return data.url
}
