def evaluate_output(text):
    words = len(text.split())
    clarity = "Good" if words < 250 else "Too Long"

    return {
        "word_count": words,
        "clarity": clarity,
        "status": "Pass"
    }
