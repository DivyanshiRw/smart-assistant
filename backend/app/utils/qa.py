from groq import Groq
import os
from dotenv import load_dotenv
import textwrap
import re


def clean_and_tokenize(text):
    return re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())  # only words ≥3 letters

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chunk_text(text: str, chunk_size: int = 1500):
    return textwrap.wrap(text.strip(), width=chunk_size)

def call_groq(prompt: str, model_priority: list = None):
    if model_priority is None:
        model_priority = ["llama3-8b-8192", "mixtral-8x7b-instruct"]

    for model in model_priority:
        try:
            res = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )
            print(f"✅ Used model: {model}")
            return res.choices[0].message.content.strip()
        except Exception as e:
            print(f"⚠️ Model {model} failed: {e}")
            continue

    return "⚠️ All models failed. Please try again later."


def answer_question(document: str, question: str):
    chunks = chunk_text(document)
    keywords = clean_and_tokenize(question)

    best_chunk = ""
    best_score = 0

    for chunk in chunks:
        chunk_text_lower = chunk.lower()
        score = sum(chunk_text_lower.count(word) for word in keywords)
        if score > best_score:
            best_chunk = chunk
            best_score = score

    prompt = f"""
You are an intelligent academic assistant. Your job is to answer a research-based question using **only the excerpt below**.

### DOCUMENT EXCERPT:
{best_chunk}

### QUESTION:
{question}

### INSTRUCTIONS:
- Base your answer only on the document excerpt. Do NOT use outside knowledge.
- If the answer is clearly stated, extract it accurately.
- If the answer is partially present, explain what can be inferred.
- If the answer is not present at all, say: "This information is not available in the provided excerpt."
- Be concise, factual, and neutral.

- After the answer, include a justification by pointing to the relevant **heading or paragraph**, e.g.:
  - "Under the heading Peer-to-Peer Networks, second paragraph"
  - or "In the final paragraph of the excerpt"

### RESPONSE FORMAT:
Answer: <your answer>  
Justification: <reference to heading/paragraph + brief reason>
"""

    answer = call_groq(prompt)

    return {
        "answer": answer,
        "supporting_snippet": best_chunk  
    }