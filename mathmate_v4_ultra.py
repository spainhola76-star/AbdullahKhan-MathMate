# mathmate_v4_ultra.py
# MathMate V4 Ultra – Advanced AI Math Teacher (Python + Streamlit + Sympy)

import streamlit as st
from sympy import symbols, Eq, solve, simplify
import re

# ==========================
# UI SETTINGS
# ==========================
st.set_page_config(
    page_title="MathMate V4 Ultra",
    page_icon="🧮",
    layout="wide",
)

st.markdown(
    """
    <style>
    body { background-color: #f9f9f9; }
    .main { background: #ffffff; border-radius: 15px; padding: 20px; }
    h1, h2, h3 { color: #2c7be5; }
    .hint { color: #ff8800; font-weight: bold; }
    .answer { color: #28a745; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================
# HELPER FUNCTIONS
# ==========================
def step_by_step_addition(a, b):
    steps = [
        f"We are adding {a} + {b}.",
        f"Start with {a} and add {b}.",
        f"Final Answer: {a + b}"
    ]
    return steps, a + b

def step_by_step_subtraction(a, b):
    steps = [
        f"We are subtracting {b} from {a}.",
        f"Start with {a} and take away {b}.",
        f"Final Answer: {a - b}"
    ]
    return steps, a - b

def step_by_step_multiplication(a, b):
    steps = [
        f"We are multiplying {a} × {b}.",
        f"Multiplication is repeated addition: add {a} to itself {b} times.",
        f"Final Answer: {a * b}"
    ]
    return steps, a * b

def step_by_step_division(a, b):
    if b == 0:
        return ["Division by zero is undefined."], None
    steps = [
        f"We are dividing {a} ÷ {b}.",
        f"Division means splitting {a} into {b} equal parts.",
        f"Final Answer: {a / b}"
    ]
    return steps, a / b

def solve_equation(equation_str):
    try:
        x = symbols('x')
        lhs, rhs = equation_str.split('=')
        eq = Eq(simplify(lhs), simplify(rhs))
        sol = solve(eq, x)
        return sol
    except Exception:
        return ["Invalid equation"]

def generate_hint(problem):
    if "+" in problem:
        return "Think about combining two numbers together."
    elif "-" in problem:
        return "Think about taking away from a number."
    elif "*" in problem:
        return "Multiplication is repeated addition."
    elif "/" in problem:
        return "Division is splitting into equal groups."
    return "Break the problem into smaller steps."

def word_problem_solver(problem_text):
    problem_text = problem_text.lower()
    if "total" in problem_text or "sum" in problem_text:
        return "This looks like an addition problem."
    elif "left" in problem_text or "remain" in problem_text:
        return "This looks like a subtraction problem."
    elif "each" in problem_text and "groups" in problem_text:
        return "This looks like a multiplication problem."
    elif "share" in problem_text or "divide" in problem_text:
        return "This looks like a division problem."
    else:
        return "Let's carefully read and translate it into math first."

def answer_student_question(question):
    q = question.lower()
    if "carry over" in q:
        return "We carry over in addition when the sum in one column is 10 or more."
    elif "fractions" in q:
        return "Fractions show parts of a whole. To add them, make denominators the same first."
    elif "division" in q:
        return "Division means splitting into equal parts or groups."
    elif "algebra" in q:
        return "Algebra uses letters to stand for numbers. It helps solve unknowns."
    else:
        return "Good question! Let’s break it down step by step like a teacher would."

# ==========================
# APP LAYOUT
# ==========================
st.title("🧮 MathMate V4 Ultra")
st.subheader("Your AI Math Teacher & Study Buddy")

mode = st.sidebar.radio("Choose a Mode", [
    "AI Teacher Mode",
    "Student Helper Mode",
    "Problem Solver",
    "Word Problem Solver",
    "Student Q&A Mode"
])

# ==========================
# MODES
# ==========================
if mode == "AI Teacher Mode":
    st.header("👩‍🏫 AI Teacher Explanation")
    concept = st.text_input("Enter a concept (e.g., Addition, Fractions, Algebra)")
    if concept:
        st.write("### Teacher says:")
        st.success(answer_student_question(concept))

elif mode == "Student Helper Mode":
    st.header("✍️ Student Helper Mode")
    problem = st.text_input("Type a simple math problem (e.g., 25+37, 50-12, 6*7, 20/4)")
    if problem:
        st.info(generate_hint(problem))
        if st.button("Show Step by Step"):
            # Detect operation
            if "+" in problem:
                a, b = map(int, problem.split("+"))
                steps, result = step_by_step_addition(a, b)
            elif "-" in problem:
                a, b = map(int, problem.split("-"))
                steps, result = step_by_step_subtraction(a, b)
            elif "*" in problem:
                a, b = map(int, problem.split("*"))
                steps, result = step_by_step_multiplication(a, b)
            elif "/" in problem:
                a, b = map(int, problem.split("/"))
                steps, result = step_by_step_division(a, b)
            else:
                st.warning("Unsupported operation. Please use +, -, *, or /.")
                steps, result = [], None
            
            # Display steps
            for s in steps:
                st.write("- ", s)

elif mode == "Problem Solver":
    st.header("🧑‍💻 Problem Solver")
    eqn = st.text_input("Enter an equation (e.g., 2*x + 3 = 7)")
    if eqn:
        st.write("### Solving...")
        sol = solve_equation(eqn)
        st.success(f"Solution: {sol}")

elif mode == "Word Problem Solver":
    st.header("📚 Word Problem Solver")
    wp = st.text_area("Enter your word problem")
    if wp:
        st.info("Analyzing your word problem...")
        suggestion = word_problem_solver(wp)
        st.write("### Teacher's Tip:")
        st.success(suggestion)

elif mode == "Student Q&A Mode":
    st.header("🙋 Student Q&A Mode")
    q = st.text_input("Ask your math question (like you would to a teacher)")
    if q:
        st.write("### Teacher's Answer:")
        ans = answer_student_question(q)
        st.success(ans)
