import requests
import os
import json
from dotenv import load_dotenv
from get_pat_livechat import get_access_token

load_dotenv(override=True)
client_id = os.getenv("live_chat_client_id_dev")
token = get_access_token()

def list_groups():
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    r = requests.post(
        "https://api.livechatinc.com/v3.5/configuration/action/list_groups",
        headers=headers,
        json={}
    )
    print(r.json())

def set_auto_access():

    url = "https://api.livechatinc.com/v3.5/configuration/action/add_auto_access"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    payload = {
        "access": {
            "groups": [1]  # 👈 Put the ID of the bot-only group
        },
        "conditions": {
            "domain": {
                "values": [
                    {
                        "value": "localhost",  # 👈 Or your actual site/domain
                        "exact_match": False
                    }
                ]
            }
        },
        "description": "Route widget chats to bot group"
    }

    resp = requests.post(url, headers=headers, json=payload)
    print(resp.json())

set_auto_access()