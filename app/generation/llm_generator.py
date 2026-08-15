import ollama
 
MODEL_NAME = "minimax-m3:cloud"
 
SYSTEM_PROMPT = """You are a helpful assistant that answers questions strictly based on the provided context.
 
Rules:
- Only use information from the given context to answer.
- If the answer is not in the context, say "I don't have this information in the provided documents."
- Always mention which page(s) the answer came from.
- Do not make up information that is not in the context.
"""
 
 
def build_context(chunks):
    context_parts = []
    for chunk in chunks:
        payload = chunk["payload"]
        context_parts.append(
            f"[Page {payload['page_number']}]\n{payload['text']}"
        )
    return "\n\n---\n\n".join(context_parts)
 
 
def generate_answer(query: str, chunks: list, conversation_history: list = None) -> str:
    context = build_context(chunks)
 
    user_message = f"""Context:
{context}
 
Question: {query}
 
Answer the question using only the context above."""
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if conversation_history:
        for turn in conversation_history[-3:]:
            messages.append({"role": "user", "content": turn["question"]})
            messages.append({"role": "assistant", "content": turn["answer"]})

    messages.append({"role": "user", "content": user_message})
 
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
 
    return response["message"]["content"]

def generate_answer_stream(query: str, chunks: list, conversation_history: list = None):
    context = build_context(chunks)

    user_message = f"""Context:
{context}

Question: {query}

Answer the question using only the context above."""

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if conversation_history:
        for turn in conversation_history[-3:]:
            messages.append({"role": "user", "content": turn["question"]})
            messages.append({"role": "assistant", "content": turn["answer"]})

    messages.append({"role": "user", "content": user_message})

    stream = ollama.chat(
        model=MODEL_NAME,
        messages=messages,
        stream=True,
    )

    for chunk in stream:
        yield chunk["message"]["content"]
 
if __name__ == "__main__":
    import sys
    import os
 
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "retrieval"))
    from reranker import search_with_rerank
 
    print("RAG chat ready. Type a question (or 'exit' to quit).\n")
 
    while True:
        query = input("Your question: ")
        if query.lower() == "exit":
            break
 
        chunks = search_with_rerank(query, retrieve_k=10, final_k=5)
        answer = generate_answer(query, chunks)
 
        print("\nAnswer:\n")
        print(answer)
        print()