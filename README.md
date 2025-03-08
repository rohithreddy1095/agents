# Agents Platform

A platform for creating and managing multiple financial data processing agents.

## Installation

```bash
# Clone the repository
git clone https://github.com/rohithreddy1095/agents.git
cd agents

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install finagent in development mode
pip install -e ./finagent
```

## Architecture

The Agents platform is designed with a modular architecture that allows for multiple specialized agents to be used independently or in combination:

```
agents/
├── finagent/            # Financial data agent
│   ├── finagent/        # Core package
│   │   ├── cli.py       # Command-line interface
│   │   ├── models/      # Data models
│   │   ├── providers/   # Data providers (News API, GNews API)
│   │   ├── processors/  # Data processors
│   │   └── utils/       # Utility functions
│   ├── tests/           # Unit tests
│   └── README.md        # FinAgent-specific documentation
└── [future_agent]/      # Placeholder for future agents
└── README.md            # This file
```

The platform follows these key architectural principles:

1. **Modularity**: Each agent is self-contained and can be used independently.
2. **Extensibility**: Plugins and providers can be easily added.
3. **Data Flow**: Clear separation between data fetching, processing, and storage.
4. **Command-line Interface**: Each agent provides a CLI for easy usage.

## Technical Report

The Agents platform is designed to consolidate various financial data processing tools under a single roof. Currently, it includes:

### FinAgent

FinAgent is specialized for collecting financial news and company data from various sources, including:

- News API (news-api.org)
- Google News API

Key features:
- Fetches financial news for specified companies.
- Stores data in structured JSON format.
- Provides summarization capabilities.
- Command-line interface for easy usage.

### Future Development

The platform is designed to accommodate additional agent types such as:
- Market data agents
- Sentiment analysis agents 
- Trading strategy agents

Each agent will maintain its independence while leveraging common infrastructure provided by the platform.