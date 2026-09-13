import os
import ssl
import certifi
from dotenv import load_dotenv

load_dotenv()
os.environ["SSL_CERT_FILE"] = certifi.where()

from langchain_openai import ChatOpenAI
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_core.prompts import PromptTemplate

# 1. Connect to Neo4j
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    database="b45c816f"
)

# 2. Scheme-Specific Cypher Prompt Template
CYPHER_TEMPLATE = """Task: Generate a Cypher statement to query a Government Scheme knowledge graph.
Instructions:
1. Use only the provided relationship types and properties in the schema.
2. Use case-insensitive searches: toLower(node.id) CONTAINS toLower('term').
3. For questions asking what benefits exist, what schemes someone qualifies for, or how to apply:
   Traverse from Beneficiary or EligibilityCriteria through Scheme to Benefit.

Schema:
{schema}

Examples:
# What schemes are available for small farmers?
MATCH (s:Scheme)-[:ELIGIBLE_FOR]->(b:Beneficiary)
WHERE toLower(b.id) CONTAINS 'small' OR toLower(b.id) CONTAINS 'farmer'
OPTIONAL MATCH (s)-[:OFFERS_BENEFIT]->(ben:Benefit)
RETURN s.id AS scheme_name, ben.id AS benefit, b.id AS target_beneficiary

# What subsidies or benefits are provided under drip irrigation?
MATCH (s:Scheme)
WHERE toLower(s.id) CONTAINS 'irrigation' OR toLower(s.id) CONTAINS 'drip'
MATCH (s)-[:OFFERS_BENEFIT]->(ben:Benefit)
RETURN s.id AS scheme_name, ben.id AS benefit_details

Question: {question}
Cypher Query:"""

cypher_prompt = PromptTemplate(
    input_variables=["schema", "question"],
    template=CYPHER_TEMPLATE
)

llm = ChatOpenAI(model="gpt-4o", temperature=0)

chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    cypher_prompt=cypher_prompt,
    verbose=True,
    allow_dangerous_requests=True
)

print("="*60)
print("Tamil Nadu Government Scheme AI Assistant (Type 'exit' to quit)")
print("="*60)

while True:
    user_query = input("\nAsk about a scheme (e.g. 'What subsidy is available for seeds or irrigation?'): ")
    if user_query.strip().lower() in ["exit", "quit", "q"]:
        break
    try:
        response = chain.invoke({"query": user_query})
        print(f"\nResponse:\n{response['result']}\n")
    except Exception as e:
        print(f"Error executing query: {e}")