# Smart Research Assistant 📄
This is a Streamlit + FastAPI based LLM-powered assistant that can:

* Automatically summarize any uploaded document.
* Answer deep, contextual questions with justifications.
* Challenge users with reasoning-based questions and evaluate their responses.

---
## 🔧 Features

- ✅ Upload PDF/TXT documents
- ✅ Auto-summarization
- ✅ Ask document-based questions and receive justified answers
- ✅ Challenge mode: Get logical questions → Submit answers → Receive feedback with correct responses
- ✅ Highlight supporting document snippet
- 🧠 Uses [Groq](https://groq.com/) API to run powerful open-source LLMs like LLaMA 3 and Mixtral

---

## 📁 Project Structure

```
smart-assistant/
│
├── backend/
│ ├── app/
│ │ ├── utils/
│ │ │ ├── qa.py                # QA logic (ask anything)
│ │ │ ├── challenge.py         # Challenge mode (Q&A evaluation)
│ │ │ ├── parser.py            # Document parsing (PDF/TXT)
│ │ │ ├── summarizer.py        # Auto-summary
| | |── routes.py              # API endpoints
│ │ ├── main.py                # FastAPI app instance
│ │ ├── state.py               # Global document memory
│── .env                       # Environment file (Groq API key) - > ⚠️ `.env` is excluded from Git.
├── requirements.txt
|
├── frontend/
| |── requirements.txt
│ ├── streamlit_app.py # Streamlit UI
│
├── Sample Outputs
|
├── venv
|
└── README.md 
```

---

## 📦 Setup & Installation

### 1. 🔑 Get a Groq API Key

1. Go to: [https://console.groq.com/keys](https://console.groq.com/keys)
2. Create an account (if needed)
3. Generate an API Key
4. Create a file named `.env` in the root of your project:
```
GROQ_API_KEY=your_key_here
```


---

### 2. 📦 Install Dependencies

Use **Python 3.9+**. Recommended to create a virtual environment:

Open new terminal on your editor.

```bash
# Create and activate venv (Windows)
python -m venv venv
& .\venv\Scripts\Activate.ps1

# OR on Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Then install:
pip install -r requirements.txt

```


### 3. 🚀 Run the Backend
```bash
cd backend
uvicorn app.main:app --reload
```
API will be live at: http://127.0.0.1:8000

### 4. 🖥️ Run the Frontend
```bash
cd frontend
streamlit run streamlit_app.py
```
Open the UI at: http://localhost:8501


## 💡 Usage Instructions
### Upload & Summarize
* Upload a PDF or TXT file.
* The assistant summarizes and shows text preview.

### Ask Anything
* Type your question → Get a clear answer with justification.
* Supporting snippet shown directly.

### Challenge Me
* Click "Generate Questions" → Answer them → Submit.
* System evaluates your logic and gives:
Feedback,
 Ideal answer

### 🌟 Bonus Feature:
📌 Answer Highlighting: Shows document snippet used for answer



## 🧪 Models Used
Via Groq API:

* llama3-8b-8192
* mixtral-8x7b-instruct

## 🧠 Tech Stack
* Backend: FastAPI    ![FastAPI](https://img.shields.io/badge/Backend-FastAPI-teal)
* Frontend: Streamlit ![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-orange)
* LLM API: Groq       ![Groq](https://img.shields.io/badge/LLM-Groq_LLaMA3-red)

---
# 📌 Project Objective:
This project is built as part of a task designed to assess the ability to go beyond basic automation and demonstrate contextual understanding, logical reasoning, and applied GenAI capabilities.

### 🎯 Objective:
The goal was to build an AI-powered assistant that is document-aware and capable of:

* Accurately answering free-form questions grounded in document content.
* Generating logical, inference-based questions from the document.
* Evaluating user-submitted answers with justifications from the source.
* Providing a concise summary upon upload.

### ✅ Functional Highlights:
* Ask Anything: Users can ask any question. The assistant finds the most relevant context and gives a precise answer with document-based justification.
* Challenge Me: The system generates 3 thought-provoking questions. It evaluates the user's answers, gives feedback, and shows the ideal response.
* Auto Summary: Displays a short summary (≤150 words) as soon as a document is uploaded.
* Justified Responses: Every response is backed by a referenced snippet or paragraph.
* Answer Highlighting (Bonus Feature Implemented): Visually shows the document excerpt that the answer is based on.


### 🖼 Sample Outputs

Screenshots demonstrating key features (summary, QA, evaluation, etc.) are available in the [`Sample_Outputs/`](./Sample_Outputs) folder.


