
!pip -q install -U langgraph langchain langchain-google-genai requests

import os
import ast
import operator
import requests
from google.colab import userdata
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_agent

# Set Google API key
os.environ["GOOGLE_API_KEY"] = userdata.get("GOOGLE_API_KEY")

# Tool 1: Get current weather
@tool
def get_weather(city: str) -> str:
    """Get the current temperature in Celsius for a city."""
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1},
        timeout=15
    ).json()

    if not geo.get("results"):
        return f"City not found: {city}"

    place = geo["results"][0]

    data = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": "temperature_2m"
        },
        timeout=15
    ).json()

    temp = data["current"]["temperature_2m"]
    return f"Current temperature in {city}: {temp} Celsius"

# Tool 2: Safe calculator
@tool
def calculate(expression: str) -> str:
    """Calculate expressions using numbers and +, -, *, /."""
    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp):
            ops = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv
            }
            op = ops.get(type(node.op))
            if op:
                return op(evaluate(node.left), evaluate(node.right))

        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -evaluate(node.operand)

        raise ValueError("Unsupported expression")

    try:
        return str(evaluate(ast.parse(expression, mode="eval").body))
    except Exception as e:
        return f"Calculation error: {e}"

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.7-flash",
    temperature=0
)

# Create LangGraph agent
agent = create_agent(
    model=llm,
    tools=[get_weather, calculate],
    system_prompt=(
        "Use the weather and calculator tools to answer the question. "
        "Get the temperature in Celsius, convert it to Fahrenheit, "
        "calculate 15% of 320, and add that value to the Fahrenheit "
        "temperature. Base your answer on tool results."
    )
)

# Hardcoded query
query = """
What is the current temperature in London in Fahrenheit?
Calculate 15% of 320 and add it to the temperature in Fahrenheit.
Use the tools to perform the calculations.
"""

# Run agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": query}]},
    config={"recursion_limit": 10}
)

# Print execution trace
print("=== AGENT EXECUTION TRACE ===")

for msg in result["messages"]:
    if getattr(msg, "tool_calls", None):
        for call in msg.tool_calls:
            print("\nAction:", call["name"])
            print("Action Input:", call["args"])

    elif msg.type == "tool":
        content = msg.content
        if isinstance(content, str):
            print("Observation:", content)
        else:
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    print("Observation:", block["text"])

# Print only the final answer text
print("\n=== FINAL ANSWER ===")

content = result["messages"][-1].content

if isinstance(content, str):
    print(content)
elif isinstance(content, list):
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            print(block["text"])
