from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq

groq = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Gemini model
gemini_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

response1 = groq.invoke("Summarize what AI is in two sentences.")
print("Groq:", response1.content)


from utils.audio_processor import process_input
from core.transcriber import transcribe_all

source ="#any url or file name"

chunks = process_input(source)

print(transcribe_all(chunks))