import requests
import os
import json
from dotenv import load_dotenv
from get_pat_livechat import get_access_token
from datetime import datetime
load_dotenv(override=True)
client_id = os.getenv("live_chat_client_id_dev")
token = get_access_token()


def create_livechat_bot(
    name: str,
    avatar: str = None,
    max_chats_count: int = None,
    default_group_priority: str = "first",
    groups: list = None,
    work_scheduler: dict = None
):
    url = "https://api.livechatinc.com/v3.5/configuration/action/create_bot"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    payload = {
        "name": name,
        "owner_client_id": client_id
    }
    payload["job_title"] = "Chatting bot"
    # Add optional fields if they are provided
    if avatar:
        payload["avatar"] = avatar
    if max_chats_count:
        payload["max_chats_count"] = max_chats_count
    if default_group_priority:
        payload["default_group_priority"] = default_group_priority  
    if groups:
        payload["groups"] = groups
    if work_scheduler:
        payload["work_scheduler"] = work_scheduler

    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        print("Everything is good")
        print(response.json())
        with open("data_ids/bot_id.json", "w") as f:
            json.dump(response.json(), f)
        return response.json()
    else:
        print(f"error in the create_livechat_bot function: {response.status_code} - {response.text}")
        #raise Exception(f"Error: {response.status_code} - {response.text}")

def set_routing_status():
    url = "https://api.livechatinc.com/v3.5/agent/action/set_routing_status"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    with open("data_ids/bot_id.json", "r") as f:
        bot_id = json.load(f)["id"]
    payload = {
        "status": "accepting_chats",
        "agent_id": bot_id
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        print("Routing status set to accepting chats")
    else:
        print(f"Error setting routing status: {response.status_code} - {response.text}")

def unregister_webhook(webhook_id: str):
    url = "https://api.livechatinc.com/v3.5/configuration/action/unregister_webhook"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "id": webhook_id,
        "owner_client_id": client_id
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        print("Webhook unregistered successfully")
    else:
        print(f"Error unregistering webhook: {response.status_code} - {response.text}")

def set_webhook():
    url = "https://api.livechatinc.com/v3.5/webhook/action/set_webhook"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
#     {
#   "webhook_id": "<webhook_id>",
#   "secret_key": "<secret_key>",
#   "action": "<action>",
#   "organization_id": "<organization_id>",
#   "payload": {
#   },
#   "additional_data": {
#     "chat_properties": { //optional
#         // chat properties
#     },
#     "chat_presence_user_ids": [ //optional
#       // User IDs
#     ]
#   }
# }

def list_webhooks():
    url = "https://api.livechatinc.com/v3.5/configuration/action/list_webhooks"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "owner_client_id": client_id
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        print("Webhooks listed successfully")
        print(response.json())
        return response.json()
    else:
        print(f"Error listing webhooks: {response.status_code} - {response.text}")
def delete_all_webhooks():
    webhooks = list_webhooks()
    for webhook in webhooks:
        id = webhook["id"]
        print(f"Deleting webhook: {id}")
        unregister_webhook(id)

def register_webhook(action: str, description: str, webhook_url: str, additional_data: list=[]):
    url = "https://api.livechatinc.com/v3.5/configuration/action/register_webhook"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
  #  print("webhook_url", f"{webhook_url}/{action}")
  #tODO change back to action endpoint
    payload = {
        "action": action,
        "secret_key": "my_secret_key_1",
        "url": f"{webhook_url}/{action}",
        #"url": f"{webhook_url}/webhook",
        "additional_data": additional_data,
        "description": description,
        "owner_client_id": client_id,
        "type": "bot"
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        print("Webhook registered successfully")
        with open(f"data_ids/webhook_{action}.json", "w") as f:
            json.dump(response.json(), f)
        print(response.json())
    else:
        print(f"Error registering webhook: {response.status_code} - {response.text}")
   

def get_bot_token():
    url = "https://api.livechatinc.com/v3.5/configuration/action/issue_bot_token"

 
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    with open("data_ids/bot_id.json", "r") as f:
        data = json.load(f)
        bot_id = data["id"]
        bot_secret = data["secret"]
    payload = {
        "bot_id": bot_id,
        "client_id": client_id,
        "bot_secret": bot_secret,
        "organization_id": os.getenv("live_chat_organization_id")
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        print("Bot token issued successfully")
        print(response.json())
    else:
        print(f"Error issuing bot token: {response.status_code} - {response.text}")

def get_chat(chat_id: str):
    url = "https://api.livechatinc.com/v3.5/agent/action/get_chat"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "chat_id": chat_id
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        return response.json()
    else:
        print(f"Error retrieving chat: {response.status_code} - {response.text}")
        return None
def get_all_threads(chat_id: str):
    url = "https://api.livechatinc.com/v3.5/agent/action/list_threads"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    all_threads = []
    page_id = None

    while True:
        payload = {
            "chat_id": chat_id
        }
        if page_id:
            payload["page_id"] = page_id

        response = requests.post(url, headers=headers, json=payload)
        if response.ok:
            data = response.json()
            all_threads.extend(data.get("threads", []))
            page_id = data.get("next_page_id")
            if not page_id:
                break
        else:
            print(f"Error retrieving threads: {response.status_code} - {response.text}")
            break

    return all_threads

def get_user_name(user_id: str):
#     0	:	5a47db8a-a9c7-495b-8dff-9fd37affd23e
# 1	:	5ec4714f45da39243bfccbc58bbcfcfa
# 2	:	f3ffdc0289c3c08f7a6ea73dedef0949
    user_id = "f3ffdc0289c3c08f7a6ea73dedef0949"
    url= "https://api.livechatinc.com/v3.5/configuration/action/list_bots"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "id": user_id
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        print("User retrieved successfully")
        print(response.json())
    else:
        print(f"Error retrieving user: {response.status_code} - {response.text}")
def parse_chat(chat_id: str):
    chat = get_chat(chat_id)
  #  print(chat)
    if not chat:
        print("Error retrieving chat")
        return "Could not get the chat"
    return parse_thread(chat)

def parse_thread(thread):

    users = {}
   
    for user in thread["users"]:
        users[user["id"]] = {"name": user["name"], "type": user["type"]}
    parsed_chat = ""
    for event in thread["thread"]["events"]:
        if event["type"] == "message":
            parsed_chat += f"{users[event['author_id']]['name']}({users[event['author_id']]['type']}): {event['text']}\n\n"
       # elif event["type"] == "filled_form":
            #TODO probably implement this
           # parsed_chat += f"Filled form: {event['form_id']}\n"
    print(parsed_chat)
    return parsed_chat

def get_date(str_date: str):
    date_obj = datetime.fromisoformat(str_date.replace('Z', '+00:00'))
    return date_obj.strftime('%d-%m-%y %H:%M')

def parse_all_threads(thread_id: str):
    threads = get_all_threads(thread_id)
    print(threads)
    parsed_chat = ""
    for thread in threads:
        parsed_chat += "\n\nNew thread\n"
        print("events", len(thread["events"]))
        for event in thread["events"]:

            if event["type"] == "message":
                parsed_chat += f"At {get_date(event['created_at'])} from {event['author_id']}: {event['text']}\n\n"
            elif event["type"] == "system_message":
                parsed_chat += f"At {get_date(event['created_at'])} System message: {event['text']}\n\n"
            elif event["type"] == "filled_form":
                parsed_chat += f"At {get_date(event['created_at'])} Customer filled a form:\n"
                for field in event["fields"]:
                    # print(field['label'])
                    # print(field['answer'])
                    parsed_chat += f"{field['label']} {field['answer']}, "
                parsed_chat += "\n\n"
            elif event["type"] == "rich_message":
                parsed_chat += f"Rich message: {event}\n\n"
            else:
                parsed_chat += f"Some other event: {event['type']}\n\n"
                parsed_chat += f"{event}\n\n"
            
    #print(parsed_chat)
    return parsed_chat


def update_routing_priorities():
    url = "https://api.livechatinc.com/v3.5/configuration/action/update_group"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    bot_id = os.getenv("bot_id")
    payload = {
        "id": 0,
        "agent_priorities": {
          bot_id: "first",
          "yanina.arameleva+120@carvago.com": "normal"
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.ok:

        print(response.json())
    else:
        print(f"Error testing endpoint: {response.status_code} - {response.text}")


def check_group():
    url = "https://api.livechatinc.com/v3.5/configuration/action/get_group"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "id": 0,
        "fields": ["agent_priorities", "routing_status"]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        print(response.json())
    else:
        print(f"Error checking group: {response.status_code} - {response.text}")


#check_group()


# 1. create bot
#create_livechat_bot("webhook_bot", default_group_priority="first" )
# 2. set routing status to accepting chats
#set_routing_status()
#3. get bot token
get_bot_token()
# 4. register webhook

# set webhooks

# delete_all_webhooks()
# ngrok_url = "https://5160-82-208-51-34.ngrok-free.app"
# register_webhook(action="incoming_event", description="webhook for new messages", webhook_url=ngrok_url)
# #register_webhook(action="incoming_chat", description="webhook new chat created", webhook_url=ngrok_url)
# register_webhook(action="chat_deactivated", description="webhook chat deactivated", webhook_url=ngrok_url)
# register_webhook(action="user_added_to_chat", description="webhook user added to chat", webhook_url=ngrok_url)


#5. update routing priorities
#update_routing_priorities()


#send_message("SV165FLZZ3", "how are you?")






