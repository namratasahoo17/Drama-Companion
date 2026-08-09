from llm import ask_gemini
import json

def extract_review(review_text):
    prompt = f"""Extract the following into JSON.
            Review : {review_text} Return only valid JSON.Return data that matches this schema. {{
  "title": "",
  "overall_rating": 0,
  "aspects": [
    {{
      "name": "",
      "score": 0,
      "reason": ""
    }}
  ]
}}"""
    response = ask_gemini(prompt)
    response = response.replace("```json", "").replace("```", "").strip()
    data = json.loads(response)
    return(data)

def extract_preferences(review_text,category_text):
    prompt = f"""Extract the following into JSON.
            Review : {review_text} Return a JSON array (a list), like this:
{{"category": " ", "value": " ", "sentiment": 1}}, {{"category": " ", "value": " ", "sentiment": 1}}
One object per preference found. Only use categories from this list: {category_text}"""
    response = ask_gemini(prompt)
    response = response.replace("```json", "").replace("```", "").strip()
    data = json.loads(response)
    return(data)