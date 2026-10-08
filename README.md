# LangGraph Chat

A simple chat app built with **LangGraph**, **FastAPI**, and a plain HTML frontend.
You type a question in the browser, the FastAPI server sends it through a LangGraph workflow, and the model's reply is shown in the chat window.

---

## How it works

```
Browser (index.html)
   │  POST /chat  {"questions": "..."}
   ▼
FastAPI (main.py)
   │  workflow.invoke({"messages": [HumanMessage(...)]})
   ▼
LangGraph:  START → chat_model node → END
   │
   ▼
{"messages": [...]}  → the last message is the AI reply
```

- `ChatState` holds a list of `messages` (merged with `add_messages`).
- The graph has one node, `chat_model`, which calls `chat_model.invoke(...)` from `model.py`.
- `index.html` reads the last message from the response and shows it.

## Project structure

```
project/
├── main.py          # LangGraph workflow + FastAPI app
├── model.py         # defines chat_model (your LLM)
├── index.html       # chat frontend (dark theme)
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10+
- An API key for the LLM provider used in `model.py`

`requirements.txt` (add the package for your LLM provider too, for example `langchain-openai` or `langchain-google-genai`):

```
fastapi
uvicorn
langgraph
langchain-core
```

## Setup

```bash
# 1. (optional) create a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux / macOS

# 2. install packages
pip install -r requirements.txt
```

### `model.py`

This file must expose a variable named `chat_model`. Example shape:

```python
# model.py
from langchain_openai import ChatOpenAI   # or any other provider

chat_model = ChatOpenAI(model="your-model-name")
```

Set your API key as an environment variable before running (the variable name depends on your provider).

### Serve the frontend from FastAPI

Add this to `main.py` right after `app = FastAPI(...)`:

```python
from fastapi.responses import FileResponse

@app.get("/")
def home():
    return FileResponse("index.html")
```

## Run

From inside the project folder:

```bash
uvicorn main:app --reload
```

Then open:

- Chat page: http://127.0.0.1:8000
- API docs (test the endpoint): http://127.0.0.1:8000/docs

> If your Python file is not named `main.py`, use its name instead, for example `uvicorn app:app --reload`.

## API

### `POST /chat`

Request body:

```json
{ "questions": "What is LangGraph?" }
```

Response (shortened):

```json
{
  "messages": [
    { "type": "human", "content": "What is LangGraph?" },
    { "type": "ai", "content": "LangGraph is ..." }
  ]
}
```

On an error the server returns status `400` with `{"detail": "..."}`.

## Opening `index.html` separately

If you open `index.html` directly or host it somewhere else:

1. Change `API_URL` at the top of the `<script>` in `index.html` to the full address, for example `http://127.0.0.1:8000/chat`.
2. Enable CORS in `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Limitations

- Each request is independent. The server does not remember earlier messages, so the model has no conversation history.
- To add memory, compile the graph with a checkpointer (for example `MemorySaver`) and send a `thread_id` with each request.

## Troubleshooting

| Problem | What to check |
|---|---|
| "Could not get a reply" in the chat | Look at the uvicorn terminal for the real error. Usually a missing API key or a mistake in `model.py`. |
| Page shows "Not Found" | Run uvicorn from the folder that contains `index.html`, and make sure the `/` route is added. |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` and install your LLM provider's package. |
| Browser blocks the request | You opened `index.html` from another origin. Follow the CORS steps above. |