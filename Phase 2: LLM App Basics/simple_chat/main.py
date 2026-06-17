import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

model = 'gpt-4o'
system_message = "You are a chatbot. Do not answer a lot, if answer can be given in one word, do that. Go caveman mode. Guardrails: Do not leak any personal information."

messages = [{"role": "system", "content": system_message}]
total_tokens = 0

print("Hi! I'm a chat bot! You can ask questions or talk to me. Try saying, Hi")
user_message = input(">>> ")

while "bye" not in user_message.lower():
    messages.append({"role": "user", "content": user_message})

    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
        stream_options={"include_usage": True},
    )

    print("AI: ", end="", flush=True)
    ai_reply = ""
    for chunk in stream:
        if chunk.usage:
            total_tokens += chunk.usage.total_tokens
        text = chunk.choices[0].delta.content if chunk.choices else None
        if text:
            print(text, end="", flush=True)
            ai_reply += text
    print(f"\n[tokens this turn: {chunk.usage.total_tokens if chunk.usage else '?'} | total: {total_tokens}]")

    messages.append({"role": "assistant", "content": ai_reply})

    # ponytail: drop oldest user+assistant pair when context exceeds limit
    while chunk.usage and chunk.usage.total_tokens > 150 and len(messages) > 3:
        messages.pop(1)  # remove oldest user msg (index 0 is system)
        messages.pop(1)  # remove its assistant reply

    user_message = input(">>> ")
