# llm/claude_client.py
import anthropic
from config.settings import ANTHROPIC_API_KEY
from config.constants import CLAUDE_MODEL, CLAUDE_MAX_TOKENS

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """You are a helpful document assistant.
Answer questions based ONLY on the document context provided.
Each context chunk includes a page number — always cite the page number
in your answer like (Page 3) so the user can verify.

Rules:
1. Answer using ONLY the provided context
2. Always mention the page number where you found the answer
3. If the answer is not in the context, say:
   "I couldn't find this information in the uploaded document."
4. Never make up facts or guess"""


def ask_claude(question: str, context_chunks: list[dict]) -> str:
    """
    Args:
        question:       user's question string
        context_chunks: list of dicts from retriever.py
                        [{"text": "...", "page": 3, "source": "doc.pdf"}, ...]
    """
    # Build context with page numbers clearly labeled
    context_parts = []
    for chunk in context_chunks:
        context_parts.append(
            f"[Page {chunk['page']}]\n{chunk['text']}"
        )
    context = "\n\n---\n\n".join(context_parts)

    user_message = f"""Here is the relevant context from the document:

{context}

---

Based on the context above, answer this question:
{question}"""

    print(f"[claude] Sending {len(context_chunks)} chunks to Claude...")

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=CLAUDE_MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}]
    )

    answer = response.content[0].text
    print(f"[claude] Done ({response.usage.input_tokens} in / "
          f"{response.usage.output_tokens} out tokens)")
    return answer