# New file to hold shared functionality
def create_answer(message: str):
    # Implementation moved from llm_agent.py
    from agents import Agent, Runner
    from llm_agent import prompt, get_carvago_knowledge_base, transfer_chat, get_whole_chat_history
    
    chat_bot = Agent(
        name="Chat Bot",
        instructions=prompt,
        tools=[get_carvago_knowledge_base, transfer_chat, get_whole_chat_history],
        output_type=str
    )
    input_data = "Here is the current chat history: " + message
    result = Runner.run(chat_bot, input=input_data)
    print(result.final_output)
    return result.final_output 