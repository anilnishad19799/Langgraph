# LangGraph MCP Application

A LangGraph-based conversational AI system integrating MCP (Model Context Protocol), Qdrant for long-term vector memory, and Checkpointer for short-term memory. Designed for intelligent, context-aware, and persistent dialogue management.

---

## ⚙️ Tech Stack

- **LangChain / LangGraph** – builds the conversational reasoning graph  
- **MCP (Model Context Protocol)** – standardizes communication between the AI agent and external tools, APIs, and memory systems  
- **Memo0AI** – memory management interface  
- **Qdrant** – long-term vector storage  
- **Checkpointer** – short-term, thread-based session memory  
- **FastAPI** – backend REST service  
- **Docker / Docker Compose** – containerized deployment  

---

## 🔐 Environment Setup

Create a `.env` file in the project root with your API credentials:  
OPENAI_API_KEY=<your_openai_api_key>  
LANGSMITH_API_KEY=<your_langsmith_api_key>  
QDRANT_URL=<your_qdrant_cloud_url>  
QDRANT_API_KEY=<your_qdrant_api_key>  

> Get Qdrant credentials from your Qdrant Cloud account.

---

## 🐳 Docker Setup

Build and run containers:  
docker-compose build  
docker-compose up  

Open your browser at:  
http://localhost:8000  

The FastAPI backend integrates MCP, Qdrant, and Checkpointer for memory-based conversation handling.

---

## 💻 Local Development (Without Docker)

Create and activate a virtual environment:  
python -m venv venv  
source venv/bin/activate  (Linux/macOS)  
venv\Scripts\activate     (Windows)  

Install dependencies:  
pip install -r requirements.txt  

Run the FastAPI app:  
uvicorn app.main:app --reload  

---

## 🔗 Qdrant Cloud Setup

1. Go to [Qdrant Cloud](https://cloud.qdrant.io/)  
2. Create a free instance  
3. Copy your API key and instance URL  
4. Add them to the `.env` file:  
QDRANT_URL=`https://<your-instance-id>.qdrant.cloud  `
QDRANT_API_KEY=`<your-api-key>`  

---

## 🧠 Memory Architecture

- **Short-term:** Checkpointer stores active session context (thread-based)  
- **Long-term:** Qdrant persists conversation history for future retrieval  
- **Context Management:** MCP bridges memory layers and external tools for coherent dialogue flow  

---

## 🚀 Contributing

Feel free to fork, improve, and submit pull requests. Suggestions and enhancements are welcome.

---

## 📄 License

This project is licensed under the **MIT License**.
