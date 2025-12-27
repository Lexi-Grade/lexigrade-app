export interface LexiGradeResponse {
  language: string
  original_cefr: string
  target_cefr: string
  accepted: boolean
  strategy: number
  soft_relaxed: boolean
  semantic_alert: string | null
  text: string

  final_hard_tests: {
    accepted: boolean
    passed_tests: number
    total_tests: number
    failed_tests: Record<string, any>
  }

  final_soft_tests: {
    accepted: boolean
    pass_ratio: number
    min_required: number
    passed_tests: string[]
    total_tests: number
    failed_tests: Record<string, any>
  }
}