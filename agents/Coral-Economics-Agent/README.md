## [Economics Tutor Agent](https://github.com/Coral-Protocol/Coral-Economics-Agent)

The Economics Tutor Agent is a specialized high school economics problem-solving agent that helps students understand and solve economics problems including supply and demand analysis, market equilibrium, elasticity calculations, GDP analysis, and other microeconomics and macroeconomics concepts.

![Economics Agent](https://github.com/Coral-Protocol/awesome-agents-for-multi-agent-systems/blob/main/images/Coral-Economics-Agent.png)

## Responsibility

The Economics Tutor Agent acts as a comprehensive economics tutor for high school students. It can solve step-by-step economics problems, explain economic concepts clearly, provide real-world examples, and help students understand complex economic relationships through structured analysis.

## Details
- **Framework**: LangChain
- **Tools used**: Custom Economics Solver, Coral Server Tools
- **AI model**: OpenAI GPT-4.1
- **Date added**: September 16, 2025
- **License**: MIT

## Capabilities

The agent can help with the following economics topics:

### Microeconomics
- Supply and demand analysis
- Market equilibrium calculations
- Price elasticity of demand and supply
- Consumer and producer surplus
- Market structures (perfect competition, monopoly, monopolistic competition, oligopoly)
- Cost analysis and profit maximization

### Macroeconomics
- GDP calculations (nominal and real)
- Economic growth analysis
- Inflation rate calculations
- Unemployment rate analysis
- Business cycle concepts
- Monetary and fiscal policy effects

### Problem-Solving Features
- Step-by-step solution breakdown
- Clear explanations of economic concepts
- Real-world examples and applications
- Graphical representations (in text format)
- Formula explanations and calculations
- Key takeaways and learning points

## Setup the Agent

### 1. Clone & Install Dependencies

<details>  

```bash
# In a new terminal navigate to the agents directory:
cd /path/to/Coral-Protocol/agents

# The agent is already created in the Coral-Economics-Agent directory
cd Coral-Economics-Agent

# Download and run the UV installer, setting the installation directory to the current one
curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=$(pwd) sh

# Create a virtual environment named `.venv` using UV
uv venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install uv
pip install uv

# Install dependencies from `pyproject.toml` using `uv`:
uv sync
```

</details>

### 2. Configure Environment Variables

Get the API Key:
[OpenAI](https://platform.openai.com/api-keys)

<details>

```bash
# Create .env file in project root
cp .env_sample .env

# Edit the .env file and add your API keys:
# OPENAI_API_KEY=your_openai_api_key_here
# CORAL_SSE_URL=http://localhost:5555/sse
# CORAL_AGENT_ID=economics_agent
```
</details>

## Run the Agent

You can run in either of the below modes to get your system running.  

- The Executable Mode is part of the Coral Protocol Orchestrator which works with [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio).  
- The Dev Mode allows the Coral Server and all agents to be separately running on each terminal without UI support.  

### 1. Executable Mode

Checkout: [How to Build a Multi-Agent System with Awesome Open Source Agents using Coral Protocol](https://github.com/Coral-Protocol/existing-agent-sessions-tutorial-private-temp) and update the file: `coral-server/src/main/resources/application.yaml` with the details below, then run the [Coral Server](https://github.com/Coral-Protocol/coral-server) and [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio). You do not need to set up the `.env` in the project directory for running in this mode; it will be captured through the variables below.

<details>

For Linux or MAC:

```bash
registry:
  # ... your other agents
  economics-agent:
    options:
      - name: "OPENAI_API_KEY"
        type: "string"
        description: "OpenAI API key"
      - name: "MODEL_NAME"
        type: "string"
        description: "What model to use (e.g 'gpt-4.1')"
        default: "gpt-4.1"
      - name: "MODEL_PROVIDER"
        type: "string"
        description: "What model provider to use (e.g 'openai', etc)"
        default: "openai"
      - name: "MODEL_MAX_TOKENS"
        type: "string"
        description: "Max tokens to use"
        default: "8000"
      - name: "MODEL_TEMPERATURE"
        type: "string"
        description: "What model temperature to use"
        default: "0.1"

    runtime:
      type: "executable"
      command: ["bash", "-c", "<replace with path to this agent>/run_agent.sh main.py"]
      environment:
        - option: "OPENAI_API_KEY"
        - option: "MODEL_NAME"
        - option: "MODEL_PROVIDER"
        - option: "MODEL_MAX_TOKENS"
        - option: "MODEL_TEMPERATURE"
```

For Windows, create a powershell command (run_agent.ps1) and run:

```bash
command: ["powershell","-ExecutionPolicy", "Bypass", "-File", "${PROJECT_DIR}/run_agent.ps1","main.py"]
```

</details>

### 2. Dev Mode

Ensure that the [Coral Server](https://github.com/Coral-Protocol/coral-server) is running on your system and run below command in a separate terminal.

<details>

```bash
# Run the agent using `uv`:
uv run python main.py
```

You can view the agents running in Dev Mode using the [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio) by running it separately in a new terminal.

</details>

## Testing the Agent

Test the economics solver functionality independently:

<details>

```bash
# Run the test script to see the agent solve various economics problems:
python test.py
```

This will demonstrate the agent's capabilities with different types of economics problems including elasticity calculations, market equilibrium, surplus analysis, and more.

</details>

## Example Usage

<details>

```bash
# Input:
Calculate the price elasticity of demand when price increases from $5 to $7 and quantity demanded decreases from 120 to 80 units.

# Output:
**ELASTICITY ANALYSIS**

**Problem Identification:**
This is an elasticity problem. Elasticity measures responsiveness of one variable to changes in another.

**Step-by-Step Solution:**

1. **Calculate Percentage Changes:**
   - % Change in Quantity = ((80 - 120) / 120) × 100 = -33.33%
   - % Change in Price = ((7 - 5) / 5) × 100 = 40%

2. **Calculate Elasticity:**
   - Price Elasticity of Demand (PED) = |-33.33% / 40%| = 0.83

3. **Interpret Results:**
   - |PED| = 0.83 < 1: Inelastic demand
   - Quantity demanded is not very responsive to price changes

**Revenue Implications:**
- Since demand is inelastic, the price increase will lead to higher total revenue

**Real-World Application:**
This suggests the product may be a necessity or have few substitutes, similar to gasoline or basic food items.
```

</details>

## Features

### Comprehensive Problem Solving
- **Automatic Problem Type Detection**: Identifies whether the problem involves supply/demand, elasticity, market equilibrium, etc.
- **Step-by-Step Solutions**: Breaks down complex problems into manageable steps
- **Formula Applications**: Shows relevant economic formulas and how to apply them
- **Numerical Calculations**: Performs calculations when sufficient data is provided

### Educational Features
- **Concept Explanations**: Clear explanations of economic principles
- **Real-World Examples**: Connects abstract concepts to real-world scenarios
- **Graph Descriptions**: Text-based representations of economic graphs
- **Key Takeaways**: Summarizes important learning points

### Supported Problem Types
- Supply and demand curve analysis
- Market equilibrium calculations
- Elasticity problems (price, income, cross-price)
- Consumer and producer surplus
- Market structure analysis
- GDP and macroeconomic indicators
- Inflation and unemployment calculations

## Creator Details
- **Name**: Claude Code Assistant
- **Affiliation**: Coral Protocol
- **Contact**: [Discord](https://discord.com/invite/Xjm892dtt3)