import logging
import os, json, asyncio, traceback
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import Tool
from dotenv import load_dotenv
import urllib.parse
from economics_solver import EconomicsSolver

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def economics_solver_tool(problem: str):
    """
    Solves high school economics problems using structured analysis.
    
    Args:
        problem (str): The economics problem to solve
        
    Returns:
        str: Detailed solution with explanation
    """
    solver = EconomicsSolver()
    solution = await solver.solve_problem(problem)
    return solution

def get_tools_description(tools):
    return "\n".join(
        f"Tool: {tool.name}, Schema: {json.dumps(tool.args_schema).replace('{', '{{').replace('}', '}}')}"
        for tool in tools
    )

async def create_agent(coral_tools, agent_tools):
    coral_tools_description = get_tools_description(coral_tools)
    agent_tools_description = get_tools_description(agent_tools)
    combined_tools = coral_tools + agent_tools

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            f"""You are a specialized high school economics tutor agent that helps students understand and solve economics problems. You interact with tools from Coral Server and have your own economics solving capabilities.

            Follow these steps in order:

            1. Call wait_for_mentions from coral tools (timeoutMs: 30000) to receive mentions from other agents.
            2. When you receive a mention, keep the thread ID and the sender ID.
            3. Analyze the content to identify if it contains an economics problem or question.
            4. If it's an economics problem:
               - Use your economics_solver tool to solve the problem step by step
               - Provide clear explanations of economic concepts involved
               - Include graphs, formulas, or diagrams when helpful (in text format)
               - Give real-world examples to illustrate concepts
            5. If it's a general economics question:
               - Explain the economic concepts clearly
               - Use examples appropriate for high school level
               - Break down complex ideas into simple terms
            6. Structure your response with:
               - Clear problem identification
               - Step-by-step solution process
               - Final answer with units/context
               - Key takeaways or learning points
            7. Use send_message from coral tools to send your complete solution back to the sender.
            8. If any error occurs, use send_message to send an error message with a brief explanation.
            9. Always respond back to the sender agent even if you cannot solve the problem.
            10. Repeat the process from step 1.

            Economics topics you can help with include:
            - Supply and demand analysis
            - Market equilibrium
            - Elasticity calculations
            - Consumer and producer surplus
            - Market structures (perfect competition, monopoly, etc.)
            - GDP and economic indicators
            - Inflation and unemployment
            - International trade
            - Government policies and their effects
            - Basic microeconomics and macroeconomics concepts

            These are the list of coral tools: {coral_tools_description}
            These are the list of your tools: {agent_tools_description}."""
        ),
        ("placeholder", "{agent_scratchpad}")
    ])

    model = init_chat_model(
        model=os.getenv("MODEL_NAME", "gpt-4.1"),
        model_provider=os.getenv("MODEL_PROVIDER", "openai"),
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=float(os.getenv("MODEL_TEMPERATURE", "0.1")),
        max_tokens=int(os.getenv("MODEL_MAX_TOKENS", "8000")),
        base_url=os.getenv("MODEL_BASE_URL") if os.getenv("MODEL_BASE_URL") else None
    )

    agent = create_tool_calling_agent(model, combined_tools, prompt)
    return AgentExecutor(agent=agent, tools=combined_tools, verbose=True, handle_parsing_errors=True)

async def main():
    runtime = os.getenv("CORAL_ORCHESTRATION_RUNTIME", None)
    if runtime is None:
        load_dotenv()

    base_url = os.getenv("CORAL_SSE_URL")
    agentID = os.getenv("CORAL_AGENT_ID")

    coral_params = {
        "agentId": agentID,
        "agentDescription": "A specialized high school economics tutor agent that helps students understand and solve economics problems including supply and demand, market equilibrium, elasticity, GDP analysis, and other microeconomics and macroeconomics concepts."
    }

    query_string = urllib.parse.urlencode(coral_params)

    CORAL_SERVER_URL = f"{base_url}?{query_string}"
    logger.info(f"Connecting to Coral Server: {CORAL_SERVER_URL}")
    
    timeout = int(os.getenv("TIMEOUT_MS", 300))

    client = MultiServerMCPClient(
        connections={
            "coral": {
                "transport": "sse",
                "url": CORAL_SERVER_URL,
                "timeout": timeout,
                "sse_read_timeout": timeout,
            }
        }
    )
    logger.info("Coral Server Connection Established")

    coral_tools = await client.get_tools(server_name="coral")
    logger.info(f"Coral tools count: {len(coral_tools)}")

    agent_tools = [
        Tool(
            name="economics_solver",
            func=None,
            coroutine=economics_solver_tool,
            description="Solves high school economics problems with step-by-step explanations. Can handle supply/demand analysis, market equilibrium, elasticity calculations, GDP analysis, and other micro/macroeconomic concepts.",
            args_schema={
                "properties": {
                    "problem": {
                        "type": "string",
                        "description": "The economics problem or question to solve"
                    }
                },
                "required": ["problem"],
                "type": "object"
            }
        )
    ]
    
    agent_executor = await create_agent(coral_tools, agent_tools)

    while True:
        try:
            logger.info("Starting new agent invocation")
            await agent_executor.ainvoke({"agent_scratchpad": []})
            logger.info("Completed agent invocation, restarting loop")
            await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Error in agent loop: {str(e)}")
            logger.error(traceback.format_exc())
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())