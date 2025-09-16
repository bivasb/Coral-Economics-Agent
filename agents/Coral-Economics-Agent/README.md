# Step-by-Step Guide: How to Write an Agent for Coral Protocol

This repository serves as both a working Economics Tutor Agent and a comprehensive guide for creating your own Coral Protocol agents. The Economics Agent demonstrates all the essential patterns and practices needed to build effective agents within the Coral ecosystem.

## Overview

The Coral Protocol enables multi-agent systems where specialized agents can communicate and collaborate. This guide walks you through creating your own agent by studying the Economics Agent implementation.

## 1. Project Structure Setup

### Required Files Structure:
```
your-agent-name/
├── main.py                 # Entry point and agent orchestration
├── {domain}_solver.py      # Core business logic for your domain
├── pyproject.toml         # Python dependencies and project metadata
├── requirements.txt       # Alternative dependency specification
├── Dockerfile            # Container configuration
├── run_agent.sh          # Local execution script
├── README.md             # Documentation and setup instructions
├── test.py               # Testing functionality
└── .env                  # Environment variables (create from .env_sample)
```

### File Purposes:
- **main.py**: Agent orchestration, Coral server communication, and LLM integration
- **{domain}_solver.py**: Domain-specific problem-solving logic
- **pyproject.toml**: Modern Python dependency management
- **Dockerfile**: Containerized deployment configuration
- **run_agent.sh**: Local development execution script

## 2. Core Dependencies

### Essential Python Packages:
```toml
[project]
name = "coral-{your-domain}-agent"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "langchain==0.3.25",           # LLM framework
    "langchain-community==0.3.24", # Community extensions
    "langchain-experimental==0.3.4", # Experimental features
    "langchain-mcp-adapters==0.1.7", # Coral Protocol MCP adapters
    "langchain-openai==0.3.26",    # OpenAI integration (or other LLM providers)
    "python-dotenv>=1.0.0",        # Environment variable management
    "uv>=0.7.17",                  # Fast Python package manager
]
```

### Key Dependencies Explained:
- **LangChain**: Framework for building LLM applications with tools and agents
- **MCP Adapters**: Enable communication with Coral Protocol servers
- **python-dotenv**: Manage environment variables and configuration
- **uv**: Fast, modern Python package manager for dependency resolution

## 3. Agent Architecture Pattern

### main.py Structure:
```python
import logging
import os, json, asyncio, traceback
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import Tool
from dotenv import load_dotenv
import urllib.parse

# Import your domain-specific solver
from {domain}_solver import {Domain}Solver

# Setup logging for debugging and monitoring
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def {domain}_solver_tool(problem: str):
    """
    Tool function that interfaces with your domain solver.
    This is how the LLM agent calls your custom logic.
    """
    solver = {Domain}Solver()
    solution = await solver.solve_problem(problem)
    return solution

def get_tools_description(tools):
    """Generate descriptions of available tools for the agent prompt"""
    return "\n".join(
        f"Tool: {tool.name}, Schema: {json.dumps(tool.args_schema)}"
        for tool in tools
    )

async def create_agent(coral_tools, agent_tools):
    """Create and configure the LangChain agent with tools and prompts"""
    # Combine Coral server tools with your custom tools
    combined_tools = coral_tools + agent_tools
    
    # Define system prompt with your agent's personality and capabilities
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""Your agent's system prompt here..."""),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    # Initialize LLM with configuration
    model = init_chat_model(
        model=os.getenv("MODEL_NAME", "gpt-4.1"),
        model_provider=os.getenv("MODEL_PROVIDER", "openai"),
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=float(os.getenv("MODEL_TEMPERATURE", "0.1")),
        max_tokens=int(os.getenv("MODEL_MAX_TOKENS", "8000"))
    )
    
    # Create agent executor
    agent = create_tool_calling_agent(model, combined_tools, prompt)
    return AgentExecutor(agent=agent, tools=combined_tools, verbose=True)

async def main():
    """Main execution loop for the agent"""
    # Environment setup
    load_dotenv()
    
    # Coral server connection
    base_url = os.getenv("CORAL_SSE_URL")
    agent_id = os.getenv("CORAL_AGENT_ID")
    
    # Configure connection parameters
    coral_params = {
        "agentId": agent_id,
        "agentDescription": "Your agent description here"
    }
    
    # Establish connection to Coral server
    client = MultiServerMCPClient({
        "coral": {
            "transport": "sse",
            "url": f"{base_url}?{urllib.parse.urlencode(coral_params)}",
            "timeout": int(os.getenv("TIMEOUT_MS", 300))
        }
    })
    
    # Get Coral tools and register your custom tools
    coral_tools = await client.get_tools(server_name="coral")
    agent_tools = [/* Your custom tools */]
    
    # Create and run agent
    agent_executor = await create_agent(coral_tools, agent_tools)
    
    # Execution loop
    while True:
        try:
            await agent_executor.ainvoke({"agent_scratchpad": []})
            await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Error in agent loop: {str(e)}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
```

## 4. Domain Solver Implementation

### Core Solver Class Pattern:
```python
import re
import math
from typing import Dict, List, Tuple, Optional

class {Domain}Solver:
    """
    Domain-specific solver for your agent's specialty.
    This is where your core business logic lives.
    """
    
    def __init__(self):
        """Initialize domain-specific knowledge, formulas, patterns"""
        self.domain_knowledge = {
            # Domain-specific data structures
            'formulas': {
                'formula_1': "Mathematical formula or rule",
                'formula_2': "Another important formula",
            },
            'concepts': {
                'concept_1': "Key concept explanation",
                'concept_2': "Another important concept",
            }
        }
    
    async def solve_problem(self, problem: str) -> str:
        """
        Main problem-solving entry point.
        This method should handle the full problem-solving workflow.
        """
        # Step 1: Identify the type of problem
        problem_type = self._identify_problem_type(problem)
        
        # Step 2: Route to specific solving methods based on problem type
        if problem_type == "type_a":
            return await self._solve_type_a(problem)
        elif problem_type == "type_b":
            return await self._solve_type_b(problem)
        elif problem_type == "type_c":
            return await self._solve_type_c(problem)
        # Add more problem types as needed
        else:
            return await self._general_explanation(problem)
    
    def _identify_problem_type(self, problem: str) -> str:
        """
        Classify the incoming problem based on keywords, patterns, or ML.
        This is crucial for routing to the right solving method.
        """
        problem_lower = problem.lower()
        
        # Keyword-based classification
        if any(word in problem_lower for word in ['keyword1', 'keyword2']):
            return "type_a"
        elif any(word in problem_lower for word in ['keyword3', 'keyword4']):
            return "type_b"
        elif any(word in problem_lower for word in ['keyword5', 'keyword6']):
            return "type_c"
        else:
            return "general"
    
    async def _solve_type_a(self, problem: str) -> str:
        """
        Solve specific problem type with step-by-step approach.
        Each solving method should return a well-formatted solution.
        """
        # Extract numerical values if present
        numbers = re.findall(r'-?\d+\.?\d*', problem)
        
        solution = f"""
**PROBLEM TYPE A ANALYSIS**

**Problem Identification:**
This is a Type A problem. [Explain what this type involves]

**Key Concepts:**
- Concept 1: [Explanation]
- Concept 2: [Explanation]

**Step-by-Step Solution:**

1. **Step 1: [Step Name]**
   - [Detailed explanation of this step]
   - [Any calculations or reasoning]

2. **Step 2: [Step Name]**
   - [Detailed explanation of this step]
   - [Any calculations or reasoning]

3. **Step 3: [Final Result]**
   - [Final answer or conclusion]
   - [Interpretation of results]

**Key Takeaways:**
- [Important learning point 1]
- [Important learning point 2]

**Real-World Application:**
[Connect the abstract concepts to real-world scenarios]
"""
        
        # Add numerical calculations if sufficient data is provided
        if len(numbers) >= 2:
            try:
                # Perform calculations with extracted numbers
                # Add calculated results to the solution
                pass
            except:
                # Handle calculation errors gracefully
                pass
        
        return solution
    
    async def _solve_type_b(self, problem: str) -> str:
        """Another problem type solver"""
        # Similar structure to _solve_type_a
        pass
    
    async def _general_explanation(self, problem: str) -> str:
        """
        Provide general guidance when the problem type is unclear.
        This serves as a fallback and educational resource.
        """
        solution = f"""
**GENERAL {DOMAIN.upper()} GUIDANCE**

I notice this might be a general {domain} question. Let me provide a comprehensive approach:

**Key {Domain} Principles:**

1. **Principle 1:**
   - [Fundamental concept explanation]
   - [Why it's important]

2. **Principle 2:**
   - [Another key concept]
   - [Practical applications]

**Problem-Solving Steps:**
1. **Identify** the specific area within {domain}
2. **Define** key terms and relationships
3. **Apply** relevant models, theories, or formulas
4. **Calculate** using appropriate methods
5. **Interpret** results in context
6. **Consider** real-world implications

**Common {Domain} Topics:**
- [Topic 1]: [Brief description]
- [Topic 2]: [Brief description]
- [Topic 3]: [Brief description]

**Study Tips:**
- [Helpful advice for learning this domain]
- [Practical approaches to problem-solving]

Please provide more specific details about your {domain} question, and I'll give you a detailed, step-by-step solution!
"""
        return solution
```

## 5. Agent Prompt Engineering

### System Prompt Template:
```python
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        f"""You are a specialized {domain} agent that helps with {domain}-related problems and questions.

        **Your Workflow:**
        1. Call wait_for_mentions from coral tools (timeoutMs: 30000) to receive mentions from other agents
        2. When you receive a mention, keep the thread ID and sender ID
        3. Analyze the content to identify if it contains a {domain} problem or question
        4. If it's a {domain} problem:
           - Use your {domain}_solver tool to solve the problem step by step
           - Provide clear explanations of concepts involved
           - Include formulas, diagrams, or visual aids when helpful (in text format)
           - Give real-world examples to illustrate concepts
        5. If it's a general {domain} question:
           - Explain the concepts clearly
           - Use examples appropriate for the target audience
           - Break down complex ideas into simple terms
        6. Structure your response with:
           - Clear problem identification
           - Step-by-step solution process
           - Final answer with units/context
           - Key takeaways or learning points
        7. Use send_message from coral tools to send your complete solution back to the sender
        8. If any error occurs, use send_message to send an error message with explanation
        9. Always respond back to the sender agent even if you cannot solve the problem
        10. Repeat the process from step 1

        **Your Capabilities:**
        - {List specific capabilities of your agent}
        - {Another capability}
        - {Another capability}

        **Available Tools:**
        Coral tools: {coral_tools_description}
        Your tools: {agent_tools_description}
        """
    ),
    ("placeholder", "{agent_scratchpad}")
])
```

### Prompt Engineering Best Practices:
- **Clear Workflow**: Define exact steps the agent should follow
- **Error Handling**: Specify how to handle various error conditions
- **Response Structure**: Template for consistent, helpful responses
- **Tool Usage**: Clear instructions on when and how to use each tool
- **Domain Expertise**: Emphasize the agent's specialized knowledge

## 6. Environment Configuration

### Required Environment Variables:
```bash
# Core Coral Protocol settings
CORAL_SSE_URL=http://localhost:5555/devmode/exampleApplication/privkey/session1/sse
CORAL_AGENT_ID={your_agent_id}

# LLM Configuration  
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4.1
MODEL_PROVIDER=openai
MODEL_TEMPERATURE=0.1
MODEL_MAX_TOKENS=8000
MODEL_BASE_URL=  # Optional: for custom LLM endpoints

# Optional runtime settings
CORAL_ORCHESTRATION_RUNTIME=  # Set by Coral when running in orchestrated mode
TIMEOUT_MS=300
```

### Environment Setup:
1. **Development**: Create `.env` file in your project root
2. **Production**: Set environment variables in your deployment system
3. **Docker**: Use ENV directives or pass via docker run -e
4. **Coral Orchestration**: Variables managed by Coral server configuration

## 7. Deployment Configuration

### Dockerfile Pattern:
```dockerfile
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager for fast dependency resolution
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Copy project files
COPY pyproject.toml ./
COPY requirements.txt ./
COPY main.py ./
COPY {domain}_solver.py ./

# Install dependencies using UV
RUN uv venv .venv && \
    . .venv/bin/activate && \
    uv pip install -r requirements.txt

# Set up virtual environment
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Run the agent
CMD ["python", "main.py"]
```

### run_agent.sh Script:
```bash
#!/bin/bash

# Navigate to the agent directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run the agent using UV
uv run python main.py
```

## 8. Testing Strategy

### test.py Pattern:
```python
import asyncio
from {domain}_solver import {Domain}Solver

async def test_agent_capabilities():
    """
    Test various problem types your agent should handle.
    This helps ensure your agent works correctly before deployment.
    """
    solver = {Domain}Solver()
    
    test_cases = [
        "Test case 1: [Description of test scenario]",
        "Test case 2: [Another test scenario]",
        "Test case 3: [Edge case or error condition]",
        "Test case 4: [Complex problem requiring multiple steps]",
        # Add domain-specific test problems
    ]
    
    print("🧪 Testing Agent Capabilities")
    print("=" * 50)
    
    for i, test in enumerate(test_cases):
        print(f"\n--- Test {i+1} ---")
        print(f"Input: {test}")
        print("\nProcessing...")
        
        try:
            result = await solver.solve_problem(test)
            print(f"Output: {result}")
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("-" * 30)

async def test_problem_type_identification():
    """Test the problem classification system"""
    solver = {Domain}Solver()
    
    test_problems = [
        ("Type A problem example", "type_a"),
        ("Type B problem example", "type_b"),
        ("Unclear problem", "general"),
    ]
    
    print("\n🎯 Testing Problem Type Identification")
    print("=" * 50)
    
    for problem, expected_type in test_problems:
        identified_type = solver._identify_problem_type(problem)
        status = "✅ PASS" if identified_type == expected_type else "❌ FAIL"
        print(f"{status} '{problem}' -> {identified_type} (expected: {expected_type})")

if __name__ == "__main__":
    asyncio.run(test_agent_capabilities())
    asyncio.run(test_problem_type_identification())
```

## 9. Integration with Coral Server

### Two Deployment Modes:

#### Executable Mode
Add to `coral-server/src/main/resources/application.yaml`:
```yaml
registry:
  {your-agent-name}:
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
        description: "What model provider to use (e.g 'openai')"
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
      command: ["bash", "-c", "{absolute_path_to_agent}/run_agent.sh main.py"]
      environment:
        - option: "OPENAI_API_KEY"
        - option: "MODEL_NAME"
        - option: "MODEL_PROVIDER"
        - option: "MODEL_MAX_TOKENS"
        - option: "MODEL_TEMPERATURE"
```

#### Dev Mode
1. Ensure Coral Server is running: `./gradlew bootRun`
2. Run your agent separately: `uv run python main.py`
3. Use Coral Studio UI to monitor agents

## 10. Best Practices

### Code Quality:
- **Error Handling**: Implement comprehensive try-catch blocks
- **Logging**: Use structured logging for debugging and monitoring
- **Async Patterns**: Follow async/await consistently throughout
- **Modularity**: Create small, testable, single-purpose functions
- **Type Hints**: Use Python type hints for better code clarity

### Agent Behavior:
- **Always Respond**: Never leave a sender without a response
- **Clear Structure**: Use consistent formatting for all responses
- **Educational Value**: Include explanations and learning opportunities
- **Error Recovery**: Handle edge cases and provide helpful error messages
- **Performance**: Optimize for response time while maintaining quality

### Documentation:
- **README**: Comprehensive setup and usage instructions
- **Code Comments**: Explain complex logic and domain-specific concepts
- **API Docs**: Document your tools and their expected inputs/outputs
- **Examples**: Provide clear usage examples and test cases
- **Troubleshooting**: Common issues and their solutions

### Security:
- **Environment Variables**: Never commit secrets to version control
- **Input Validation**: Sanitize and validate all inputs
- **Error Messages**: Don't expose sensitive information in error messages
- **Dependencies**: Keep dependencies updated and scan for vulnerabilities

## 11. Customization Guide

### For Your Domain:
1. **Replace Economics Logic**: Substitute `economics_solver.py` with your domain solver
2. **Update Keywords**: Modify problem type identification keywords
3. **Adapt Formulas**: Replace economic formulas with domain-specific ones
4. **Customize Prompts**: Tailor system prompts to your domain expertise
5. **Modify Tests**: Create test cases relevant to your problem space

### Domain-Specific Considerations:
- **Mathematics**: Focus on formula application and step-by-step calculations
- **Science**: Emphasize experimental design and hypothesis testing
- **Language**: Prioritize grammar rules and linguistic analysis
- **History**: Stress chronological analysis and cause-effect relationships
- **Programming**: Focus on code analysis, debugging, and best practices

## 12. Troubleshooting

### Common Issues:
1. **Connection Errors**: Check CORAL_SSE_URL and network connectivity
2. **Tool Not Found**: Verify tool registration in agent_tools list
3. **LLM API Errors**: Validate API keys and rate limits
4. **Import Errors**: Ensure all dependencies are installed via `uv sync`
5. **Permission Errors**: Check file permissions on scripts and directories

### Debugging Tips:
- Enable verbose logging: `logging.basicConfig(level=logging.DEBUG)`
- Test solver independently: `python test.py`
- Check environment variables: `env | grep CORAL`
- Validate JSON schemas: Use online JSON validators for tool schemas
- Monitor Coral Studio: Use the UI to track agent communications

## 13. Economics Agent Example

This repository implements a complete Economics Tutor Agent that demonstrates all the patterns described above. Key features:

### Capabilities:
- Supply and demand analysis
- Market equilibrium calculations  
- Elasticity problems (price, income, cross-price)
- Consumer and producer surplus
- GDP and macroeconomic indicators
- Inflation and unemployment calculations
- Market structure analysis

### Example Usage:
```
Input: "Calculate the price elasticity of demand when price increases from $5 to $7 and quantity demanded decreases from 120 to 80 units."

Output:
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
Since demand is inelastic, the price increase will lead to higher total revenue.

**Real-World Application:**
This suggests the product may be a necessity or have few substitutes, similar to gasoline or basic food items.
```

## Getting Started

1. **Clone this repository** as a template for your own agent
2. **Customize the domain solver** with your specific logic
3. **Update environment variables** with your API keys and configuration
4. **Test your agent** using the provided test framework
5. **Deploy** using either executable mode or dev mode
6. **Monitor** agent performance using Coral Studio UI

This guide provides everything you need to create sophisticated, domain-specific agents that integrate seamlessly with the Coral Protocol ecosystem. The Economics Agent serves as a complete reference implementation demonstrating production-ready patterns and practices.