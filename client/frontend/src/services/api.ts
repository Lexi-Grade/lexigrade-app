import type { LexiGradeResponse } from './types'
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000'

export async function estimateCEFR(text: string, language: string) {
  const res = await fetch(`${API_BASE}/cefr-classifier/estimate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ language, text })
  })

  const data = await res.json()
  return data.estimated_level
}

export async function generateSimplified(
  text: string,
  target_cefr: string,
  language: string
): Promise<LexiGradeResponse> {

  const res = await fetch(`${API_BASE}/main/execute`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      language,
      original_text: text,
      cefr_level_target: target_cefr
    })
  })

  if (!res.ok) {
    throw new Error('API error')
  }

  return res.json()
}
