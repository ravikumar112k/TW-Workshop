# test.py
import os
import json
import time
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv

import openai
import streamlit as st

st.set_page_config(page_title="Pre-assessment Test", page_icon="📝", layout="wide")

# ====== CONFIG ======
APP_TITLE = "AI-Powered Adaptive Test"
DEFAULT_LEVELS = ["Easy", "Medium", "Hard"]
NUM_MCQ = 5
NUM_SA = 5
SAVE_RESULTS = True

# Load variables from .env
load_dotenv()

# ====== LLM CLIENT (OpenAI) ======
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY", None)

    if not api_key:
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except Exception:
            api_key = None

    if not api_key:
        return None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        def chat(messages: List[Dict[str, str]], model: str = "gpt-4o-mini", response_format: str = None) -> str:
            kwargs = dict(model=model, messages=messages)
            if response_format == "json":
                kwargs["response_format"] = {"type": "json_object"}
            resp = client.chat.completions.create(**kwargs)
            return resp.choices[0].message.content

        return chat
    except Exception as e:
        st.warning(f"OpenAI client unavailable: {e}")
        return None

OPENAI_CHAT = get_openai_client()

# ====== PROMPTS ======
QUESTION_GEN_SYSTEM = """You are an expert exam setter. You produce concise, accurate questions.
Output STRICT JSON with this schema:
{{
  "mcq": [
    {{"question": "string", "options": ["A","B","C","D"], "answer_index": 0, "explanation": "why the correct is correct"}}
  ],
  "short_answers": [
    {{"question": "string (can include a short passage/prompt)", "expected_answer": "high-level ideal answer"}}
  ]
}}
- Create exactly {num_mcq} MCQs and {num_sa} short-answer questions.
- Difficulty: {difficulty}. Course: {course}.
- MCQs must have 4 options and exactly one correct answer_index (0..3).
- Keep questions self-contained and unambiguous.
"""

EVAL_SA_SYSTEM = """You are a strict grader.
Given a student's short answer and the expected answer, grade it strictly between 0.0 and 1.0.
Provide concise reasoning.
Return STRICT JSON array of objects, one per short answer:
[
  {
    "score": 0.0-1.0,
    "feedback": "short actionable feedback",
    "missing_points": ["key concept 1", "key concept 2"]
  }
]
"""

SUMMARY_SYSTEM = """You are a learning coach.
Given per-question evaluation results and the course/difficulty, produce:

- 3 bullet strengths
- 3 bullet areas to improve
- 3 recommended next topics/resources (generic, not links)

Return in clean markdown (no code fences, no JSON)."""

# ====== UTILITIES ======
def safe_json_loads(s: str) -> Any:
    try:
        return json.loads(s)
    except Exception:
        start = s.find("{")
        end = s.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(s[start:end+1])
            except Exception:
                pass
        raise

def keyword_grade(student_answer: str, expected: str) -> Tuple[float, List[str], str]:
    sa = (student_answer or "").lower()
    exp = (expected or "").lower()
    tokens = [t.strip(".,:;!?()[]{}\"'") for t in exp.split()]
    kws = {t for t in tokens if len(t) >= 5}
    if not kws:
        return (0.5 if sa.strip() else 0.0, [], "Answer length/clarity could be improved. Include key concepts.")
    hits = sum(1 for k in kws if k in sa)
    score = hits / max(1, len(kws))
    missing = [k for k in kws if k not in sa]
    feedback = "Covers some key ideas." if score >= 0.5 else "Missing several key ideas; expand with definitions and examples."
    return (round(score, 2), missing[:5], feedback)

def ensure_attempts_dir():
    if SAVE_RESULTS:
        os.makedirs("attempts", exist_ok=True)

def save_attempt(payload: Dict[str, Any]):
    if not SAVE_RESULTS:
        return
    ensure_attempts_dir()
    ts = int(time.time())
    fname = f"attempts/attempt_{ts}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

# ====== STREAMLIT UI ======
# Get the course from session state
course = st.session_state.get("selected_category", "Unknown")
st.title(f"📝 Pre-assessment for {course}")
st.caption(f"Course/Subject: {course}")

with st.sidebar:
    st.header("Setup")
    student_name = st.text_input("Student name (optional)", "")
    st.markdown(f"**Course:** {course}")
    difficulty = st.selectbox("Difficulty", DEFAULT_LEVELS, index=0)
    st.divider()
    use_llm = st.toggle(
        "Use LLM for generation/grading",
        value=OPENAI_CHAT is not None,
        help="If off (or no API key), uses rule-based fallback for grading and demo questions."
    )
    model_hint = st.text_input("Model (OpenAI)", "gpt-4o-mini")
    st.caption("Set OPENAI_API_KEY in environment or st.secrets.")

colA, colB = st.columns([1, 1])

# Session state
if "questions" not in st.session_state:
    st.session_state.questions = None
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "graded" not in st.session_state:
    st.session_state.graded = None

# ====== QUESTION GENERATION ======
def generate_questions(course: str, difficulty: str) -> Dict[str, Any]:
    if use_llm and OPENAI_CHAT:
        sys = QUESTION_GEN_SYSTEM.format(num_mcq=NUM_MCQ, num_sa=NUM_SA, difficulty=difficulty, course=course)
        msg = [{"role": "system", "content": sys}]
        raw = OPENAI_CHAT(msg, model=model_hint, response_format="json")
        data = safe_json_loads(raw)
        return data
    # Fallback demo
    mcq = []
    for i in range(NUM_MCQ):
        mcq.append({
            "question": f"[DEMO] {course} {difficulty}: Which option best fits item {i+1}?",
            "options": ["Alpha", "Bravo", "Charlie", "Delta"],
            "answer_index": (i % 4),
            "explanation": "In this demo, correctness alternates by index."
        })
    sa = []
    for i in range(NUM_SA):
        sa.append({
            "question": f"[DEMO] Briefly explain the core idea of topic {i+1} in {course}. Include one example.",
            "expected_answer": f"In {course}, topic {i+1} focuses on fundamental principles and an example usage."
        })
    return {"mcq": mcq, "short_answers": sa}

with colA:
    if st.button("📝 Generate Test", type="primary"):
        st.session_state.questions = generate_questions(course, difficulty)
        st.session_state.answers = {}
        st.session_state.graded = None

# ====== RENDER QUESTIONS ======
if st.session_state.questions:
    qdata = st.session_state.questions
    st.subheader("Part A: Multiple Choice (5 questions)")
    for i, q in enumerate(qdata["mcq"]):
        st.markdown(f"**Q{i+1}. {q['question']}**")
        key = f"mcq_{i}"
        st.session_state.answers[key] = st.radio(
            label=f"Choose for Q{i+1}",
            options=[0,1,2,3],
            format_func=lambda idx, opts=q["options"]: f"{chr(65+idx)}. {opts[idx]}",
            key=key
        )

    st.subheader("Part B: Short Answers (5 questions)")
    for i, q in enumerate(qdata["short_answers"]):
        st.markdown(f"**Q{i+1+NUM_MCQ}. {q['question']}**")
        key = f"sa_{i}"
        st.session_state.answers[key] = st.text_area("Your answer:", key=key, height=120)

    st.divider()
    if st.button("✅ Submit & Grade", type="primary"):
        # ====== GRADING ======
        mcq_results = []
        correct_mcq = 0
        for i, q in enumerate(qdata["mcq"]):
            chosen = st.session_state.answers.get(f"mcq_{i}", None)
            is_correct = (chosen == q["answer_index"])
            if is_correct: correct_mcq += 1
            mcq_results.append({
                "question": q["question"],
                "chosen_index": chosen,
                "correct_index": q["answer_index"],
                "options": q["options"],
                "is_correct": bool(is_correct),
                "explanation": q.get("explanation", "")
            })

        sa_results = []
        for i, q in enumerate(qdata["short_answers"]):
            s = st.session_state.answers.get(f"sa_{i}", "")
            sc, miss, fb = keyword_grade(s, q["expected_answer"])
            sa_results.append({
                "question": q["question"],
                "student_answer": s,
                "expected_answer": q["expected_answer"],
                "score": sc,
                "feedback": fb,
                "missing_points": miss
            })

        total_sa = len(sa_results)
        avg_sa = round(sum(r["score"] for r in sa_results) / max(1, total_sa), 2)
        grade_payload = {
            "student": student_name or "Anonymous",
            "course": course,
            "difficulty": difficulty,
            "mcq": mcq_results,
            "sa": sa_results,
            "mcq_score": f"{correct_mcq}/{len(mcq_results)}",
            "sa_avg": avg_sa,
            "summary": "",
            "timestamp": int(time.time())
        }
        st.session_state.graded = grade_payload
        save_attempt(grade_payload)

# ====== RESULTS VIEW ======
if st.session_state.graded:
    res = st.session_state.graded
    st.success("Assessment complete!")
    mcq_correct = sum(1 for m in res["mcq"] if m["is_correct"])
    st.metric("MCQ Score", f"{mcq_correct}/{len(res['mcq'])}")
    st.metric("Short Answer Avg", f"{res['sa_avg']:.2f}")

    st.subheader("📈 Personalized Feedback & Next Steps")
    strengths = []
    if mcq_correct >= 4:
        strengths.append("Strong conceptual recall on objective items.")
    if res["sa_avg"] >= 0.7:
        strengths.append("Short answers show good coverage of key ideas.")
    if not strengths:
        strengths.append("Consistent effort; baseline understanding established.")
    improvements = [
        "Revise foundational definitions and common pitfalls.",
        "Practice explaining concepts concisely with examples.",
        "Attempt more mixed-difficulty questions to build confidence."
    ]
    st.markdown(
        "- **Strengths:** " + "; ".join(strengths) + "\n"
        "- **Areas to Improve:** " + "; ".join(improvements) + "\n"
        "- **Next Steps:** 1) Review notes; 2) Solve 20 practice MCQs; "
        "3) Write brief explanations for 5 core topics; 4) Retake a test; 5) Track mistakes."
    )
    st.download_button(
        "Download Attempt JSON",
        data=json.dumps(st.session_state.graded, ensure_ascii=False, indent=2),
        file_name=f"{res['student']}_{course}_{difficulty}_attempt.json",
        mime="application/json",
        use_container_width=True
    )

# ====== FOOTER ======
st.divider()
st.caption("Tip: Toggle LLM off to demo without an API key. Add your key for better generation & grading.")
