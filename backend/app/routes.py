# backend/app/routes.py
from fastapi import APIRouter, File, UploadFile
from app.utils.parser import parse_document
from app.utils.summarizer import summarize_with_groq
from app.state import DOCUMENT_STORE
from fastapi import Request
from pydantic import BaseModel
from app.utils.qa import answer_question
from app.utils.challenge import generate_questions, evaluate_answers


router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    filename = file.filename
    text = parse_document(contents, filename)

    # Store full text in memory
    DOCUMENT_STORE["text"] = text

    summary = summarize_with_groq(text)
    return {
        "filename": filename,
        "text": text[:1000],
        "summary": summary
    }

class QARequest(BaseModel):
    question: str

@router.post("/ask/")
async def ask_question(data: QARequest):
    document = DOCUMENT_STORE.get("text", "")
    if not document:
        return {"error": "No document uploaded."}

    return answer_question(document, data.question)


class AnswerEvaluation(BaseModel):
    answers: list[str]

@router.get("/challenge/")
async def get_challenge_questions():
    document = DOCUMENT_STORE.get("text", "")
    if not document:
        return {"error": "No document uploaded"}
    
    questions = generate_questions(document)
    return {"questions": questions}

@router.post("/challenge/evaluate/")
async def evaluate_user_answers(payload: AnswerEvaluation):
    document = DOCUMENT_STORE.get("text", "")
    if not document:
        return {"error": "No document uploaded"}

    return evaluate_answers(document, payload.answers)
