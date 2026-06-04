import os
import sys
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_core.prompts import PromptTemplate
import gradio as gr

# --- Neo4j & Ollama Connection (from  .env file) --- #
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")         # GET NEO4J URI 
NEO4J_USERNAME =os.getenv("NEO4J_USERNAME","neo4j")   # GET NEO4J USERNAME  # GET NEO4J USERNAME
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD","neo4jpassword")    # GET NEO4J PASSWORD
OLLAMA_BASE_URL = os.getenv("OLAMA_BASE_URL","http://ollama:11434")   # GET OLLAMA BASE URL
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL","llama3.2:1b")
print(f"Using llama3.2 from Ollama at {OLLAMA_BASE_URL}")

if NEO4J_PASSWORD is None:
    print("Error: NEO4J_PASSWORD environment variable not set.")
    exit()


print(f"Attempting to use Ollama model '{OLLAMA_MODEL}' from {OLLAMA_BASE_URL}")
print(f"Connecting to Neo4j at {NEO4J_URI} with user {NEO4J_USERNAME}")

# --- Initialize Neo4jGraph --- #
#graph = ...
try:
    graph = Neo4jGraph(
        url=NEO4J_URI,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD
    ) 
    
    print(f"Neo4j Graph Schema: {graph.schema}")
except Exception as exception:
    print(f"Failed to connect to Neo4j or initialize graph: {exception}")
    exit()

# --- Initialize LLM --- #
#llm = ...
try:
    llm = ChatOllama(
        base_url=OLLAMA_BASE_URL,
        model=OLLAMA_MODEL,
        temperature=0.2,  
        timeout=200.0   
    )
    # Test LLM 
    llm.invoke("Hi")
    print(f"Successfully initialized Ollama LLM with model: {OLLAMA_MODEL}")
except Exception as e:
    print(f"Failed to initialize Ollama LLM: {e}")
    exit()

# --- Define Cypher Generation Prompt --- #
#CYPHER_GENERATION_TEMPLATE = ... 
CYPHER_GENERATION_TEMPLATE = """Task: Generate Cypher query to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}

Note: 
- Only return the Cypher query. No other text, explanations, or apologies.
- If you cannot construct a query from the schema to answer the question, return "ERROR: Cannot answer question from schema."

Question: {question}
Cypher Query:"""

cypher_generation_prompt = PromptTemplate(
    template=CYPHER_GENERATION_TEMPLATE,
    input_variables=["schema", "question"]
)

# --- Initialize Chain --- #
#chain = ...
#This chain will:
# 1. Introspect the graph schema.
# 2. Use the LLM to convert the user's question into a Cypher query (using its default prompt or your cypher_generation_prompt).
# 3. Execute the Cypher query against the Neo4j graph.
# 4. If return_direct=False (default), it passes the query results back to the LLM to synthesize a natural language answer.
# 5. If return_direct=True, it returns the raw JSON result from the database.
try:
    chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=True,  # Set to True to see the generated Cypher queries and intermediate steps.
        # Add this parameter to acknowledge the risk:
        allow_dangerous_requests=True,
        cypher_prompt=cypher_generation_prompt, 
        # Uncomment to use your custom Cypher generation prompt.
        return_direct=False # For a chatbot, False usually provides a more natural response.
    )
    print("GraphCypherQAChain initialized successfully.")
except Exception as e:
    print(f"Failed to initialize GraphCypherQAChain: {e}")
    exit()

# --- Gradio Interface Function ---
def chat_interface(user_question):
    """
    This function is called by Gradio when the user submits a question.
    It invokes the Langchain QA chain and returns the answer.
    """
    if not user_question:
        return "Please type a question."
    try:
        # The chain expects a dictionary with the key 'query' (or as defined by its input_keys)
        response = chain.invoke({"query": user_question})
        # The result from GraphCypherQAChain is a dictionary, typically with a 'result' key for the answer.
        return response.get("result", "Sorry, I couldn't find an answer for that.")
    except Exception as e:
        print(f"Error during chain invocation: {e}") # Log the error for debugging
        return "An error occurred while processing your question. Please check the logs."

# --- Gradio App Setup --- # 
# NOTHING TO DO HERE
if __name__ == "__main__":
    print("Launching Gradio interface...")
    iface = gr.Interface(
        fn=chat_interface,
        inputs=gr.Textbox(lines=2, placeholder="Ask a question about the graph...", label="Your Question"),
        outputs=gr.Textbox(label="AI Response"),
        title="Neo4j & Ollama Graph QA Chatbot",
        description="Ask questions about the graph data loaded using the llama3.2 model.",
        flagging_mode="never"
    )

    iface.launch(server_name="0.0.0.0", server_port=8050)