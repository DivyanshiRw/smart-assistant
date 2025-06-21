from groq import Groq
import os
from dotenv import load_dotenv
from app.utils.qa import chunk_text, call_groq  # reusing chunking and Groq client

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------------------------------
# QUESTION GENERATION
# ---------------------------------------

def generate_questions(document: str) -> list:
    prompt = f"""
You are a research assistant.

Your task is to generate 3 challenging and inferential questions using ONLY the content from the document below. Do not introduce any topics that are not explicitly mentioned in the document.

- Focus on reasoning, interpretation, or application of what's present in the text.
- Avoid factual recall or generic questions.
- Do NOT ask about terms or topics that do not appear in the document.
- Make sure each question is directly answerable from the document.

### DOCUMENT:
{document[:6000]}

### QUESTIONS:
1.
2.
3.

"""
    output = call_groq(prompt)

    return [
        line.strip()[2:].strip()
        for line in output.splitlines()
        if line.strip().startswith("1.") or line.strip().startswith("2.") or line.strip().startswith("3.")
    ]



# ----------------------------------------
# EVALUATION
# ----------------------------------------

def evaluate_answers(document: str, user_answers: list[str]) -> dict:
    chunks = chunk_text(document)
    context = " ".join(chunks[:3])  # Use first few chunks for safe context

    evaluations = []

    for i, answer in enumerate(user_answers):
        prompt = f"""
You are an academic evaluator.

### CONTEXT:
{context}

### USER ANSWER:
{answer}

### EVALUATION TASK:
Evaluate the answer using only the document context. Do not rely on external knowledge. Your response should include:

- A concise justification explaining whether the answer reflects the document accurately.
- The ideal or correct answer from the document context in ≤2 sentences.

Respond only in the following format:

FEEDBACK: <brief explanation referring to specific concept or section>  
CORRECT_ANSWER: <ideal answer>
"""

        output = call_groq(prompt)

        if not isinstance(output, str) or not output.strip():
            output = "FEEDBACK: No valid output.\nCORRECT_ANSWER: Unavailable."

        try:
            lines = [line.strip() for line in output.strip().splitlines()]
            feedback_line = next((l for l in lines if l.startswith("FEEDBACK:")), "")
            correct_line = next((l for l in lines if l.startswith("CORRECT_ANSWER:")), "")

            feedback = feedback_line.replace("FEEDBACK:", "").strip() or "No feedback."
            correct = correct_line.replace("CORRECT_ANSWER:", "").strip() or "Not provided."
        except Exception as e:
            feedback = f"Parsing error: {str(e)}"
            correct = "Unavailable"

        evaluations.append({
            "feedback": feedback,
            "correct_answer": correct
        })

    # Final fallback in case Groq failed
    if not evaluations or not isinstance(evaluations, list):
        return {"error": "Evaluation failed or invalid format."}

    return {
        "evaluations": evaluations
    }
