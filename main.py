from fastapi import FastAPI, Request
import os
from odoo import create_odoo_lead

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Webhook is live"}

from fastapi import Request

@app.get("/webhook")
def verify_webhook(request: Request):
    from fastapi.responses import PlainTextResponse
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if token == "verify_token":
        return PlainTextResponse(content=challenge, status_code=200)
    return {"error": "Invalid verification token"}


@app.post("/webhook")
async def receive_lead(request: Request):
    data = await request.json()

    # Extract basic lead info
    full_name = ""
    phone = ""
    email = ""
    campaign = data.get("campaign_name", "Unknown Campaign")
    questions = []

    if "entry" in data:
        for entry in data["entry"]:
            for change in entry.get("changes", []):
                lead_data = change.get("value", {})
                for field in lead_data.get("field_data", []):
                    name = field.get("name")
                    val = field.get("values", [""])[0]

                    if "name" in name.lower():
                        full_name = val
                    elif "email" in name.lower():
                        email = val
                    elif "phone" in name.lower():
                        phone = val
                    else:
                        questions.append(f"{name}: {val}")

    description = f"Campaign: {campaign}\n" + "\n".join(questions)

    # Send to Odoo
    create_odoo_lead(full_name, phone, email, description)

    return {"status": "Lead received"}
