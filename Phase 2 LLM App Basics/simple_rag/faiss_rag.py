import numpy as np
from openai import OpenAI
import faiss


client = OpenAI()
model = 'text-embedding-3-small'

documents = [
    "The corporate office kitchen coffee machine password is 'Espresso2026!'. Do not share it.",
    "Company health insurance is provided by BlueCross. Employees can submit claims via the HR portal.",
    "The office will be closed for regular maintenance on July 14th, 2026.",
    "Project 'Zephyr' is our upcoming autonomous drone delivery software scheduled for beta in Q4.",
    "For IT support, open a ticket at help.internal or call extension 404."
]

def generate_embeddings(string: str):
  return client.embeddings.create(
    input = [string],
    model = model
  )

response = [generate_embeddings(document) for document in documents]

embdeddings = [item.data.embedding for item in response]

embedding_matrix = np.array(embdeddings, dtype = 'float32')

print(embedding_matrix.shape)

