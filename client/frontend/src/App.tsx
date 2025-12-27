import { useState } from 'react'
import { Header } from './components/Header'
import { Controls } from './components/Controls'
import { TextAreas } from './components/TextAreas'
import { TestResults } from './components/TestResults'
import { generateSimplified } from './services/api'
import type { LexiGradeResponse } from './services/types'

export default function App() {
  const [language, setLanguage] = useState<'english' | 'spanish'>('english')
  const [targetCEFR, setTargetCEFR] = useState('B1')
  const [estimatedCEFR, setEstimatedCEFR] = useState<string | null>(null)
  const [originalText, setOriginalText] = useState('')
  const [simplifiedText, setSimplifiedText] = useState('')
  const [lexigradeResult, setLexigradeResult] = useState<LexiGradeResponse | null>(null)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)


  async function handleGenerate() {
  setLoading(true)
  setErrorMessage(null)
  setLexigradeResult(null)

  try {
    const result = await generateSimplified(
      originalText,
      targetCEFR,
      language
    )

    setLexigradeResult(result)

    if (!result.accepted) {
      setSimplifiedText('')
      setErrorMessage(
        'The text could not be generated because it did not pass quality control. Please wait a moment and try again.'
      )
    } else {
      setSimplifiedText(result.text)
    }

  } catch {
    setErrorMessage('Unexpected error while generating text.')
  }

  setLoading(false)
}


  return (
    <>
      <div className="container">
        <Header />

        <Controls
          language={language}
          setLanguage={setLanguage}
          targetCEFR={targetCEFR}
          setTargetCEFR={setTargetCEFR}
          estimatedCEFR={estimatedCEFR}
          setEstimatedCEFR={setEstimatedCEFR}
          originalText={originalText}
          setSimplifiedText={setSimplifiedText}
          setLoading={setLoading}
          onGenerate={handleGenerate}
          loading={loading}
        />

        <TextAreas
          originalText={originalText}
          setOriginalText={setOriginalText}
          simplifiedText={simplifiedText}
          estimatedCEFR={estimatedCEFR}
          loading={loading}
        />

        {lexigradeResult && (
          <TestResults result={lexigradeResult} />
        )}
      </div>
    </>
  )
}
