import os
import ssl
import json
import certifi
from dotenv import load_dotenv

# SSL certificate bypass for macOS Python
load_dotenv()
os.environ["SSL_CERT_FILE"] = certifi.where()

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_neo4j import Neo4jGraph

# 1. Load Scraped Schemes
with open("schemes.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

documents = [
    Document(
        page_content=f"Scheme Name: {item['title']}\nDetails: {item['details']}",
        metadata={"source": "TN_Gov_Portal"}
    )
    for item in raw_data[:25] # Batch first 25 schemes for clean mapping
]

# 2. Extract Entities and Relations with LLM
llm = ChatOpenAI(temperature=0, model="gpt-4o")

transformer = LLMGraphTransformer(
    llm=llm,
    allowed_nodes=["Scheme", "Beneficiary", "Benefit", "EligibilityCriteria", "Department"],
    allowed_relationships=["ELIGIBLE_FOR", "OFFERS_BENEFIT", "REQUIRES", "MANAGED_BY"]
)

print("Extracting Graph Entities and Triples...")
graph_documents = transformer.convert_to_graph_documents(documents)

# 3. Save directly to Neo4j
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

print("Connecting to Neo4j AuraDB...")
graph = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    database="b45c816f"
)

graph.add_graph_documents(
    graph_documents,
    baseEntityLabel=True,
    include_source=True
)

graph.refresh_schema()
print("\n--- Ingestion Complete! Current Schema ---")
print(graph.schema)