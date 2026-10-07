import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Instancia o cliente direto da env
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

model = "qwen/qwen3.8-27b"

# entregavel 1 
req1 = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "Você é um assistente de estudos prestativo e direto. Responda de forma concisa."},
        {"role": "user", "content": "Qual é a diferença entre uma pilha e uma fila em estrutura de dados?"}
    ],
    temperature=0.7,
    max_tokens=300
)

print("Entregavel 01:")
print(req1.choices[0].message.content)
print("tokens entrada:", req1.usage.prompt_tokens)
print("tokens saida:", req1.usage.completion_tokens)
print("total:", req1.usage.total_tokens)
print("-" * 20)

# entregavel 2
# a1-sem hist
client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "Olá! Meu nome é Gabriel."}],
    max_tokens=50
)

r_sem = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "Qual é o meu nome?"}],
    max_tokens=100
)
print("Sem historico:", r_sem.choices[0].message.content)

# a2-com hist
msgs = [
    {"role": "system", "content": "Você é um assistente de estudos prestativo."},
    {"role": "user", "content": "Olá! Meu nome é Gabriel."},
    {"role": "assistant", "content": "Olá Gabriel! Como posso te ajudar hoje?"},
    {"role": "user", "content": "Qual é o meu nome?"}
]

r_com = client.chat.completions.create(
    model=model,
    messages=msgs,
    max_tokens=100
)
print("Com historico:", r_com.choices[0].message.content)
print("-" * 20)

# b - temp
p = "Crie uma analogia curta de 2 frases para explicar o que é uma API."

t0 = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": p}],
    temperature=0.0,
    max_tokens=100
)
print("Temp 0.0:", t0.choices[0].message.content)

t1 = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": p}],
    temperature=1.0,
    max_tokens=100
)
print("Temp 1.0:", t1.choices[0].message.content)