# mathmate_v2_advanced.py
# Advanced MathMate V2+ for Primary School (Python + Streamlit)
# White & Green theme, Duolingo-inspired, smarter AI

import streamlit as st
from sympy import symbols, Eq, solve
import re
import random

# ==========================
# UI THEME SETTINGS
# ==========================
st.set_page_config(
    page_title="MathMate V2+",
    page_icon="🧮",
    layout="wide",
)

st.markdown("""
<style>
body {background-color: #ffffff; color: #333333;}
.stButton>button {background-color: #00cc44; color: white; font-weight: bold;}
.stTextInput>div>div>input {border: 2px solid #00cc44; border-radius: 8px; padding: 8px;}
.step {background-color:#e0ffe0; padding:5px; border-radius:5px; margin:5px 0;}
</style>
""", unsafe_allow_html=True)

st.title("🧮 MathMate V2+")
st.subheader("Primary School Math, Multi-Step & Smarter AI!")

# ==========================
# PROBLEM TYPES
# ==========================
problem_type = st.radio(
    "Choose Problem Type:",
    ("Addition", "Subtraction", "Multiplication", "Division", "Word Problem", "Random Problem")
)

# ==========================
# HELPER FUNCTIONS
# ==========================

def multi_step_addition(a, b):
    st.markdown("<div class='step'>Step 1: Break numbers into tens and ones</div>", unsafe_allow_html=True)
    tens_a, ones_a = divmod(a, 10)
    tens_b, ones_b = divmod(b, 10)
    st.write(f"{a} = {tens_a*10} + {ones_a}")
    st.write(f"{b} = {tens_b*10} + {ones_b}")
    
    st.markdown("<div class='step'>Step 2: Add tens and ones separately</div>", unsafe_allow_html=True)
    tens_sum = tens_a*10 + tens_b*10
    ones_sum = ones_a + ones_b
    st.write(f"Tens sum: {tens_sum}, Ones sum: {ones_sum}")
    
    st.markdown("<div class='step'>Step 3: Combine for final answer</div>", unsafe_allow_html=True)
    total = tens_sum + ones_sum
    st.success(f"Answer: {total}")
    return total

def multi_step_subtraction(a, b):
    st.markdown("<div class='step'>Step 1: Break numbers into tens and ones</div>", unsafe_allow_html=True)
    tens_a, ones_a = divmod(a, 10)
    tens_b, ones_b = divmod(b, 10)
    st.write(f"{a} = {tens_a*10} + {ones_a}")
    st.write(f"{b} = {tens_b*10} + {ones_b}")
    
    st.markdown("<div class='step'>Step 2: Subtract ones and tens separately</div>", unsafe_allow_html=True)
    if ones_a < ones_b:
        ones_a += 10
        tens_a -= 1
    ones_diff = ones_a - ones_b
    tens_diff = tens_a*10 - tens_b*10
    st.write(f"Tens diff: {tens_diff}, Ones diff: {ones_diff}")
    
    st.markdown("<div class='step'>Step 3: Combine for final answer</div>", unsafe_allow_html=True)
    total = tens_diff + ones_diff
    st.success(f"Answer: {total}")
    return total

def multi_step_multiplication(a, b):
    st.markdown("<div class='step'>Step 1: Split numbers into tens and ones</div>", unsafe_allow_html=True)
    tens_a, ones_a = divmod(a, 10)
    tens_b, ones_b = divmod(b, 10)
    st.write(f"{a} = {tens_a*10} + {ones_a}, {b} = {tens_b*10} + {ones_b}")
    
    st.markdown("<div class='step'>Step 2: Multiply parts separately</div>", unsafe_allow_html=True)
    part1 = tens_a * tens_b * 100
    part2 = tens_a * ones_b * 10
    part3 = ones_a * tens_b * 10
    part4 = ones_a * ones_b
    st.write(f"Products: {part1}, {part2}, {part3}, {part4}")
    
    st.markdown("<div class='step'>Step 3: Add all parts</div>", unsafe_allow_html=True)
    total = part1 + part2 + part3 + part4
    st.success(f"Answer: {total}")
    return total

def multi_step_division(a, b):
    st.markdown("<div class='step'>Step 1: Estimate quotient</div>", unsafe_allow_html=True)
    quotient = a // b
    remainder = a % b
    st.write(f"{a} ÷ {b} ≈ {quotient} remainder {remainder}")
    
    st.markdown("<div class='step'>Step 2: Check by multiplication</div>", unsafe_allow_html=True)
    st.write(f"{quotient} * {b} + {remainder} = {quotient*b + remainder}")
    
    st.markdown("<div class='step'>Step 3: Final Answer</div>", unsafe_allow_html=True)
    st.success(f"Answer: {quotient} remainder {remainder}")
    return quotient, remainder

def solve_word_problem(problem_text):
    st.markdown("<div class='step'>Step 1: Analyze problem</div>", unsafe_allow_html=True)
    st.write(f"Problem: {problem_text}")
    
    numbers = list(map(int, re.findall(r'\d+', problem_text)))
    st.write(f"Numbers found: {numbers}")
    
    # Try to identify operation intelligently
    if "add" in problem_text or "sum" in problem_text:
        operation = "Addition"
        result = sum(numbers)
    elif "subtract" in problem_text or "left" in problem_text:
        operation = "Subtraction"
        result = numbers[0] - sum(numbers[1:])
    elif "multiply" in problem_text or "times" in problem_text:
        operation = "Multiplication"
        result = 1
        for n in numbers:
            result *= n
    elif "divide" in problem_text or "each" in problem_text:
        operation = "Division"
        result = numbers[0] // numbers[1] if len(numbers) > 1 else numbers[0]
    else:
        # Advanced AI: Try symbolic solution if complex
        x = symbols('x')
        try:
            expr = problem_text.lower().replace("?", "").replace("what is", "").replace("find", "")
            eq = Eq(x, sum(numbers))  # Simplified symbolic equation
            result = solve(eq)[0]
        except:
            result = sum(numbers)
        operation = "Smart Guess"

    st.write(f"Operation detected: {operation}")
    st.markdown("<div class='step'>Step 2: Compute answer</div>", unsafe_allow_html=True)
    st.success(f"Answer: {result}")
    return result

def generate_random_problem():
    ops = ["Addition", "Subtraction", "Multiplication", "Division"]
    op = random.choice(ops)
    a, b = random.randint(1, 50), random.randint(1, 50)
    st.write(f"Random {op} problem: {a} and {b}")
    return a, b, op

# ==========================
# MAIN INTERFACE
# ==========================
if problem_type != "Word Problem" and problem_type != "Random Problem":
    a = st.number_input("Enter first number:", step=1, min_value=0)
    b = st.number_input("Enter second number:", step=1, min_value=0)
    
    if st.button("Solve"):
        if problem_type == "Addition":
            multi_step_addition(a, b)
        elif problem_type == "Subtraction":
            multi_step_subtraction(a, b)
        elif problem_type == "Multiplication":
            multi_step_multiplication(a, b)
        elif problem_type == "Division":
            multi_step_division(a, b)

elif problem_type == "Word Problem":
    problem_text = st.text_area("Enter a word problem here:")
    if st.button("Solve Word Problem"):
        solve_word_problem(problem_text)

elif problem_type == "Random Problem":
    if st.button("Generate & Solve Random Problem"):
        a, b, op = generate_random_problem()
        if op == "Addition":
            multi_step_addition(a, b)
        elif op == "Subtraction":
            multi_step_subtraction(a, b)
        elif op == "Multiplication":
            multi_step_multiplication(a, b)
        elif op == "Division":
            multi_step_division(a, b)
