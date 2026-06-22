from openai import OpenAI
import numpy as np
from dotenv import load_dotenv
load_dotenv()

documents = [
    "The corporate office kitchen coffee machine password is 'Espresso2026!'. Do not share it.",
    "Company health insurance is provided by BlueCross. Employees can submit claims via the HR portal.",
    "The office will be closed for regular maintenance on July 14th, 2026.",
    "Project 'Zephyr' is our upcoming autonomous drone delivery software scheduled for beta in Q4.",
    "For IT support, open a ticket at help.internal or call extension 404."
]

client = OpenAI()
model = 'text-embedding-3-small'

def generate_embeddings(string: str):
  return client.embeddings.create(
    input = [string],
    model = model
  )

doc_embeddings = [generate_embeddings(doc).data[0].embedding for doc in documents]
print(doc_embeddings[0])

def calculate_cosine(vec_a: list, vec_b: list) -> float:
  return float(np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b)))

new_string = "Zephyr is our upcoming drone that will be released in Q4"
new_string_embedding = generate_embeddings(new_string).data[0].embedding
sim_scores = [calculate_cosine(new_string_embedding, embeds) for embeds in doc_embeddings]

print(sim_scores)
