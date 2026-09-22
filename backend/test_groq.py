import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

from langchain_groq import ChatGroq

def test_groq():
    key = os.getenv("GROQ_API_KEY")
    print(f"Key loaded: {bool(key)} (Prefix: {key[:10] if key else 'None'}...)")
    llm = ChatGroq(groq_api_key=key, model_name="llama-3.3-70b-versatile", temperature=0.1)
    response = llm.invoke("Say 'Groq connection successful for Saturday Planner!'")
    print("Response:", response.content)

if __name__ == "__main__":
    test_groq()
