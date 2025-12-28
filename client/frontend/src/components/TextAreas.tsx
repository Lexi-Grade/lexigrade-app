import { useState } from 'react'

export function TextAreas({
  originalText,
  setOriginalText,
  simplifiedText,
  estimatedCEFR
}: any) {

    const MAX_CHARS = 3000
    const [copied, setCopied] = useState(false)

    async function handlePasteOriginal() {
      try {
        const text = await navigator.clipboard.readText()
        if (text) setOriginalText(text)
      } catch {
        alert('Clipboard access denied.')
      }
    }

    async function handleCopySimplified() {
      try {
        await navigator.clipboard.writeText(simplifiedText)
        setCopied(true)
        setTimeout(() => setCopied(false), 1500)
      } catch {
        alert('Failed to copy text.')
      }
    }

  return (
    <div className="text-areas">

      <div className="text-section">
        <div className="text-header">
          <div className="text-title">
            <h2>Original Text</h2>

            {estimatedCEFR && (
              <span className="level-badge">{estimatedCEFR}</span>
            )}
          </div>

          <button
            className="icon-btn"
            onClick={handlePasteOriginal}
            title="Paste from clipboard"
          >
            📋 Paste
          </button>
        </div>

        <div className="text-wrapper">
          <textarea
            value={originalText}
            onChange={e => {
              const value = e.target.value
              if (value.length <= MAX_CHARS) {
                setOriginalText(value)
              }
            }}
            placeholder="Enter your text here..."
          />
        <div
          className={`char-counter ${
            originalText.length > 2800
              ? 'limit'
              : originalText.length > 2500
              ? 'warning'
              : ''
          }`}
        >
          {originalText.length} / {MAX_CHARS}
        </div>
        </div>
      </div>

      <div className="text-section">
        <div className="text-header">
          <h2>Simplified Text</h2>

          <button
            className="icon-btn"
            onClick={handleCopySimplified}
            disabled={!simplifiedText}
            title="Copy simplified text"
          >
            {copied ? '✅ Copied' : '📄 Copy'}
          </button>
        </div>

        <textarea value={simplifiedText} disabled />
      </div>

    </div>
  )
}

