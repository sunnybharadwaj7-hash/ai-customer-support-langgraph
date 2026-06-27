# AI-Powered Customer Support Automation System

## Overview
This project is a LangGraph-based customer support system that classifies customer queries, routes them to the appropriate department, retrieves information using RAG, stores conversation history with SQLite, and supports human approval for critical requests.

## Features
- Intent Classification
- Conditional Routing
- Sales, Technical, Billing & Account Agents
- RAG-based Knowledge Retrieval
- SQLite Memory
- Human-in-the-Loop Approval
- Supervisor Validation

## Technologies
- Python 3.12
- LangGraph
- LangChain
- Ollama
- ChromaDB (or FAISS)
- SQLite

## Project Structure
```text
customer_support_system/
├── documents/
├── state.py
├── memory.py
├── rag.py
├── prompts.py
├── nodes.py
├── graph.py
├── main.py
├── requirements.txt
└── README.md
```

## Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Start Ollama:

```bash
ollama serve
ollama pull qwen2.5:3b
```

Run the project:

```bash
python main.py
```

## Sample Queries
- What are the pricing plans available?
- I forgot my account password.
- My application crashes while uploading a file.
- I need a refund.
- What was my previous support issue?

## Workflow
Customer Query → Intent Classification → Memory → RAG → Department Agent → Human Approval (if required) → Supervisor → Final Response → SQLite Memory

## Knowledge Base
- Company Policy
- Pricing Guide
- Technical Manual
- FAQ

## Author
AI-Powered Customer Support Automation System using LangGraph.
