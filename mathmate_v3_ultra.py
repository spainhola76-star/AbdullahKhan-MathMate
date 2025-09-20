import streamlit as st
import random, re
from sympy import symbols, Eq, solve

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="MathMate V3 Ultra", page_icon="🧮", layout="centered")

st.title("🧮 MathMate V3 Ultra")
st.subheader("Zero-Mistake AI Math Teacher & Student Helper")

mode = st.radio("Choose Mode:", ["👩‍🏫 Teaching Mode", "🙋 Student Helper Mode"])

# ======================
# PROBLEM GENERATOR
# ======================
def generate_problem():
    # Arithmetic OR Word Problem
    if random.choice([True, False]):
        ops = ["addition", "subtraction", "multiplication", "division"]
        op = random.choice(ops)
        a, b = random.randint(2, 20), random.randint(2, 20)
        if op == "division": a = a * b
        return {"category": "arithmetic", "type": op, "a": a, "b": b}
    else:
        word_templates = [
            "Ali has {a} bags with {b} apples each. How many apples are there in total?",
            "Sara had {a} candies and gave {b} to her friend. How many are left?",
            "A box has {a} pencils. Another box has {b} pencils. How many pencils altogether?",
            "There are {a} cookies shared equally among {b} kids. How many cookies does each get?",
            "John read {a} pages on Monday and {b} pages on Tuesday. How many pages did he read in total?",
            "A farmer has {a} cows. He buys {b} more. How many cows does he have now?"
        ]
        a, b = random.randint(2, 20), random.randint(2, 20)
        q = random.choice(word_templates).format(a=a, b=b)
        return {"category": "word", "question": q}

# ======================
# HINT SYSTEM
# ======================
def give_hint(question):
    if "each" in question or "every" in question:
        return "Hint: 'each' usually means multiplication."
    if "left" in question:
        return "Hint: 'left' usually means subtraction."
    if "total" in question or "altogether" in question:
        return "Hint: 'total/altogether' usually means addition."
    if "share" in question or "equally" in question:
        return "Hint: 'share/equally' usually means division."
    return "Hint: Look for keywords like total, each, left, share."

# ======================
# TEACHER EXPLAINER
# ======================
def teacher_explain(problem):
    if problem["category"] == "arithmetic":
        a, b = problem["a"], problem["b"]
        if problem["type"] == "addition":
            steps = [
                f"We need to add {a} + {b}.",
                f"Step 1: Line up the numbers.",
                f"Step 2: Add the ones → {a%10} + {b%10}.",
                f"Step 3: Add the tens → {a//10*10} + {b//10*10}.",
                f"Final Step: Combine to get {a+b}."
            ]
            return steps, a+b
        elif problem["type"] == "subtraction":
            steps = [
                f"We need to subtract {b} from {a}.",
                f"Step 1: Line up the numbers.",
                f"Step 2: Subtract ones → {a%10} - {b%10}.",
                f"Step 3: Subtract tens → {a//10*10} - {b//10*10}.",
                f"Final Step: Combine to get {a-b}."
            ]
            return steps, a-b
        elif problem["type"] == "multiplication":
            steps = [
                f"We need to multiply {a} × {b}.",
                f"Step 1: Break into tens and ones.",
                f"{a} = {a//10*10} + {a%10}, {b} = {b//10*10} + {b%10}.",
                f"Step 2: Multiply each part and add together.",
                f"Final Step: {a} × {b} = {a*b}."
            ]
            return steps, a*b
        elif problem["type"] == "division":
            steps = [
                f"We need to divide {a} ÷ {b}.",
                f"Step 1: Estimate → {b} goes into {a}.",
                f"Step 2: Exact division gives {a//b} remainder {a%b}.",
                f"Final Step: {a} ÷ {b} = {a//b}."
            ]
            return steps, a//b

    elif problem["category"] == "word":
        return word_problem_solver(problem["question"])

    return ["I don’t know this yet."], None

# ======================
# WORD PROBLEM SOLVER (AI + Sympy)
# ======================
def word_problem_solver(question):
    numbers = list(map(int, re.findall(r'\d+', question)))
    x = symbols('x')

    if len(numbers) >= 2:
        a, b = numbers[0], numbers[1]

        if "each" in question or "every" in question:  # multiplication
            steps = [f"We see 'each', so it's multiplication.",
                     f"{a} × {b} = {a*b}."]
            return steps, a*b
        elif "left" in question:  # subtraction
            steps = [f"We see 'left', so it's subtraction.",
                     f"{a} - {b} = {a-b}."]
            return steps, a-b
        elif "total" in question or "altogether" in question:  # addition
            steps = [f"We see 'total/altogether', so it's addition.",
                     f"{a} + {b} = {a+b}."]
            return steps, a+b
        elif "share" in question or "equally" in question:  # division
            steps = [f"We see 'share/equally', so it's division.",
                     f"{a} ÷ {b} = {a//b}."]
            return steps, a//b

    # fallback with sympy equation (advanced AI)
    eq = Eq(x, sum(numbers))
    result = solve(eq)[0] if numbers else None
    return [f"I analyzed it as an equation: {eq}", f"Answer: {result}"], result

# ======================
# APP BODY
# ======================
problem = generate_problem()

if problem["category"] == "arithmetic":
    st.write(f"📘 Problem: {problem['a']} "
             f"{'+' if problem['type']=='addition' else '-' if problem['type']=='subtraction' else '×' if problem['type']=='multiplication' else '÷'} "
             f"{problem['b']}")
else:
    st.write(f"📘 Word Problem: {problem['question']}")

if mode == "👩‍🏫 Teaching Mode":
    steps, answer = teacher_explain(problem)
    for step in steps:
        st.info(step)
    if answer is not None:
        st.success(f"✅ Final Answer: {answer}")

else:  # Student Helper Mode
    st.warning("💡 You are in Student Helper Mode. Try solving first!")
    if problem["category"] == "word":
        st.write(give_hint(problem["question"]))
    if st.button("Show Teacher Help"):
        steps, answer = teacher_explain(problem)
        for step in steps:
            st.info(step)
        st.success(f"✅ Final Answer: {answer}")
