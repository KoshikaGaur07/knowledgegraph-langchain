# 🧠 Knowledge Graph QA — LangChain + Neo4j + Ollama

> Natural language querying over a Neo4j graph database using a local LLM via Ollama and LangChain's `GraphCypherQAChain`.

Built as part of my MSc in International Software System Sciences at Otto-Friedrich University of Bamberg.

---

## 💡 What This Project Does

This application lets users ask questions in plain English and get answers from a Neo4j graph database — no Cypher knowledge required.

**Example:**
```
User: "Who directed The Matrix?"
App:  Translates → Cypher query → Executes on Neo4j → Returns answer
```

The pipeline works as follows:
1. User types a natural language question
2. A local LLM (LLaMA 3.2 via Ollama) translates it into a Cypher query
3. The query runs against a Neo4j Movies database
4. Results are returned in a human-readable format

---

## 🏗️ Architecture

```
User Input (natural language)
        │
        ▼
  LangChain GraphCypherQAChain
        │
   ┌────┴────┐
   │         │
Ollama     Neo4j
(LLaMA 3.2) (Movies DB)
   │         │
   └────┬────┘
        │
        ▼
   Answer returned to user
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| LLM Framework | LangChain + `GraphCypherQAChain` |
| Local LLM | Ollama (LLaMA 3.2:1b) |
| Graph Database | Neo4j (Movies dataset) |
| Interface | Dash (Python web app) |
| Containerisation | Docker + Docker Compose |

---

## 📁 Project Structure

```
├── app/
│   ├── interface.py        # Main Dash app + LangChain logic
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile
├── neo4j/
│   ├── init/
│   │   └── movies.cypher   # Movies graph dataset
│   ├── entrypoint.sh       # Auto-loads DB on startup
│   └── Dockerfile
├── ollama/
│   └── entrypoint.sh       # Pulls and runs LLaMA model
├── .env                    # Environment variables (not committed)
├── docker-compose.yaml
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- At least **8GB RAM** available for Docker (LLaMA model is memory-intensive)

### 1. Clone the repository
```bash
git clone https://github.com/KoshikaGaur07/knowledgegraph-langchain.git
cd knowledgegraph-langchain
```

### 2. Set up your environment variables
Create a `.env` file in the root directory:
```
NEO4J_URI=bolt://neo4j:7687
NEO4J_USERNAME=neo4j
NEO4J_PWD=your_password_here
OLLAMA_BASE_URL=http://ollama:7869
```

### 3. Run the application
```bash
docker-compose up --build
```
> First run takes ~3–5 minutes — Ollama needs to pull the LLaMA model (~1.3GB)

### 4. Open the app
```
http://localhost:8050
```

---

## 💬 Example Queries You Can Try

```
"Who directed The Matrix?"
"Which movies did Tom Hanks act in?"
"Who are the top 5 most connected actors?"
"What movies were released after 2000?"
```

---

## ⚙️ Configuration

**Switching to a different LLM model** — edit `ollama/entrypoint.sh`:
```bash
ollama pull llama3.2:1b      # smaller, faster
ollama pull llama3.2         # default (better quality)
ollama pull mistral          # alternative
```

**Note:** Smaller models are faster but may occasionally generate incorrect Cypher syntax. This is expected behaviour with local LLMs.

---

## 🧩 Key Implementation — LangChain GraphCypherQAChain

The core logic in `interface.py` uses LangChain's graph QA chain to bridge natural language and Cypher:

```python
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_ollama import OllamaLLM

graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PWD)
llm = OllamaLLM(model="llama3.2:1b", base_url=OLLAMA_BASE_URL)
chain = GraphCypherQAChain.from_llm(llm, graph=graph, verbose=True)

response = chain.invoke({"query": user_question})
```

---

## 📚 Built With / References

- [LangChain Neo4j Integration](https://python.langchain.com/docs/integrations/graphs/neo4j_cypher/)
- [GraphCypherQAChain Docs](https://python.langchain.com/api_reference/neo4j/chains/langchain_neo4j.chains.graph_qa.cypher.GraphCypherQAChain.html)
- [Ollama](https://ollama.com/) — run LLMs locally
- [Neo4j Movies Dataset](https://neo4j.com/developer/example-data/)

---

## 👩‍💻 Author

**Koshika Gaur**
MSc International Software System Sciences — Otto-Friedrich University of Bamberg
[GitHub](https://github.com/KoshikaGaur07) · [LinkedIn](https://linkedin.com/in/koshika-gaur) · [Email](mailto:gaurkoshika@gmail.com)

