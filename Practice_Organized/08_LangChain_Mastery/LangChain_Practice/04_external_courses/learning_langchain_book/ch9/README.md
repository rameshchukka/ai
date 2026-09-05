# Chapter 9: Deployment - RAG AI Agent Example

This directory contains the code for deploying a Retrieval-Augmented Generation (RAG) AI chatbot agent, as discussed in Chapter 9 of "Learning LangChain." This agent is designed to ingest documents and then answer questions based on the content of those documents.

## Overview

This example demonstrates how to deploy a LangGraph application that consists of two main components:

1.  **Ingestion Graph:** Responsible for loading, embedding and indexing documents.
2.  **Retrieval Graph:** Responsible for answering questions based on the indexed documents.

Both Python and JavaScript implementations are provided.

**Note:** If you'd like to see a full ai app (frontend and backend) that incorporates the concepts discussed in this chapter, check it out [here](https://github.com/mayooear/ai-pdf-chatbot-langchain/tree/main).

## Prerequisites

Before running the code, ensure you have:

1.  **Environment Variables at the root of the learning-langchain repository:** If you haven't already, set up the required environment variables in a `.env` file at the root of the learning-langchain repository. See `.env.example` for the list of variables.

2.  **Supabase account and a Supabase API key:**
    *   To register for a Supabase account, go to [supabase.com](https://supabase.com) and sign up.
    *   Once you have an account, create a new project then navigate to the settings section.
    *   In the settings section, navigate to the API section to see your keys.
    *   Copy the project URL and service_role key and add them to the `.env` file as values for `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`.

3.  **Docker (optional):** Docker is required to run the Chroma vector database in the js implementation. Follow the instructions in the [README](../../README.md#docker-setup-and-usage) to install and set up Docker. After setting up Docker, run the following command to start the Chroma server:

```bash 
docker pull chromadb/chroma
docker run -p 8000:8000 chromadb/chroma

```

This will start the Chroma server on port 8000.

## Repository Structure

This directory contains the following structure:

```
├── js # JavaScript implementation
│ ├── src # Source code
│ │ ├── ingestion_graph # Ingestion graph components
│ │ ├── retrieval_graph # Retrieval graph components
│ │ ├── shared # Shared components
│ │ ├── configuration.ts # Configuration files
│ │ ├── graph.ts # Graph definition files
│ │ ├── state.ts # State definition files
│ │ └── utils.ts # Utility functions
│ ├── demo.ts # Demo script
│ ├── langgraph.json # LangGraph configuration file
│ ├── package.json # JavaScript dependencies
│ └── tsconfig.json # TypeScript configuration
└── py # Python implementation
    ├── src # Source code
    │ ├── ingestion_graph # Ingestion graph components
    │ ├── retrieval_graph # Retrieval graph components
    │ ├── shared # Shared components
    │ ├── configuration.py # Configuration files
    │ ├── graph.py # Graph definition files
    │ ├── state.py # State definition files
    │ └── utils.py # Utility functions
    ├── demo.py # Demo script
    ├── langgraph.json # LangGraph configuration file
    └── pyproject.toml # Python dependencies
```

## Setting up the Environment

### Python

1.  **Create a virtual environment:**

    ```bash
    python -m venv .venv
    ```

2.  **Activate the virtual environment:**

    *   macOS/Linux:

    ```bash
    source .venv/bin/activate
    ```

    *   Windows:

    ```bash
    .venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -e .
    ```

### JavaScript

1.  **Install dependencies:**

    ```bash
    npm install
    ```

## Running the Application

### Python

1.  **Navigate to the `py` directory:**

    ```bash
    cd ch9/py
    ```

2.  **Run the demo script:**

    ```bash
    python demo.py
    ```

### JavaScript

1.  **Navigate to the `js` directory:**

    ```bash
    cd ch9/js
    ```

2.  **Run the demo script:**

    ```bash
    node demo.ts
    ```

## Local Development Server

You can run the local development server for either JavaScript or Python implementations from the root directory of the learning-langchain repository:

##### For JavaScript:
```bash
# Using npm script
npm run langgraph:dev
```

##### For Python:
You have two options:

1. Using the CLI directly:
```bash
langgraph dev -c ch9/py/langgraph.json --verbose
```

2. Using the installed script command:
```bash
langgraph-dev
```

Note: To use the script command, make sure you have installed the package in development mode (`pip install -e .`).

This will start the local development server on port 2024 and redirect you to the langsmith UI for debugging and tracing.

## Deploying the Application

To deploy your LangGraph agent to a cloud service, you can either use LangGraph's cloud as per this [guide](https://langchain-ai.github.io/langgraph/cloud/quick_start/?h=studio#deploy-to-langgraph-cloud) or self-host it as per this [guide](https://langchain-ai.github.io/langgraph/how-tos/deploy-self-hosted/).

### Using LangGraph CLI

1.  **Configure LangGraph:**

    *   Ensure that the `langgraph.json` file is correctly configured to point to the entry points of your graphs.

2.  **Deploy the application:**

    *   Run the following command from the root of the repository:

    ```bash
    npx @langchain/langgraph-cli deploy -c ch9/js/langgraph.json
    ```

    *   Or, for python:

    ```bash
    npx @langchain/langgraph-cli deploy -c ch9/py/langgraph.json
    ```

    *   Follow the prompts to deploy your application.

## Interacting with the Deployed Application

Once deployed, you can interact with the application using the LangGraph SDK. The `demo.ts` and `demo.py` files provide examples of how to create threads and invoke the deployed graphs.

## Troubleshooting

*   **Dependency Issues:** Ensure all dependencies are installed correctly using `pip install -e .` (Python) or `npm install` (JavaScript).
*   **Environment Variables:** Verify that all required environment variables are set correctly in the `.env` file in the root of the learning-langchain repository.
*   **Docker:** Ensure that Docker is running and that the container is set up correctly.
*   **API URL:** Ensure that the `LANGGRAPH_API_URL` environment variable is set to the correct URL of your LangGraph server.
*   **File Paths:** Double-check that all file paths in the configuration files are correct.
