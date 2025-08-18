import ollama

model = "phi3:mini"

prompt = input("Enter your prompt: ")

meesage = {
    "role": "user",  
    "content": prompt
}

response = ollama.chat(model=model, messages=[meesage])
message = response.message.content
print(f"Response: {message}")