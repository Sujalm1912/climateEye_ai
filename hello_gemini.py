import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key or api_key == "paste-your-key-here":
    print("\n[!] Please replace 'paste-your-key-here' in your .env file with your actual Gemini API key from https://aistudio.google.com/")
    exit(1)

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Explain gravity to a 10-year-old in three lines.",
)

print(response.text)
