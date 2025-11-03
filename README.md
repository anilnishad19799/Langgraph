# LangGraph MCP Application

A LangGraph-based conversational AI system integrating MCP (Model Context Protocol) with Qdrant for long-term vector memory and Checkpointer for short-term memory. Built for intelligent, context-aware, and persistent dialogue management.

---

## ⚙️ Tech Stack

- **LangChain / LangGraph** – conversational graph and agent logic  
- **MCP (Model Context Protocol)** – structured context handling and orchestration  
- **Memo0AI** – memory management interface  
- **Qdrant** – vector database for long-term memory  
- **Checkpointer** – manages short-term, thread-based session memory  
- **FastAPI** – backend REST service  
- **Docker / Docker Compose** – containerized deployment  

---

## 🔐 Environment Setup

Create a `.env` file in the project root with your API credentials:  
OPENAI_API_KEY=<your_openai_api_key>  
LANGSMITH_API_KEY=<your_langsmith_api_key>  
QDRANT_URL=<your_qdrant_cloud_url>  
QDRANT_API_KEY=<your_qdrant_api_key>  
Qdrant credentials can be generated from your Qdrant Cloud account.

---

## 🐳 Docker Setup

Build and start the services using:  
docker-compose build  
docker-compose up  
Once started, access the application at:  
http://localhost:8000  
The FastAPI backend integrates MCP, Qdrant, and Checkpointer for dynamic memory-based conversation handling.

---

## 💻 Local Development (Without Docker)

python -m venv venv  
source venv/bin/activate  (for Linux/macOS)  
venv\Scripts\activate     (for Windows)  
pip install -r requirements.txt  
uvicorn app.main:app --reload  
This will launch the FastAPI server locally for development and testing.

---

## 🔗 Qdrant Cloud Setup

1. Visit [Qdrant Cloud](https://cloud.qdrant.io/)  
2. Create a free instance  
3. Copy your API key and instance URL  
4. Add them to the `.env` file as:  
QDRANT_URL=https://<your-instance-id>.qdrant.cloud  
QDRANT_API_KEY=<your-api-key>

---

## 🧠 Memory Architecture

- **Short-term:** Checkpointer stores active session context (thread-based)  
- **Long-term:** Qdrant persists conversation history for future retrieval  
- **Context Management:** MCP (Model Context Protocol) bridges memory layers for coherent dialogue flow  

---

## 🚀 Contributing

Feel free to fork, improve, and submit pull requests. Suggestions and enhancements are welcome.

---

## 📄 License

This project is licensed under the **MIT License**.
