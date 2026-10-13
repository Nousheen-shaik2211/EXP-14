# EXP-14
# LangGraph ReAct Agent: Weather and Calculator

## Aim
To build a basic LLM agent using LangGraph's `create_react_agent`, equipped with weather and calculator tools to handle a multi-step query.

## Problem Statement
Create an agent that retrieves the current temperature in London, converts Celsius to Fahrenheit, calculates 15% of 320, and adds the percentage result to the Fahrenheit temperature.

## Technologies Used
- Python
- LangGraph
- LangChain OpenAI
- OpenAI GPT-4o-mini
- Open-Meteo Weather API

## Tools
1. `get_weather(city)` — retrieves the current temperature in Celsius.
2. `calculate(expression)` — safely evaluates basic arithmetic expressions.

## Algorithm
1. Install the required dependencies.
2. Configure the OpenAI API key.
3. Define the weather and calculator tools.
4. Initialize the LLM with temperature set to zero.
5. Create the ReAct agent using `create_react_agent`.
6. Invoke the agent with the hardcoded multi-step query.
7. Display tool calls and observations.
8. Print the final combined answer.

## Project Structure
```text
LangGraph_ReAct_Agent/
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Installation

```bash
pip install -r requirements.txt
```

## Configure the API Key

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

Linux/macOS:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Replace the placeholder with your valid OpenAI API key. Never commit API keys to GitHub.

## Run the Experiment

```bash
python main.py
```

## Expected Output
The execution trace displays:
- Weather tool invocation and temperature observation
- Calculator tool invocations and calculation results
- Final answer combining the Fahrenheit temperature with 15% of 320

The actual output depends on current weather conditions in London.

## Conclusion
This experiment demonstrates a tool-using ReAct agent that combines live weather retrieval with mathematical calculations to answer a multi-step question.

## Notes
- An internet connection is required for weather retrieval.
- OpenAI API access is required for the LLM.
- The program prints tool calls and observations rather than private internal reasoning.
