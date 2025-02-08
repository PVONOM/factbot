import requests
from transformers import pipeline
from typing import List
import os
from typing import Final


API_KEY: Final[str] = os.getenv('SEARCH_API_KEY')
CX: Final[str] = os.getenv('SEARCH_CX')

def scrape(query: str, num_results=5) -> str:
    
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}&num={num_results}"

    try:
        response = requests.get(url)
        results = response.json()
        if "items" in results and results["items"]:
            return results["items"][0]["snippet"]
        else:
            return "No relevant evidence found."
    except Exception as e:
        return f"Error retrieving results: {str(e)}"


classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


def fact_check(claim: str) -> str:
    evidence = scrape(claim)
    
    result = classifier(claim, [evidence], hypothesis_template="This implies that {}.")

    score = result["scores"][0]

    #return score
    
    if score <= 0.1:
        return f"Factbot has high confidence that this is true"
    elif score >= 0.2:
        return f"Factbot has high confidence that this is false"
    else:
        return f"Factbot is a little uncertain on this one. Further research reccommended. "
    

toxicity_labels = ["Profanity", "Hate Speech", "Offensive Language", "Positive", "Neutral"] # the categories the messages will go into 
# have them labeled as [0,1,2,3,4]

def profain_check(message: str) -> List[float]:
    result = classifier(message, toxicity_labels, hypothesis_template="This message contains {}.")
    # Get the label with the highest score
    label = result['labels'][0]
    score = result['scores'][0]

    score: float = [toxicity_labels.index(label),score] # label,score
    return score

# if profanity, it must start with inappropriate language detected:
'''
    # Interpret the result
    if score >= 0.8:
        return f"Flagged as: {label} (High confidence)"
    elif score >= 0.5:
        return f"Flagged as: {label} (Moderate confidence)"
    else:
        return "Message is clean (No toxicity detected)"
'''


#print(profain_check("pizza"))

#print(profain_check("fuck you! you ruined my day!"))

