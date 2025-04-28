import asyncio
from llm_agent import create_answer
from text_api_chatting import recieve_message, send_message, recieve_new_chat

async def answer_message_async(event_data: dict):
    chat_history, chat_id = recieve_message(event_data)
    if chat_history is None:
        return
    answer = await create_answer(chat_history)
    send_message(chat_id, answer)

async def answer_new_chat_async(event_data: dict):
    messages, chat_id = recieve_new_chat(event_data)
    if messages is None:
        return
    messages = "This is a new chat.\n" + messages
    answer = await create_answer(messages)
    send_message(chat_id, answer)

# Synchronous wrapper functions for compatibility
def answer_message(event_data: dict):
    asyncio.run(answer_message_async(event_data))

def answer_new_chat(event_data: dict):
    asyncio.run(answer_new_chat_async(event_data))



