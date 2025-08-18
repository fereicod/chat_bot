from openai import OpenAI

API_KEY = "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"

client = OpenAI(api_key=API_KEY)

response = client.responses.create(
    model="gpt-4o",
    input="Write a short bedtime story about a unicorn."
)

print(response.output_text)


