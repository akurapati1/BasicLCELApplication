# BasicLCELApplication

A minimal example of the **LangChain Expression Language (LCEL)**: a `prompt | model | parser` chain served as a REST API with **LangServe/FastAPI** and consumed by a **Streamlit** front-end. It translates text into a chosen language using a Groq-hosted LLM.

## Architecture
```
Streamlit (client.py) ──POST /chain/invoke──▶ LangServe (serve.py)
                                                 prompt | ChatGroq | StrOutputParser
```

## Files
| File | Purpose |
|---|---|
| `serve.py` | Builds the LCEL chain and exposes it at `/chain` (playground at `/chain/playground`) |
| `client.py` | Streamlit UI that calls the API |
| `simplellmLCEL.ipynb` | Notebook walkthrough of the same chain |
| `.env.example` | Required environment variables |

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env     # add your GROQ_API_KEY (https://console.groq.com)
```

## Run
```bash
python serve.py                 # terminal 1 - API on http://127.0.0.1:8000
streamlit run client.py         # terminal 2 - UI
```
Or call the API directly:
```bash
curl -s http://127.0.0.1:8000/chain/invoke -H 'Content-Type: application/json' \
  -d '{"input": {"language": "French", "text": "Hello"}}'
```

## Configuration
| Variable | Default | Description |
|---|---|---|
| `GROQ_API_KEY` | – | Required |
| `GROQ_MODEL` | `llama-3.1-8b-instant` | Any Groq chat model |
| `API_URL` | `http://127.0.0.1:8000/chain/invoke` | Used by the Streamlit client |

## What it demonstrates
LCEL composition with `|`, LangServe route generation, and a decoupled UI/API split.
