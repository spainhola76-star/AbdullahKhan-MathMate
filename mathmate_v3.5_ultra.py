# mathmate_v3_ultra.py
# MathMate V3 Ultra - AI Teacher + Solver + Student Helper
# Streamlit + Sympy

import streamlit as st
from sympy import symbols, Eq, solve, simplify
import re

# ==========================
# PAGE SETTINGS
# ==========================
st.set_page_config(
    page_title="MathMate V3 Ultra",
    page_icon="🧮",
    layout="wide",
)

st.title("🧮 MathMate V3 Ultra")
st.markdown("### Your AI Teacher, Solver & Study Buddy")

# ==========================
# HELPER FUNCTIONS
# ==========================
def step_by_step_solver(expr_str):
    x = symbols('x')
    steps = []

    try:
        # Try to detect equations like "2x + 3 = 7"
        if "=" in expr_str:
            left, right = expr_str.split("=")
            equation = Eq(simplify(left), simplify(right))
            steps.append(f"Equation detected: {equation}")

            solution = solve(equation, x)

            steps.append("Step 1: Rearrange terms to isolate variable.")
            steps.append("Step 2: Simplify both sides.")
            steps.append("Step 3: Solve for the unknown.")

            return solution, steps
        else:
            # Just a normal expression
            simplified = simplify(expr_str)
            steps.append(f"Simplifying expression: {expr_str}")
            steps.append(f"Result: {simplified}")
            return simplified, steps
    except Exception as e:
        return None, [f"❌ Error: {e}"]

def give_hint(expr_str):
    if "=" in expr_str:
        return "👉 Try moving terms with 'x' to one side and numbers to the other."
    elif "+" in expr_str:
        return "👉 Add similar terms together."
    elif "*" in expr_str:
        return "👉 Multiply step by step."
    else:
        return "👉 Break it into smaller steps."

# ==========================
# APP LAYOUT
# ==========================
mode = st.sidebar.selectbox("Choose Mode:", ["AI Solver", "AI Teacher", "Student Helper"])

problem = st.text_input("✏️ Enter your math problem (e.g., 2x + 3 = 7):")

if problem:
    solution, steps = step_by_step_solver(problem)

    if mode == "AI Solver":
        st.subheader("🔹 Solution")
        st.write(solution)

    elif mode == "AI Teacher":
        st.subheader("📘 Step-by-Step Explanation")
        for i, step in enumerate(steps, 1):
            st.markdown(f"**Step {i}:** {step}")
        st.success(f"✅ Final Answer: {solution}")

    elif mode == "Student Helper":
        st.subheader("🤝 Student Helper")
        st.markdown("Here’s a hint to get you started:")
        st.info(give_hint(problem))

        with st.expander("Show Step-by-Step Solution"):
            for i, step in enumerate(steps, 1):
                st.markdown(f"**Step {i}:** {step}")
            st.success(f"✅ Final Answer: {solution}")
