from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware 

from detector import detect_sensitive_data
from redactor import redact_text, restore_text
from logger import log_event, get_logs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    text: str
    role: str


# ✅ Simulated AI
def call_external_ai(prompt):
    return "AI Response for: " + prompt


@app.post("/analyze")
def analyze_prompt(request: PromptRequest):
    text = request.text
    role = request.role

    # 🔹 Step 1: Detect
    detected = detect_sensitive_data(text)

    # 🔹 Step 2: Mask ALWAYS
    masked_text, mapping = redact_text(text)

    # 🔹 Step 3: Send masked to AI
    ai_raw_response = call_external_ai(masked_text)

    # 🔹 Step 4: Restore original data
    final_response = restore_text(ai_raw_response, mapping)

    # 🔹 Logging (optional)
    log_event({
        "role": role,
        "original": text,
        "masked": masked_text,
        "detected": detected
    })

    return {
        "role": role,
        "original": text,
        "detected": detected,
        "masked_text": masked_text,
        "ai_raw_response": ai_raw_response,
        "final_response": final_response
    }


@app.get("/logs")
def fetch_logs():
    return get_logs()