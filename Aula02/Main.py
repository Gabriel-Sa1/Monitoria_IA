import os
import re
from dotenv import load_dotenv
from openai import OpenAI

# 1. Carrega variáveis de ambiente
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY não encontrada. Verifique se o arquivo .env contém a chave."
    )

client = OpenAI(
    api_key=api_key,
    base_url=os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1"),
)

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# 2. Base do Conhecimento (Knowledge Base)
knowledge_base = [
    {
        "id": "doc1",
        "title": "Regras de Avaliação e Frequência",
        "keywords": ["nota", "prova", "frequencia", "media", "presenca"],
        "content": "A média final da disciplina é calculada por (P1 * 0.4) + (P2 * 0.4) + (Trabalhos * 0.2). A frequência mínima para aprovação é de 75% das aulas presenciais."
    },
    {
        "id": "doc2",
        "title": "Horários e Local de Monitoria",
        "keywords": ["monitoria", "horario", "duvidas", "local", "laboratorio"],
        "content": "As monitorias de Inteligência Artificial acontecem todas as terças e quintas-feiras, das 17h às 19h00, na Sala 1002 do Bloco 1."
    },
    {
        "id": "doc3",
        "title": "Ementa do Módulo de LLMs e RAG",
        "keywords": ["conteudo", "llm", "groq", "prompt", "rag", "contexto"],
        "content": "O módulo aborda APIs de LLM, engenharia de prompt, histórico de conversa, context engineering e técnicas de busca de contexto local."
    },
    {
        "id": "doc4",
        "title": "Prazos do Projeto Final",
        "keywords": ["prazo", "entrega", "projeto", "data", "classroom"],
        "content": "O envio do projeto final deve ser realizado até 25 de Novembro às 23:59 via Google Classroom. Entregas em atraso sofrem penalidade de 1 ponto por dia."
    },
    {
        "id": "doc5",
        "title": "Configuração do Ambiente Python",
        "keywords": ["python", "env", "pip", "instalacao", "dependencias"],
        "content": "Para rodar o projeto localmente, crie um ambiente virtual com python -m venv venv, ative-o e instale as dependências com pip install python-dotenv openai."
    }
]

STOPWORDS = {
    "a", "o", "e", "de", "da", "do", "das", "dos", "em",
    "um", "uma", "para", "por", "com", "que", "na", "no",
    "as", "os", "qual", "quais", "como", "é", "são",
}

# 3. Funções de Seleção e Formatação de Contexto
def normalize_terms(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    return {term for term in text.split() if len(term) > 2 and term not in STOPWORDS}

def select_context(query, documents, max_docs=3, max_chars=1800):
    query_terms = normalize_terms(query)
    ranked = []

    for document in documents:
        searchable = " ".join([
            document["title"],
            document["content"],
            " ".join(document.get("keywords", [])),
        ])
        score = len(query_terms & normalize_terms(searchable))
        if score > 0:
            ranked.append({**document, "score": score})

    ranked.sort(key=lambda document: (-document["score"], document["id"]))

    selected = []
    used_chars = 0
    for document in ranked:
        cost = len(document["title"]) + len(document["content"])
        if selected and used_chars + cost > max_chars:
            continue
        selected.append(document)
        used_chars += cost
        if len(selected) >= max_docs:
            break

    return selected

def build_context(selected_documents):
    if not selected_documents:
        return "Nenhum documento relevante foi selecionado."

    blocks = ["<contexto>"]
    for document in selected_documents:
        blocks.append(
            f"[fonte: {document['id']} | relevância: {document['score']}]\n"
            f"{document['title']}\n{document['content']}"
        )
    blocks.append("</contexto>")
    return "\n\n".join(blocks)

# 4. Processamento da Pergunta via LLM
def responder_pergunta(query: str, max_chars: int = 1800):
    selected = select_context(query, knowledge_base, max_chars=max_chars)
    context = build_context(selected)

    messages = [
        {
            "role": "system",
            "content": (
                "Você é um assistente de estudos. Use apenas as informações dentro de <contexto>. "
                "Cite os ids das fontes quando fizer uma afirmação baseada nelas. "
                "Se o contexto não for suficiente, diga isso claramente."
            ),
        },
        {
            "role": "user",
            "content": f"{context}\n\nPergunta: {query}",
        },
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.2
    )

    fonte_ids = [doc["id"] for doc in selected]
    return response.choices[0].message.content, fonte_ids

# 5. Interface do Terminal
if __name__ == "__main__":
    print(f"=== Assistente de Estudos V2 (Modelo: {MODEL}) ===")
    print("Digite 'sair' para encerrar.\n")

    while True:
        pergunta = input("Sua pergunta: ").strip()
        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("Encerrando...")
            break

        if not pergunta:
            continue

        resposta, fontes = responder_pergunta(pergunta)
        
        print("\n--- Resposta ---")
        print(resposta)
        print(f"\n[Fontes Utilizadas: {fontes if fontes else 'Nenhuma'}]")
        print("=" * 50 + "\n")