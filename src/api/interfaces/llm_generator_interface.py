from pydantic import BaseModel


class LLMGeneratorInterface(BaseModel):
    text: str
    cefr_level_target: str

class LLMRegeneratorInterface(BaseModel):
    text: str
    cefr_level_target: str
    previous_simplification: str
    feedback: str


