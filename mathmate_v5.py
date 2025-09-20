# mathmate_v5.py
import streamlit as st
import random
import openai

# =======================
# OpenAI API Configuration
# =======================
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your key

def get_ai_explanation(question, user_answer=None):
    """
    Ask OpenAI to explain the answer in a fun, step-by-step way for kids
    """
    prompt = f"""
You are a super fun, friendly math tutor for kids. 
Explain the answer to this problem step by step in a funny, happy, emoji-filled way.
Problem: {question}
User answer: {user_answer if user_answer is not None else "None"}
Make it clear and educational like a story, and guide the kid to understand.
"""
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=250
    )
    return response.choices[0].text.strip()

# =======================
# App Configuration
# =======================
st.set_page_config(
    page_title="MathMate V5 🧮",
    page_icon="🎉",
    layout="wide",
)

st.markdown("""
    <style>
    .stApp {background-color: #ffffff;}
    h1 {color: #2E8B57; font-family: 'Comic Sans MS', sans-serif; font-size: 60px;}
    p {color: #2E8B57; font-family: 'Comic Sans MS', sans-serif; font-size: 24px;}
    .stButton button {background-color: #2E8B57; color: white; font-size: 24px;}
    </style>
""", unsafe_allow_html=True)

# =======================
# User Info & Points
# =======================
if "points" not in st.session_state:
    st.session_state.points = 0
if "history" not in st.session_state:
    st.session_state.history = []

st.title("MathMate V5 🧮")
st.write(f"Points: {st.session_state.points} 🎯")

# =======================
# Sample Word Problems (Grades 1–5)
# =======================
word_problems = [
    {"question": "Ali has 4 pencils ✏️, and his friend gives him 3 more. How many pencils does he have now?", "answer": 7},
    {"question": "Sara had 18 pencils. She gave 6 to her friend and then bought 4 more. How many pencils does she have now?", "answer": 16},
    {"question": "If a pizza is cut into 4 slices and you eat 1 slice, how many slices are left?", "answer": 3},
    {"question": "Multiply 7 × 8. Be careful! Some students forget the 7s table.", "answer": 56},
    {"question": "Divide 29 pencils among 4 students. How many pencils does each get and how many are left?", "answer": "7 each, 1 leftover"},
    {"question": "Shade half of 12 circles. How many should be shaded?", "answer": 6},
    {"question": "Which is bigger: 102 or 99?", "answer": 102},
    {"question": "A rectangle is 8 cm long and 5 cm wide. What is its perimeter and its area?", "answer": "Perimeter: 26 cm, Area: 40 cm²"},
]

problem = random.choice(word_problems)
st.subheader("Try this problem:")
st.write(problem["question"])

# =======================
# User Input
# =======================
user_answer = st.text_input("Your Answer:")

if st.button("Check Answer ✅"):
    correct = str(user_answer).strip() == str(problem["answer"])
    
    # Get AI explanation
    ai_explanation = get_ai_explanation(problem["question"], user_answer)
    
    if correct:
        st.success(f"🎉 Correct! {ai_explanation}")
        st.session_state.points += 10
    else:
        st.error(f"❌ Oops! The correct answer is {problem['answer']}. {ai_explanation}")

    # Save to history
    st.session_state.history.append({
        "question": problem["question"],
        "your_answer": user_answer,
        "correct_answer": problem["answer"]
    })

# =======================
# Memory / History
# =======================
st.write("### Your Previous Problems:")
for h in st.session_state.history[-5:]:
    st.write(f"Q: {h['question']}")
    st.write(f"Your Answer: {h['your_answer']} | Correct: {h['correct_answer']} ✅")

# =======================
# Ideas for Next Upgrades:
# - Mini-games: counting shapes, drag-and-drop
# - Levels for Grades 1–5
# - Custom avatars and animations
# - Emoji rewards 🎈🍎
# - Adaptive difficulty using AI
