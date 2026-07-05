from pydantic import BaseModel

class IntentRequest(BaseModel):
    text: str

class IntentResponse(BaseModel):
    intent: str
    confidence: float
