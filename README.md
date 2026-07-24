# FYP: A-Human-Instruction-Driven-Agent-Platform-with-Workflow-Generation

PolyuHK FYP
by Tse Yiu Fai, Alan 25001163d

Project Description：
This project aims to design and develop an agent platform that enables the
generation and modification of agent workflows from natural language instructions.
The platform allows users to describe tasks in plain language, and automatically
translates them into executable workflows composed of modular agents. It further
supports interactive editing and refinement of the generated workflows. Based on this
platform, two representative agent applications will be implemented: an automatic
literature retrieval agent and a campus policy Q&A agent. The project emphasizes
human-AI collaboration, workflow generation, and extensibility

Expected outcome：
A functional agent platform featuring instructionto-workflow generation and an interactive
workflow editor, along with two integrated
agent applications (literature download and
campus policy Q&A), with evaluation on
generation accuracy, usability, and task
completion effectiveness.

Knowledge/ Skill/ Tools Required:
Python Programming; AI agent


System design:

Frontend Layer: (Workflow Editor + Chat Interface + Dashboard)

API Gateway Layer: (RESTful API + WebSocket for real-time updates)

Core Engine Layer: Workflow Engine  + Instruction Parser  (NL → Workflow Generator) 

Agent Module Layer: Search Agent / Parse Agent / QA Agent / Custom Agent

Infrastructure Layer: (LLM API + Database + File Storage + Vector DB)   

The Frontend Layer handles user interaction and comprises three main modules: a dialog interface for natural language input, a visual workflow editor, and an execution monitoring dashboard. Users can generate workflows through dialogue or directly drag and drop to modify them in the editor.

The API Gateway Layer manages frontend and backend communication. A RESTful API handles CRUD operations, and WebSockets handle real-time status updates during workflow execution (e.g., a node is executing, completed, or encountered an error).

The Core Engine Layer is the platform's core, containing two key components. The Workflow Engine parses workflow definitions, executes nodes in topological order, handles branch/conditional logic, and manages data transfer between nodes. The Instruction Parser receives natural language instructions, calls the LLM for intent understanding and task decomposition, and ultimately outputs a structured workflow definition.

The Agent Module Layer is the registry for all available agents. Each agent is an independent, standardized module with unified input/output interfaces. The platform can dynamically load and combine these agents.

The Infrastructure Layer provides underlying service support, including LLM API calls, persistent storage, file management, and a vector database (used for semantic retrieval of campus policy Q&A).



Tech Stack:
Frontend	        React + TypeScript + React Flow + Tailwind + Zustand
Backend	            Python + FastAPI + Pydantic
LLM	OpenAI          GPT-4o (openai SDK)
Database	        PostgreSQL/SQLite + ChromaDB
Communication	    REST + WebSocket
Deploy/Container    Docker Compose
