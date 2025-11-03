# LangGraph MCP Application

This repository contains a LangGraph-based project using MCP (Multi-Chain Processing) with Qdrant as the long-term vector database and Checkpointer for short-term memory. The system is built to handle conversational AI with persistent memory using threads.

---

## 🛠 Tech Stack

- LangChain & LangGraph – for building the conversational graph and agent logic  
- MCP – Multi-Chain Processing for orchestration  
- Memo0AI – memory management  
- Qdrant – vector database for long-term memory  
- Checkpointer – short-term memory  
- FastAPI – backend API (app/main.py)  
- Docker & Docker Compose – containerization and orchestration  

---

## ⚙️ Environment Variables

Create a `.env` file in the root of the project with the following keys:  
OPENAI_API_KEY=<your_openai_api_key>  
LANGSMITH_API_KEY=<your_langsmith_api_key>  
QDRANT_URL=<your_qdrant_cloud_url>  
QDRANT_API_KEY=<your_qdrant_api_key>  
Note: You need to create a Qdrant Cloud instance to get the QDRANT_URL and QDRANT_API_KEY.

---

## 🐳 Docker Setup and Run

Build Docker images and run containers using:  
docker-compose build  
docker-compose up  
This will start the FastAPI backend along with any additional services defined in docker-compose.yml.  
Access the application by opening your browser and navigating to:  
http://localhost:8000  
The FastAPI app will serve your endpoints and interact with MCP, Qdrant, and Checkpointer for memory management.

---

## 📦 Running Locally Without Docker

Create a virtual environment and activate it:  
python -m venv venv  
source venv/bin/activate  (for Linux/macOS)  
venv\Scripts\activate     (for Windows)  
Install dependencies:  
pip install -r requirements.txt  
Run the FastAPI app:  
uvicorn app.main:app --reload  

---

## 🔗 Qdrant Cloud Setup

Go to Qdrant Cloud (https://cloud.qdrant.io/), create a free instance, copy your API Key and Instance URL, and add them to your `.env` file:  
QDRANT_URL=https://<your-instance-id>.qdrant.cloud  
QDRANT_API_KEY=<your-api-key>  

---

## 📝 Notes

- Short-term memory is managed by Checkpointer threads for session-specific context  
- Long-term memory is stored in Qdrant for persistent knowledge retrieval  
- Ensure all API keys are valid and have correct permissions  
- Docker Compose handles container orchestration and service dependencies  

---

## 🚀 Contributing

Feel free to open issues or submit pull requests for improvements.

---

## 📄 License

This project is licensed under the MIT License.
