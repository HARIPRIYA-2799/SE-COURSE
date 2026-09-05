from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

# 1. Setup the chain components
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an elite high-altitude trek leader. Provide concise, direct, "
        "and safety-critical advice tailored to the user's fitness profile."
    ),
    (
        "user",
        "I am planning to do the {trek_name} trek. My fitness level is {fitness_level}. "
        "Provide: \n"
        "1. A realistic difficulty rating for my level\n"
        "3. Recommended preparation time"
    )
])

parser = StrOutputParser()
trek_chain = prompt_template | model | parser

# 2. Interactive CLI loop
print("🏔️  Welcome to the AI Trek Advisor! (type 'exit' to quit)\n")

while True:
    trek_name = input("\nEnter Trek Name (e.g., Roopkund, Annapurna Base Camp): ").strip()
    if trek_name.lower() == "exit":
        break

    fitness_level = input("Enter your fitness level (Beginner / Intermediate / Advanced): ").strip()
    if fitness_level.lower() == "exit":
        break

    print(f"\nAnalyzing plan for {trek_name}...\n")

    # 3. Use .stream() instead of .invoke() for real-time word-by-word output
    for chunk in trek_chain.stream({
        "trek_name": trek_name,
        "fitness_level": fitness_level
    }):
        print(chunk, end="", flush=True)

    print("\n" + "-" * 50)