import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("ERRO: A chave GROQ_API_KEY não foi encontrada no arquivo .env!")

client = Groq(api_key=api_key)

MODELO = "qwen/qwen3.8-27b"

print("Entregável 01")

response = client.chat.completions.create(
    model=MODELO,
    messages=[
        {"role": "system", "content": "Você é um assistente de estudos prestativo e direto. Responda de forma concisa."},
        {"role": "user", "content": "Qual é a diferença entre uma pilha e uma fila em estrutura de dados?"}
    ],
    temperature=0.7,
    max_tokens=300
)

print("RESPOSTA DO MODELO")
print(response.choices[0].message.content)

print("\nUso de Tokens")
print(f"Tokens de Entrada (Prompt) : {response.usage.prompt_tokens}")
print(f"Tokens de Saída (Completion): {response.usage.completion_tokens}")
print(f"Total de Tokens            : {response.usage.total_tokens}")

print("\nENTREGÁVEL 02")

print("\n[A1] Teste SEM histórico:")

client.chat.completions.create(
    model=MODELO,
    messages=[
        {"role": "user", "content": "Olá! Meu nome é Gabriel."}
    ],
    max_tokens=50
)

res_sem_historico = client.chat.completions.create(
    model=MODELO,
    messages=[
        {"role": "user", "content": "Qual é o meu nome?"}
    ],
    max_tokens=100
)
print("Resposta do modelo:", res_sem_historico.choices[0].message.content)

print("\n[A2] Teste COM histórico explícito:")

res_com_historico = client.chat.completions.create(
    model=MODELO,
    messages=[
        {"role": "system", "content": "Você é um assistente de estudos prestativo."},
        {"role": "user", "content": "Olá! Meu nome é Gabriel."},
        {"role": "assistant", "content": "Olá Gabriel! Como posso te ajudar hoje?"},
        {"role": "user", "content": "Qual é o meu nome?"}
    ],
    max_tokens=100
)
print("Resposta do modelo:", res_com_historico.choices[0].message.content)

print("\nENTREGÁVEL 02 - EXPERIMENTO B: TEMPERATURA")

prompt_temp = "Crie uma analogia curta de 2 frases para explicar o que é uma API."

res_temp_0 = client.chat.completions.create(
    model=MODELO,
    messages=[{"role": "user", "content": prompt_temp}],
    temperature=0.0,
    max_tokens=100
)

print("\n[B1] Resposta com Temperature = 0.0:")
print(res_temp_0.choices[0].message.content)

res_temp_1 = client.chat.completions.create(
    model=MODELO,
    messages=[{"role": "user", "content": prompt_temp}],
    temperature=1.0,
    max_tokens=100
)

print("\n[B2] Resposta com Temperature = 1.0:")
print(res_temp_1.choices[0].message.content)

print("\nFIM DA EXECUÇÃO")