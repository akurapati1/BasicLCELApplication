"""LangServe API exposing a simple translation chain (prompt | Groq LLM | parser)."""
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langserve import add_routes

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise SystemExit("GROQ_API_KEY is not set. Copy .env.example to .env and add your key.")

model = ChatGroq(model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"), groq_api_key=groq_api_key)

# 1. Prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([("system", system_template), ("user", "{text}")])

# 2. LCEL chain
parser = StrOutputParser()
chain = prompt_template | model | parser

# 3. App definition
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain runnable interfaces",
)
add_routes(app, chain, path="/chain")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
