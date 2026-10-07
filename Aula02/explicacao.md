## Experimentos e Observações (Entregável 02)

### 1. Comparação: Sem Contexto × Com Contexto

* **Sem Contexto:** Quando a pergunta é feita diretamente ao modelo sem nenhum documento anexo, a LLM fornece uma resposta genérica (ou recusa-se a responder com precisão por não ter acesso aos dados internos da instituição/disciplina). O grau de confiança factual é baixo e é impossível rastrear fontes reais.
* **Com Contexto:** Ao injetar os documentos selecionados da `knowledge_base` na mensagem de sistema e do utilizador, a resposta torna-se extremamente específica e precisa. O modelo cita diretamente os detalhes presentes nos textos (como os horários da monitoria, o laboratório exato e a fórmula de cálculo da média) e identifica corretamente os IDs das fontes utilizadas (`doc1`, `doc2`, etc.).

---

### 2. Orçamento de Contexto (`max_chars`)

* **Com `max_chars=1800`:** O limite de caracteres permite incluir todos os documentos relevantes que fizeram *match* de termos com a pergunta. A LLM recebe a informação completa e contextualizada.
* **Com `max_chars=500`:** O orçamento reduzido força a função `select_context` a descartar documentos assim que o limite de caracteres é atingido. Consequentemente, apenas os primeiros documentos ordenados por relevância entram no prompt, omitindo informações secundárias que poderiam complementar a resposta.

---

### 3. O Papel da Seleção de Contexto (Context Engineering)

A seleção de contexto (RAG) é fundamental para construir assistentes de IA eficientes e viáveis:
1. **Controlo de Custos e Latência:** Enviar apenas a informação relevante reduz drasticamente o consumo de tokens na API, diminuindo custos e acelerando o tempo de resposta do modelo.
2. **Janela de Contexto Limita:** Evita que a requisição estoure os limites de tokens impostos pelo modelo de linguagem.
3. **Mitigação de Alucinações:** Focar o modelo num conjunto restrito e factual de dados reduz o risco de invenção de informações e melhora a precisão na atribuição de fontes.