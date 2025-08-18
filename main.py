import ollama

history = []
model = "phi3:mini"

while True:
    prompt = input("Input: ")
    if prompt.lower() == "exit":
        print("Exiting the chat.")
        break

    meesage = {
        "role": "user",  
        "content": prompt
    }
    history.append(meesage)
    
    print("Bot:", end="", flush=True)

    message_content = ""
    response = ollama.chat(model=model, messages=history, stream=True)
    
    for chunk in response:
        message_content += chunk.message.content
        print(chunk.message.content, end="", flush=True)
    
    print()  # New line after the bot's response

    bot_message = {
        "role": "assistant",
        "content": message_content
    }
    history.append(bot_message)