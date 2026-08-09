from dotenv import load_dotenv
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-lite-latest",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0,
)

client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

def get_client():
    return client

def ask_gemini(prompt):
    response = client.models.generate_content(model="gemini-flash-lite-latest", contents = prompt)
    return response.text

embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
def get_embedding(text):
    return embeddings_model.embed_query(text)