import { estimateCEFR, generateSimplified } from '../services/api'

const CEFR_LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'] as const

export function Controls({
  language,
  setLanguage,
  targetCEFR,
  setTargetCEFR,
  estimatedCEFR,
  setEstimatedCEFR,
  originalText,
  setLoading,
  onGenerate,
  loading
}: any) {

  async function handleEstimate() {
  setLoading(true)
  try {
    const level = await estimateCEFR(originalText, language)
    setEstimatedCEFR(level)
  } finally {
    setLoading(false)
  }
}

  return (
    <div className="controls">
      <div className="control-row top-row">
        <div className="control-group">
          <label>Language:</label>
          <button
            className={`lang-btn ${language === 'english' ? 'active' : ''}`}
            onClick={() => setLanguage('english')}
          >
            🇺🇸 EN
          </button>
          <button
            className={`lang-btn ${language === 'spanish' ? 'active' : ''}`}
            onClick={() => setLanguage('spanish')}
          >
            🇪🇸 ES
          </button>
        </div>

        <div className="control-group">
          <label>Target CEFR:</label>

          {CEFR_LEVELS.map(level => {
            const locked =
              estimatedCEFR &&
              CEFR_LEVELS.indexOf(level) >= CEFR_LEVELS.indexOf(estimatedCEFR)

            return (
              <button
                key={level}
                className={`cefr-btn ${targetCEFR === level ? 'active' : ''}`}
                disabled={!!locked}
                onClick={() => setTargetCEFR(level)}
              >
                {level}
              </button>
            )
          })}
        </div>

      </div>

      <div className="action-buttons">
        <button
          className="btn btn-estimate"
          onClick={handleEstimate}
          disabled={loading}
        >
          {loading ? <span className="loading" /> : 'Estimate Text Level'}
        </button>

        <button
          className="btn btn-generate"
          disabled={!estimatedCEFR || loading}
          onClick={onGenerate}
        >
          {loading ? <span className="loading" /> : 'Generate'}
        </button>
      </div>
    </div>
  )
}
