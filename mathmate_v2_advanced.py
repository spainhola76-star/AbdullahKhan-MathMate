def solve_word_problem_with_ai(problem_text):
    st.markdown("### 👩‍🏫 Step 1: Read the problem together")
    st.write(f"Problem: {problem_text}")

    # Extract numbers
    numbers = list(map(int, re.findall(r'\d+', problem_text)))
    st.write(f"📊 Numbers found: {numbers}")

    text = problem_text.lower()
    operation = None
    result = None
    explanation = ""

    # Detect operation
    if any(word in text for word in ["add", "sum", "together", "plus", "total"]):
        operation = "Addition"
        result = sum(numbers)
        explanation = f"We need the **total**, so we add {numbers[0]} and {numbers[1]}."

        # Teaching AI breakdown
        st.markdown("### 👨‍🏫 Step 2: Teach the steps")
        tens_a, ones_a = divmod(numbers[0], 10)
        tens_b, ones_b = divmod(numbers[1], 10)
        st.write(f"Break {numbers[0]} into {tens_a*10} + {ones_a}")
        st.write(f"Break {numbers[1]} into {tens_b*10} + {ones_b}")
        st.write(f"Now add tens: {tens_a*10} + {tens_b*10} = {tens_a*10 + tens_b*10}")
        st.write(f"Add ones: {ones_a} + {ones_b} = {ones_a + ones_b}")
        st.write(f"Finally, combine: {numbers[0]} + {numbers[1]} = {result}")

    elif any(word in text for word in ["subtract", "take away", "left", "difference", "minus"]):
        operation = "Subtraction"
        result = numbers[0] - numbers[1]
        explanation = f"We need to know what is **left**, so we subtract {numbers[1]} from {numbers[0]}."

        st.markdown("### 👨‍🏫 Step 2: Teach the steps")
        st.write(f"Start with {numbers[0]}")
        st.write(f"Take away {numbers[1]}")
        st.write(f"{numbers[0]} - {numbers[1]} = {result}")

    elif any(word in text for word in ["multiply", "times", "product", "each group has"]):
        operation = "Multiplication"
        result = numbers[0] * numbers[1]
        explanation = f"We are asked about **equal groups**, so we multiply {numbers[0]} × {numbers[1]}."

        st.markdown("### 👨‍🏫 Step 2: Teach the steps")
        for i in range(1, numbers[1] + 1):
            st.write(f"{numbers[0]} × {i} = {numbers[0] * i}")
        st.write(f"So, {numbers[0]} × {numbers[1]} = {result}")

    elif any(word in text for word in ["divide", "split", "share", "each", "quotient"]):
        operation = "Division"
        result = numbers[0] // numbers[1]
        remainder = numbers[0] % numbers[1]
        explanation = f"We are asked to **share equally**, so we divide {numbers[0]} ÷ {numbers[1]}."

        st.markdown("### 👨‍🏫 Step 2: Teach the steps")
        st.write(f"{numbers[1]} goes into {numbers[0]} → {result} times with a remainder of {remainder}")
        st.write(f"Because {numbers[0]} = {result} × {numbers[1]} + {remainder}")

    else:
        operation = "Smart Guess"
        if len(numbers) >= 2:
            result = numbers[0] + numbers[1]
            explanation = f"Not sure, but adding is the safest guess: {numbers[0]} + {numbers[1]} = {result}"
        else:
            result = numbers[0]
            explanation = f"Only one number found, so answer might be {result}"

    st.markdown("### ✅ Step 3: Final Answer")
    st.success(f"{explanation} → **Answer: {result}**")

    # 🎉 Student Helper Mode
    st.markdown("### 🎓 Student Helper Mode")
    st.info("🌟 Great work! You’re learning fast. Keep practicing and you’ll be a math master!")
    return result
