from langchain.chat_models import init_chat_model

model = init_chat_model(model='gpt-5-nano')

response = model.invoke(
  "Whats the capital of France"
)
