# backend/app/utils/summarizer.py
import os
import textwrap
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chunk_text(text: str, chunk_size: int = 1500) -> list:
    return textwrap.wrap(text.strip(), width=chunk_size)

def call_llm(prompt: str, model_priority: list = None) -> str:
    if model_priority is None:
        model_priority = ["llama3-8b-8192", "mixtral-8x7b-instruct"]

    for model in model_priority:
        try:
            chat_completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=500,
            )
            print(f"✅ Used model: {model}")
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"⚠️ Model {model} failed: {e}")
            continue

    return "⚠️ All models failed. Please try again later."



def summarize_with_groq(text: str, model: str = "llama3-8b-8192") -> str:
    chunks = chunk_text(text, chunk_size=1500)

    partial_summaries = []
    for chunk in chunks:
        prompt = f"""
### TEXT CHUNK:
{chunk}

### TASK:
Write a high-quality academic summary of the text above in 90–100 words.

- Use only the content from the chunk.
- Avoid preambles, vague language, or extra detail.
- Focus on clarity and factual accuracy.

### SUMMARY:
"""
        partial = call_llm(prompt)
        partial_summaries.append(partial)

    combined_text = " ".join(partial_summaries)

    final_prompt = f"""
### PARTIAL SUMMARIES:
{combined_text}

### TASK:
Write a final full-document summary based on the above, in 130–150 words. Avoid repetition and filler.

### FINAL SUMMARY:
"""
    return call_llm(final_prompt)
