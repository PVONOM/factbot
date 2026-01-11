import requests
from transformers import pipeline
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from typing import List
import os
from typing import Final
from dotenv import load_dotenv


load_dotenv()

API_KEY: Final[str] = os.getenv('API_KEY')
CX: Final[str] = os.getenv('CX')
NEWSAPI_KEY: Final[str] = os.getenv('NEWSAPI_KEY')


NLI_MODEL = "ynie/roberta-large-snli_mnli_fever_anli_R1_R2_R3-nli"
nli_tokenizer = AutoTokenizer.from_pretrained(NLI_MODEL)
nli_model = AutoModelForSequenceClassification.from_pretrained(NLI_MODEL)

label_map = {0: "CONTRADICTION", 1: "NEUTRAL", 2: "ENTAILMENT"}

def fever_fact_check(claim: str, evidences: list) -> str:
    verdicts = []
    for ev in evidences:
        text = f"{claim} </s> {ev}"
        inputs = nli_tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
        with torch.no_grad():
            logits = nli_model(**inputs).logits
        pred = torch.argmax(logits, dim=1).item()
        verdicts.append(label_map[pred])

    ent = verdicts.count("ENTAILMENT")
    con = verdicts.count("CONTRADICTION")

    if ent > con:
        return "TRUE"
    elif con > ent:
        return "FALSE"
    else:
        return "UNCERTAIN"




def newsapi_scrape(claim: str, max_results: int = 20) -> List[str]:
    """
    Query NewsAPI and return a list of relevant article snippets
    """
    if not NEWSAPI_KEY:
        return []

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": claim,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": max_results,
        "apiKey": NEWSAPI_KEY
    }

    try:
        resp = requests.get(url, params=params)
        data = resp.json()
        articles = data.get("articles", [])
        return [a["description"] or a["title"] for a in articles if a.get("description") or a.get("title")]
    except Exception as e:
        print(f"NewsAPI error: {e}")
        return []


def scrape(query: str, num_results=10) -> str:
    
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

def combine_verdicts(avg_score: float, fever_label: str) -> str:
    
    #Combines zero-shot numerical confidence & FEVER categorical verdict.
    #avg_score ~ confidence claim is false
    # map FEVER to numeric

    fever_map = {"TRUE": 0.0, "FALSE": 1.0, "UNCERTAIN": 0.5}
    fever_score = fever_map[fever_label]

    # weights — adjustable
    w_zero_shot = 0.3
    w_fever = 0.7

    combined = (w_zero_shot * avg_score) + (w_fever * fever_score)

    if combined <= 0.10:
        return f"Factbot has high confidence that this is true"
    elif combined >= 0.40:
        return f"Factbot has high confidence that this is false"
    else:
        return f"Factbot is a little uncertain on this one. Further research reccommended. "


classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


def fact_check(claim: str) -> str:
    google_evidence = scrape(claim)
    news_evidence = newsapi_scrape(claim)

    evidence_list = [google_evidence] + news_evidence
    evidence_list = [e for e in evidence_list if e]

    if not evidence_list:
        return "Factbot is having a tough time finding evidence. Further research recommended."
    
    scores = []
    for evidence in evidence_list:
        result = classifier(claim, [evidence], hypothesis_template="This implies that {}.")
        scores.append(result["scores"][0])

    avg_score = sum(scores) / len(scores)

    fever_label = fever_fact_check(claim, evidence_list)

    return combine_verdicts(avg_score, fever_label)


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

