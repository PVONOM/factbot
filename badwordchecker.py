'''
def check_toxicity(message: str) -> str:
    result = classifier(message, toxicity_keywords, hypothesis_template="This message contains {}.")

    label = result['labels'][0]
    score = result['scores'][0]

    if score >= 0.8:
        return f"Flagged as: {label} (High confidence)"
    elif score >= 0.5:
        return f"Flagged as: {label} (Moderate confidence)"
    else:
        return "Message is clean (No toxicity detected)"
    



# Example messages for toxicity check
claim2 = "i hate you and hope that you die"
print(check_toxicity(claim2))

claim3 = "i love waffles and donuts"
print(check_toxicity(claim3))
'''
