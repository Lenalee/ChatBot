import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv(override=True)

def get_access_token():
    ACCOUNT_ID = os.getenv("live_chat_account_id")              
    PERSONAL_ACCESS_TOKEN = os.getenv("live_chat_pat")

    auth_string = f"{ACCOUNT_ID}:{PERSONAL_ACCESS_TOKEN}"
   # print(auth_string)
    auth_encoded = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")

    return f"Basic {auth_encoded}"



# headers = {
#     "Authorization": get_access_token(),
#     "Content-Type": "application/json"
# }

# url = "https://api.livechatinc.com/v3.5/configuration/action/list_agents"
# response = requests.post(url, headers=headers, json={})

# if response.status_code == 200:
#     print("Success!")
#     print(response.json())
# else:
#     print("Failed with status:", response.status_code)
#     print("Body:", response.text)