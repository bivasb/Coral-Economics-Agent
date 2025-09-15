# Coral Protocol - Multi-Agent Communication System

A complete multi-agent system built on the Coral Protocol that enables AI agents to communicate, collaborate, and coordinate through a thread-based messaging system.

## System Architecture

- **Server**: Kotlin/Gradle-based MCP server that orchestrates agent communication
- **Studio**: SvelteKit web interface for managing sessions and monitoring agents  
- **Agents**: Python-based AI agents with specialized capabilities

## Prerequisites

- **Docker** (for server)
- **Node.js 18+** and **yarn** (for studio)
- **Python 3.10+** and **uv** (for agents)
- **OpenAI API Key** (required for all agents)
- **Additional API Keys** as needed per agent:
  - Linkup API Key (for OpenDeepResearch Agent)
  - GitHub Personal Access Token (for RepoUnderstanding Agent)

## Quick Start

### 1. Start the Coral Server (Docker)

```bash
# Navigate to server directory
cd server

# Build the Docker image
docker build -t coral-server .

# Run the Docker container
docker run -p 5555:5555 -v $(pwd)/src/main/resources:/config coral-server
```

The server will be available at `http://localhost:5555`

### 2. Start the Coral Studio (yarn)

```bash
# Navigate to studio directory  
cd studio

# Install dependencies
yarn install

# Start development server
yarn dev
```

The studio will be available at `http://localhost:5173`

### 3. Set Up and Run Agents

Each agent requires its own setup and configuration:

#### Coral Interface Agent
```bash
cd agents/Coral-Interface-Agent

# Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=$(pwd) sh

# Create virtual environment
uv venv .venv
source .venv/bin/activate

# Install dependencies
pip install uv
uv sync

# Configure environment
cp .env_sample .env
# Edit .env with your OpenAI API key

# Run the agent
uv run python main.py
```

#### Coral OpenDeepResearch Agent
```bash
cd agents/Coral-OpenDeepResearch-Agent

# Setup (same UV process as above)
curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=$(pwd) sh
uv venv .venv
source .venv/bin/activate
pip install uv
uv sync

# Configure environment
cp .env_sample .env
# Edit .env with OpenAI and Linkup API keys

# Run the agent
uv run python main.py
```

#### Coral RepoUnderstanding Agent
```bash
cd agents/Coral-RepoUnderstanding-Agent

# Setup (same UV process as above)
curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=$(pwd) sh
uv venv .venv
source .venv/bin/activate
pip install uv
uv sync

# Configure environment
cp .env.example .env
# Edit .env with OpenAI API key and GitHub Personal Access Token

# Run the agent
uv run python main.py
```

## Agent Capabilities

### Interface Agent
- Main user interaction interface
- Coordinates multi-agent tasks
- Terminal-based conversation logging
- Human-in-the-loop functionality

### OpenDeepResearch Agent  
- Automated research and report generation
- Multi-agent workflow coordination
- Web search integration (Tavily, Linkup, DuckDuckGo)
- Structured report output

### RepoUnderstanding Agent
- GitHub repository analysis
- Automatic code structure understanding
- README and documentation parsing
- Architecture overview generation

## Alternative Running Modes

### Production Mode (using yarn build)
```bash
# In studio directory
yarn build
yarn preview
# Available at http://localhost:4173
```

### Server Alternative Modes
```bash
# Run with Gradle (without Docker)
cd server
./gradlew run

# Run with custom arguments
./gradlew run --args="--stdio"
./gradlew run --args="--sse-server 5555"
```

## MCP Inspector (Optional)
Connect to the server using MCP Inspector for debugging:
```bash
npx @modelcontextprotocol/inspector sse --url http://localhost:5555/devmode/exampleApplication/privkey/session1/sse
```

## Environment Variables

Each agent requires specific environment variables in their `.env` files:

**All Agents:**
- `OPENAI_API_KEY` - Your OpenAI API key
- `MODEL_NAME` - Model to use (default: gpt-4.1)
- `MODEL_PROVIDER` - Provider (default: openai)

**OpenDeepResearch Agent:**
- `LINKUP_API_KEY` - Linkup API key for web search

**RepoUnderstanding Agent:**
- `GITHUB_ACCESS_TOKEN` - GitHub Personal Access Token

## Usage Flow

1. Start the Coral Server (Docker)
2. Start the Coral Studio (yarn dev)
3. Configure and run desired agents
4. Access the Studio UI to create sessions and manage agent interactions
5. Agents will automatically register with the server and be available for coordination

## Troubleshooting

- Ensure all ports (5555 for server, 5173 for studio) are available
- Verify API keys are correctly set in agent `.env` files
- Check that the Coral Server is running before starting agents
- For Windows users, consider using Git Bash or WSL

## Documentation

- [Server Documentation](server/README.md)
- [Studio Documentation](studio/README.md)
- [Interface Agent](agents/Coral-Interface-Agent/README.md)
- [OpenDeepResearch Agent](agents/Coral-OpenDeepResearch-Agent/README.md)
- [RepoUnderstanding Agent](agents/Coral-RepoUnderstanding-Agent/README.md)