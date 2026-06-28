from langchain.chat_models import init_chat_model
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

model = init_chat_model(model='gpt-5-nano')

response = model.invoke(
  "Whats the capital of France"
)

print(response.content)

print('++++++')

pprint(response.response_metadata)
