# Cover Letter RAG Agent

A RAG (Retrieval-Augmented Generation) based agent for creating tailored cover letters.

## Installation

### Prerequisites
- Python 3.8 or later
- pip (Python package manager)

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/coverletter-rag-agent.git
cd coverletter-rag-agent
```

2. Create and activate a virtual environment using uv (recommended):
```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment with Python 3.11
uv python install 3.11
uv venv --python=3.11
uv sync
```

## Environment Configuration

Create a `.env.local` file in the root directory with the following variables:

```
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
```

## Running the Application
## Running the Application

### Using FastAPI with uv

Run the FastAPI application with:

```bash
uv run fastapi dev
```

This will start the server with hot-reloading enabled for development.

You can access the API documentation at `http://127.0.0.1:8000/docs` after starting the server.
