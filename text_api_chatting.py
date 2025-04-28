import json
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from get_pat_livechat import get_access_token

# Remove the circular import
# from llm_agent import create_answer

load_dotenv(override=True)
bot_id = os.getenv("bot_id")
token = get_access_token()

def send_message(chat_id: str, message: str):
    url = "https://api.livechatinc.com/v3.5/agent/action/send_event"
    headers = {
        "Authorization": "Bearer " + os.getenv("bot_token"),
        "Content-Type": "application/json",
        "X-Author-Id": bot_id

    }
    payload = {
        "chat_id": chat_id,
        "event": {
            "type": "message",    # Must be "message"
            "text": message,      # Use the message variable here
            "visibility": "all"
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        print("Message sent successfully")
    else:
        print(f"Error sending message: {response.status_code} - {response.text}")


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

def get_current_chat_history(chat_id: str):
    chat = get_chat(chat_id)
    if not chat:
        print("Error retrieving chat")
        return "Could not get the chat"
    users = {}
    current_data = ""
    for user in chat["users"]:
        users[user["id"]] = {"name": user["name"], "type": user["type"]}
        if user["type"] == "customer": #save customer data
            current_data += "The user is currently looking at this car: " + str(user["session_fields"]) + "\n"
    messages = get_thread_messages(chat["thread"]["events"], users)

    return current_data + messages

def get_thread_messages(thread: dict, users: dict):
    parsed_chat = ""
    for event in thread:
        if event["type"] == "message":
            parsed_chat += f"At {get_date(event['created_at'])} from {users[event['author_id']]['name']}({users[event['author_id']]['type']}): {event['text']}\n\n"
        elif event["type"] == "system_message":
            parsed_chat += f"At {get_date(event['created_at'])} System message: {event['text']}\n\n"
        elif event["type"] == "filled_form":
            parsed_chat += f"At {get_date(event['created_at'])} Customer filled a form:\n"
            for field in event["fields"]:
                parsed_chat += f"{field['label']} {field['answer']}, "
            parsed_chat += "\n\n"
        elif event["type"] == "rich_message":
            try:
                parsed_chat += f'Rich message: {event["elements"][0]["title"]} \n\n'
            except:
                parsed_chat += f"Rich message: {event}\n\n"
        else:
            parsed_chat += f"Some other event: {event['type']}\n\n"
            parsed_chat += f"{event}\n\n"
    return parsed_chat

def get_complete_chat_history(chat_id: str):
    chat = get_chat(chat_id)
    if not chat:
        print("Error retrieving chat")
        return "Could not get the chat"
    
    users = {}
   
    for user in chat["users"]:
        users[user["id"]] = {"name": user["name"], "type": user["type"]}
    #print("Gathered users: ", users)
    threads = get_all_threads(chat_id)
    threads.sort(key=lambda x: x['created_at'])
    parsed_chat = ""
    for thread in threads:
        parsed_chat += f"\n\nNew thread with {len(thread['events'])} amount of events\n"
        parsed_chat += get_thread_messages(thread["events"], users)
        
            
    return parsed_chat

def get_date(str_date: str):
    date_obj = datetime.fromisoformat(str_date.replace('Z', '+00:00'))
    return date_obj.strftime('%d-%m-%y %H:%M')

def recieve_message(message_data: dict):
    event_type = message_data["payload"]["event"]["type"]
    if event_type != "message":
        print("some other event type: ", event_type)
        return None, None
    sender = message_data["payload"]["event"]["author_id"]
    if sender == bot_id:
        print("message from myself")
        return None, None
    visibility = message_data["payload"]["event"]["visibility"]
    if visibility != "all":
        print("message not visible to the customer")
        return None, None
    chat_id = message_data["payload"]["chat_id"]
    chat_id = message_data["payload"]["chat_id"]
    chat_history = "chat_id: " + chat_id + "\n" + get_current_chat_history(chat_id)
    print("History of incomming message\n", chat_history)
   # print("returning chat history: ", chat_history, ", chat_id: ", chat_id)
    return chat_history, chat_id
    # # Import create_answer here to avoid circular import
    # from llm_agent import create_answer
    # answer = create_answer(chat_history)
    # send_message(chat_id, answer)


def recieve_new_chat(chat_data: dict):
    chat_data = chat_data["payload"]["chat"]
    current_users = chat_data["thread"]["user_ids"]
    if bot_id not in current_users:
        print("I will not respond, i'm not in the chat-------------------_!")
        return None, None
    
    users = {}
    current_data = ""
    for user in chat_data["users"]:
        users[user["id"]] = {"name": user["name"], "type": user["type"]}
        if user["type"] == "customer": #save customer data
            current_data += "The user is currently looking at this car: " + str(user["session_fields"]) + "\n"
    messages = "chat_id: " + chat_data["id"] + "\n" +get_thread_messages(chat_data["thread"]["events"], users)
    print("History of new chat\n", current_data + messages)

    return current_data + messages, chat_data["id"]



# when transfering, first check if someone is online, if not, say this to customer annnnd create a ticket?
def transfer_chat(chat_id: str):
    url = "https://api.livechatinc.com/v3.5/agent/action/transfer_chat"
    headers = {
        "Authorization": "Bearer " + os.getenv("bot_token"),
        "Content-Type": "application/json",
        "X-Author-Id": bot_id

    }
    payload = {
        "id": chat_id,
        "target.type": "group",
        "target.ids": [0]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        print(response.json())
        print("Chat transferred successfully")
    else:
        print(f"Error transferring chat: {response.status_code} - {response.text}")

def check_transfer_availability(chat_id: str):
    url = "https://api.livechatinc.com/v3.5/agent/action/list_agents_for_transfer"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
    }

    payload = {
        "chat_id": chat_id,
       # "fields": ["routing_status"]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        print(response.json())
        agent_list = response.json()
        if len(agent_list) == 1 and bot_id in agent_list[0]["agent_id"]: #only the bot is online
            return False
        else:
            return True
    else:
        print(f"Error checking availability: {response.status_code} - {response.text}")
#check_availability("SV17SOCW0M")
#print(get_complete_chat_history("SV17SOCW0M"))
#print(get_current_chat_history("SV17SOCW0M"))





