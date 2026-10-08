from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

import os

api = os.getenv('API_KEY_GROQ')

chat_model = ChatGroq(model='openai/gpt-oss-120b',api_key=api)