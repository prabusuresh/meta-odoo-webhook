import requests
import os

def create_odoo_lead(name, phone, email, description):
    url = f"{os.getenv('ODOO_URL')}/jsonrpc"
    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "object",
            "method": "execute_kw",
            "args": [
                os.getenv("ODOO_DB"),
                os.getenv("ODOO_USER_ID"),
                os.getenv("ODOO_API_KEY"),
                "crm.lead",
                "create",
                [{
                    "name": name or "Facebook Lead",
                    "email_from": email,
                    "phone": phone,
                    "description": description,
                    "user_id": int(os.getenv("ODOO_USER_ID")),
                }]
            ]
        },
        "id": 1,
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
