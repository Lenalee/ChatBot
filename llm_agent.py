
import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from text_api_chatting import get_current_chat_history, check_transfer_availability, transfer_chat, send_message
from agents import set_tracing_export_api_key 
import asyncio

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

set_tracing_export_api_key(OPENAI_API_KEY) 

load_dotenv(override=True)

prompt = """
You are CarvagoBot, an expert virtual assistant on Carvago’s used-cars website.  
Your goals:  
  • Greet visitors warmly and answer questions about our inventory, policies, and buying process.  
  • Use the following tools when needed:
    1. get_carvago_knowledge_base(query): returns factual info about Carvago.  
    2. get_whole_chat_history(user_id): retrieves this user’s past interactions. Use it when the past information is needed to answer the question. 
    3. transfer_chat(): notifies the customer you’re passing them to a human agent—but always send a closing message first so the user knows they’re being transferred.
  • If you can’t confidently answer from the knowledge base or history, reply with a brief apology, call transfer_chat(), and let the user know a real person will assist them shortly.
  • Keep responses friendly, concise, and focused on the user’s immediate need.  
  • Do not use phrasing "used car"
  • Never invent details: if you’re unsure, offer to connect them with a human.  
"""


@function_tool
def get_carvago_knowledge_base() -> str:
    with open("Carvago_KB.txt", "r") as file:
        return file.read()
    
@function_tool
def get_whole_chat_history(chat_id: str) -> str:
    return get_current_chat_history(chat_id)

@function_tool
def transfer_chat_tool(chat_id: str, message_before_transfer: str):
    can_transfer = check_transfer_availability(chat_id)
    if can_transfer:
        send_message(chat_id, message_before_transfer)
        transfer_chat(chat_id)
        return "Chat transferred successfully"
    else:
        return "Cannot transfer chat, no active agents"
    
# a vector storage?
# a part of prompt?
async def create_answer(message: str):
    chat_bot = Agent(
        name="Chat Bot",
        instructions=prompt,
        tools=[get_carvago_knowledge_base, transfer_chat_tool, get_whole_chat_history],
        output_type=str,
        model="gpt-4.1-2025-04-14"
    )
    
    input_data = "Here is the current chat history: " + message
    result = await Runner.run(chat_bot, input=input_data)
    return result.final_output

# Create a function to run the async code
# async def main():
#     response = await create_answer("chat_id: SV17SOCW0M\nHello, can you help me find a car?")
#     print(response)

# # Run the async function
# if __name__ == "__main__":
#     asyncio.run(main())

