import streamlit as st
import requests

st.title("📄 Smart Research Assistant")

#------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------
for key in ["upload_response", "last_question", "last_answer", "last_snippet", "challenge_questions", "challenge_answers", "challenge_results"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "challenge_answers" else ["", "", ""]

# ------------------------------------------
# FILE UPLOAD + SUMMARY
# ------------------------------------------

uploaded_file = st.file_uploader("Upload a PDF or TXT file:", type=["pdf", "txt"])

if uploaded_file and st.button("Upload and Summarize"):
    with st.spinner("Processing..."):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post("http://127.0.0.1:8000/upload/", files={"file": uploaded_file})
        if response.status_code == 200:
            st.session_state.upload_response = response.json()
        else:
            st.error("❌ Upload failed.")

if st.session_state.upload_response:
    st.subheader("📝 Auto Summary")
    st.write(st.session_state.upload_response["summary"])
    st.subheader("🔍 Extracted Text Preview")
    st.text_area("Preview", st.session_state.upload_response["text"], height=200)


# -------------------------------------------
# ASK ANYTHING
# -------------------------------------------
st.header("💬 Ask Anything")

user_question = st.text_input("Ask a question based on the uploaded document:")

if st.button("Get Answer") and user_question:
    with st.spinner("Thinking..."):
        try:
            res = requests.post("http://127.0.0.1:8000/ask/", json={"question": user_question})
            if res.status_code == 200:
                data = res.json()
                st.session_state.last_question = user_question
                st.session_state.last_answer = data["answer"]
                st.session_state.last_snippet = data.get("supporting_snippet", "")
            else:
                st.error("⚠️ Could not get an answer.")
        except Exception as e:
            st.error(f"Server error: {e}")

if st.session_state.last_answer:
    st.markdown(f"**Answer:** {st.session_state.last_answer}")
    if st.session_state.last_snippet:
        st.markdown("📌 **Supporting Snippet:**")
        st.markdown(
            f"""
<div style='
    background-color: #1e1e1e;
    padding: 1rem;
    border-radius: 0.5rem;
    color: #f1f1f1;
    line-height: 1.6;
    font-size: 0.95rem;
    white-space: normal;
    word-wrap: break-word;
    border-left: 4px solid #9b59b6;
'>
{st.session_state.last_snippet.strip()}
</div>
""",
            unsafe_allow_html=True
        )
        st.caption("This excerpt was selected from the document as the basis for the answer above.")




# -------------------------------------------
# CHALLENGE ME
# -------------------------------------------
st.header("🧠 Challenge Me")

if st.button("Generate Questions"):
    if not st.session_state.upload_response:
        st.warning("⚠️ Please upload a document first.")
    else:
      with st.spinner("Generating..."):
        res = requests.get("http://127.0.0.1:8000/challenge/")
        if res.status_code == 200:
            st.session_state.challenge_questions = res.json()["questions"]
            st.session_state.challenge_answers = ["", "", ""]
            st.session_state.challenge_results = None
        else:
            st.error("❌ Couldn't generate questions.")

if st.session_state.challenge_questions:
    st.markdown("### ✍️ Your Answers:")
    for i, q in enumerate(st.session_state.challenge_questions):
        st.markdown(f"**Q{i+1}:** {q}")
        st.session_state.challenge_answers[i] = st.text_area(
            f"Your Answer {i+1}",
            value=st.session_state.challenge_answers[i],
            key=f"answer_{i}"
        )

    
    if st.button("Submit Answers"):
        if not st.session_state.upload_response:
            st.warning("⚠️ Please upload a document first.")
        else:
            with st.spinner("Evaluating your answers..."):
                res = requests.post(
                    "http://127.0.0.1:8000/challenge/evaluate/",
                    json={"answers": st.session_state.challenge_answers}
                )
                if res.status_code == 200:
                    st.session_state.challenge_results = res.json()
                else:
                    st.error("❌ Evaluation failed.")



if st.session_state.challenge_results:
    results = st.session_state.challenge_results

    # for testing purpose----------
    # st.subheader("🧪 Raw Evaluation Response")
    # st.json(results)  

    if isinstance(results, dict) and "evaluations" in results and isinstance(results["evaluations"], list):
        st.markdown("### 📊 Results")

        for idx, result in enumerate(results["evaluations"]):
            if isinstance(result, dict) and "feedback" in result and "correct_answer" in result:
                st.markdown(f"**Q{idx+1}:**")
                st.markdown(f"📝 **Justification:** _{result['feedback']}_")
                st.markdown(f"✅ **Ideal Answer:** {result['correct_answer']}")
            else:
                st.warning(f"⚠️ Skipped Q{idx+1}: Invalid format.")
    elif "error" in results:
        st.error(f"❌ {results['error']}")
    else:
        st.error("⚠️ Unexpected response format.")
