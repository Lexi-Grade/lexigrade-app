from pydantic import BaseModel


class LLMReviewerInterface(BaseModel):
    original_text: str
    simplified_text: str
    cefr_level_target: str



