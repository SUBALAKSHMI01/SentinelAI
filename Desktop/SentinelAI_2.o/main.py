from fastapi import FastAPI, Query
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
    role: str   # admin / employee
    user_id: str   # 🔥 important


@app.post("/analyze")
def analyze_prompt(request: PromptRequest):
    text = request.text
    role = request.role.lower()
    user_id = request.user_id

    if role not in ["admin", "employee"]:
        return {"error": "Invalid role"}

    # 🔍 Detect
    detected = detect_sensitive_data(text)

    # 🔐 Mask
    masked_text, mapping = redact_text(text, detected)

    # 🔄 Restore
    final_response = restore_text(masked_text, mapping, role)

    # 🧾 Log everything
    log_event({
        "user_id": user_id,
        "role": role,
        "original": text,
        "masked": masked_text,
        "detected": detected
    })

    return {
        "role": role,
        "user_id": user_id,
        "original": text,
        "detected": detected,
        "masked_text": masked_text,
        "final_response": final_response
    }


# 🔥 ROLE-BASED LOG ACCESS
@app.get("/logs")
def fetch_logs(role: str = Query(...), user_id: str = Query(None)):
    return get_logs(role, user_id)


@app.get("/")
def home():
    return {"message": "SentinelAI with Audit Logs Running"}