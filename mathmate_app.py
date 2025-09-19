# mathmate_app.py
# MathMate - Primary School AI Math Tutor (friendly, green & white)
# Paste this into GitHub as mathmate_app.py
# Requires: streamlit, sympy

import re
import streamlit as st
import sympy as sp
from sympy import pretty

# ---------- Page setup & style ----------
st.set_page_config(page_title="MathMate", page_icon="🧮", layout="centered")
st.markdown(
    """
    <style>
      body { background-color: #f3fff3; }
      .appview-container .main .block-container{ padding: 1.5rem 2rem; }
      h1 { color: #0b8a2f; }
      .stButton>button { background-color: white; color: #0b8a2f; border: 2px solid #0b8a2f; border-radius:10px; padding:8px 14px; font-weight:700; }
      .stTextInput>div>input { border: 2px solid #0b8a2f; border-radius:8px; padding:8px; font-size:16px; }
      .stAlert { border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True
)

# ---------- Header ----------
st.title("🧮 MathMate")
st.markdown("<h4 style='color:#0b8a2f;'>Your friendly math tutor — for primary school ✨</h4>", unsafe_allow_html=True)
st.write("Type a math question using `+ - * / ^` and parentheses `()` — e.g. `3 + 4*2`, `(5+3)^2`, `7/2`.")

# ---------- Helper functions for safe step-by-step calculation ----------
ALLOWED = re.compile(r'^[0-9\s+\-*/().\^xX×÷]+$')  # allowed characters (we'll convert x/÷/^)
def clean_input(s: str) -> str:
    s = s.replace("×", "*").replace("x", "*").replace("X", "*").replace("÷", "/")
    s = s.replace("^", "**")
    s = s.replace(",", ".")  # allow comma decimals if typed
    return s

def is_safe(s: str) -> bool:
    return bool(ALLOWED.match(s))

def tokenize(expr: str):
    tokens = []
    i = 0
    L = len(expr)
    while i < L:
        c = expr[i]
        if c.isspace():
            i += 1
            continue
        # number (int or decimal)
        if c.isdigit() or c == '.':
            j = i
            while j < L and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            tokens.append(expr[i:j])
            i = j
            continue
        # exponent operator **
        if c == '*' and i+1 < L and expr[i+1] == '*':
            tokens.append('**'); i += 2; continue
        # single-char operators / parentheses
        if c in '+-*/()':
            tokens.append(c); i += 1; continue
        # anything else (shouldn't happen after cleaning)
        raise ValueError(f"Invalid character: {c}")
    # handle unary minus (like -3 or -(...))
    j = 0
    while j < len(tokens):
        if tokens[j] == '-' and (j == 0 or tokens[j-1] in ('(', '+', '-', '*', '/', '**')):
            # if next is number -> make negative number
            if j+1 < len(tokens) and re.match(r'^\d+(\.\d+)?$', tokens[j+1]):
                tokens[j+1] = '-' + tokens[j+1]
                tokens.pop(j)
                continue
            # if next is '(' -> convert "- (" to "-1 * ("
            if j+1 < len(tokens) and tokens[j+1] == '(':
                tokens[j] = '-1'
                tokens.insert(j+1, '*')
                j += 2
                continue
        j += 1
    return tokens

def compute_with_sympy(left: str, op: str, right: str):
    # Use SymPy to compute exactly (rationals) when possible
    expr_str = f"({left}){op}({right})"
    val = sp.simplify(sp.sympify(expr_str))
    return val

def evaluate_no_paren(tokens):
    steps = []
    # operator precedence groups
    groups = [['**'], ['*', '/'], ['+', '-']]
    # work left-to-right within each group
    for ops in groups:
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if t in ops:
                left = tokens[i-1]
                op = tokens[i]
                right = tokens[i+1]
                result = compute_with_sympy(left, op, right)
                # text for kid-friendly explanation
                op_word = {'+':'add', '-':'subtract', '*':'multiply', '/':'divide', '**':'power'}[op]
                steps.append(f"Compute {left} {op} {right} → {sp.pretty(result)}  ({op_word})")
                # replace three tokens with the single result
                tokens = tokens[:i-1] + [str(result)] + tokens[i+2:]
                i = max(i-1, 0)
            else:
                i += 1
    return tokens, steps

def evaluate_tokens(tokens):
    steps = []
    # first, handle parentheses (innermost first)
    while '(' in tokens:
        # find innermost '(' index (last '(')
        start = max(i for i,t in enumerate(tokens) if t == '(')
        # find closing ')'
        end = start + 1
        while end < len(tokens) and tokens[end] != ')':
            end += 1
        if end >= len(tokens) or tokens[end] != ')':
            raise ValueError("Mismatched parentheses")
        inner = tokens[start+1:end]
        if not inner:
            raise ValueError("Empty parentheses")
        inner_tokens, inner_steps = evaluate_no_paren(inner)
        # record the inner steps first (if any)
        steps.extend(inner_steps)
        # final inner result
        inner_result = inner_tokens[0]
        steps.append(f"Simplify ({' '.join(inner)}) → {sp.pretty(sp.sympify(inner_result))}")
        # replace the parentheses with the result
        tokens = tokens[:start] + [str(inner_result)] + tokens[end+1:]
    # now no parentheses remain; evaluate remaining expression
    tokens, final_steps = evaluate_no_paren(tokens)
    steps.extend(final_steps)
    return tokens[0], steps

# ---------- UI: input + examples ----------
# Use session state so example buttons fill the input
if 'q' not in st.session_state:
    st.session_state.q = ""

col1, col2, col3 = st.columns([1,2,1])
with col1:
    if st.button("Try 3+4*2"):
        st.session_state.q = "3+4*2"
with col2:
    st.text_input("Try an example or type your own:", key='q', label_visibility="collapsed")
with col3:
    if st.button("(5+3)^2"):
        st.session_state.q = "(5+3)^2"

st.write("Hints: You can use `^` for powers, e.g. `2^3`. Use `x` or `*` for multiply, `÷` or `/` for divide.")

# Solve action
if st.button("Solve"):
    raw = st.session_state.q.strip()
    if raw == "":
        st.warning("Please enter a math question (e.g. 2+2 or (3+4)*2).")
    else:
        cleaned = clean_input(raw)
        if not is_safe(cleaned):
            st.error("Please use only numbers and standard math symbols (+ - * / ^ ( )).")
        else:
            try:
                tokens = tokenize(cleaned)
                # show original expression nicely
                st.markdown("### ✅ First look — your expression:")
                try:
                    parsed = sp.sympify(cleaned.replace('**','^'))  # for prettier display w ^ (best-effort)
                    st.latex(sp.pretty(parsed, use_unicode=True))
                except Exception:
                    st.write(" ".join(tokens))
                # compute step-by-step
                result_str, steps = evaluate_tokens(tokens)
                st.markdown("### ✨ Step-by-step solution (easy language):")
                for i, step in enumerate(steps, start=1):
                    st.write(f"**Step {i}.** {step}")
                # show final answer nicely
                final_val = sp.sympify(result_str)
                st.markdown("### 🎉 Final Answer:")
                st.latex(sp.pretty(final_val, use_unicode=True))
                st.success("Great! Keep practicing — you're doing awesome ✨")
            except Exception as e:
                st.error("Sorry, I couldn't solve that. Try a simpler expression like `2+2`, `5*3`, or `(3+4)*2`.")
                st.info(f"Debug: {e}")

# ---------- Footer ----------
st.markdown("---")
st.markdown("Made with ❤️ by MathMate — fun, simple and safe for primary school learners.")
