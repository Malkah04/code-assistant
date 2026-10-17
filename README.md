# AI Coding Assistant 🤖💻

An AI-powered coding assistant built as part of my training, designed to help users generate code, understand existing code, and ask follow-up questions while maintaining conversation context.

## 📌 Project Overview

The goal of this project is to build more than a basic chatbot that simply returns code. It combines request classification, Retrieval-Augmented Generation (RAG), relevance evaluation, and conversation memory to create a structured workflow for programming assistance.

The assistant supports two main types of requests:
- **Code Generation:** Generates code based on the user's request and relevant retrieved examples.
- **Code Explanation:** Helps users understand existing code.

## ⚙️ How It Works

The assistant follows a multi-step pipeline:

1. **Request Classification**  
   Classifies the user's request as either code generation or code explanation and routes it to the corresponding workflow.

2. **Knowledge Retrieval (RAG)**  
   Uses ChromaDB to retrieve relevant programming examples from a vector database built using the HumanEval dataset.

3. **Relevance Evaluation**  
   Evaluates whether the retrieved context is useful for answering the user's request before passing it to the generation stage.

4. **Response Generation**  
   Uses an LLM to generate code or explain code based on the request and available context.

5. **Conversation Memory**  
   Stores conversation history in SQLite, allowing the assistant to use previous interactions when handling follow-up questions.

## 🧰 Tech Stack

- **Python** — Core implementation
- **Streamlit** — User interface
- **LangChain** — LLM orchestration and prompt pipelines
- **Ollama** — Local LLM integration
- **OpenRouter** — LLM integration
- **ChromaDB** — Vector database for semantic retrieval
- **HumanEval** — Programming examples dataset
- **SQLite** — Conversation history storage

## 🗂️ Main Components

- Request classification
- Code generation and explanation workflows
- Vector-based document retrieval
- Retrieved-context relevance evaluation
- LLM prompt pipelines
- Persistent conversation history

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Malkah04/code-assistant.git
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

If the project includes a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Configure the LLMs

Install Ollama and pull the local model used by the project. Configure any required OpenRouter credentials according to your implementation.

**Important:** Keep API keys in environment variables or a `.env` file, and never commit secrets to GitHub.

### 5. Run the application

```bash
streamlit run streamlit_app.py
```

## 🧠 Key Learning Areas

Working on this project involves exploring:

- Building multi-step LLM workflows
- Using RAG for programming-related tasks
- Understanding the difference between semantic similarity and actual relevance
- Designing prompts and evaluating model responses
- Managing conversation history with SQLite
- Debugging interactions between different pipeline components

## 🔮 Future Improvements

- Add automated execution and testing of generated code.
- Improve retrieval quality and relevance evaluation.
- Expand the programming knowledge base.
- Evaluate code-generation quality using structured test cases.
- Improve conversation memory and context handling.

## 👩‍💻 Author

**Malak Sobhy**

[GitHub](https://github.com/Malkah04) · [LinkedIn](https://www.linkedin.com/in/malksobhy/)
