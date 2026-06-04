## Integrating Knowledge Graphs with Langchain and Neo4j

### Task Description

Develop a functional prototype that allows users to query a Neo4j graph database using natural language. This will involve an Large Language Model (LLM) from Ollama to translate natural language questions into Cypher queries, execute these queries against a Neo4j instance, and return the results.

---
To support you in solving the task, we provided some `docker` setup files. For the database and the LLM they should work out of the box, but minor adjustments may be necessary, based on your project structure.

The base project setup **should** look like this:

```
├── container-name/
│   ├── app/
│   │   ├── interface.py
│   │   ├── requirements.txt
│   │   └── Dockerfile/
│   ├── neo4j/
│   │   ├── init/
│   │   │   └── movies.cypher
│   │   ├── entrypoint.sh
│   │   └── Dockerfile
│   ├── ollama/
│   │   └── entrypoint.sh
│   ├── .env
│   ├── docker-compose.yaml
│   └── README.md
```
---
With the provided files, solve complete the following tasks:

1. **Neo4j Database Setup**: Set up a Neo4j graph database instance. As a database we use the "Movies" database. It is already present in the `neo4j/init` directory, but needs to be loaded into the database at startup. The `neo4j/entrypoint.sh` script *should* take care of that.
    
2. **Ollama LLM Setup**: Set up an Ollama instance, running a **suitable** open-source LLM capable of understanding and generating Cypher. Since you are probably working in a constrained environment regarding RAM etc. feel free to use a smaller model. 
   
   **It is not a problem if the generated queries don't always work!**
   - *By default we load the `LLama3.2` model. It is a medium-sized model. If you want to use a smaller (or larger) model, adjust the necessary files accordingly.*

3. **Application**: Write an application using primarly Python and Langchain that performs the following steps by finishing the functions in the `interface.py` file:
   1. Accepts a natural language query from the user (e.g., "Who directed 'The Matrix' movie?").
   2. Sends this natural language query to the LLM with appropriate prompting to instruct it to generate a Cypher query.
   3. Receives the generated Cypher query from the LLM.
   4. Executes the generated Cypher query against the Neo4j database.
   5. Processes the results from Neo4j into a human-readable format and returns it **OR** Directly returns the result of the query.

4. **Docker-Compose:** Finish the `docker-compose.yaml` by completing the `app` service.
5. **Run your application**

---

**Hint**: For interfacing between model and database you can use [https://python.langchain.com/api_reference/neo4j/chains/langchain_neo4j.chains.graph_qa.cypher.GraphCypherQAChain.html#langchain_neo4j.chains.graph_qa.cypher.GraphCypherQAChain](https://python.langchain.com/api_reference/community/chains/langchain_community.chains.graph_qa.cypher.GraphCypherQAChain.html).

---

