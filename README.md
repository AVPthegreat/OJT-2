# AI Viva Interview Platform

> 🎤 Practice DSA interviews with an AI-powered voice bot that speaks like your professor

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Ollama (for local LLM)
- CUDA GPU (recommended for real-time inference)

### Backend Setup

1. **Install Ollama and pull Mistral**

```bash
# Install Ollama from https://ollama.ai
ollama pull mistral
```

2. **Create virtual environment and install dependencies**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Add professor voice recording**

```bash
# Place your 2-3 min professor voice recording at:
# data/professor_audio/professor.wav
```

4. **Run the backend**

```bash
python main.py
# or
uvicorn main:app --reload
```

### 🐳 Docker Setup (Recommended)

**Development Mode** (with hot reload):

```bash
# Start all services
./scripts/dev.sh start

# View logs
./scripts/dev.sh logs

# Stop
./scripts/dev.sh stop
```

**Production Mode**:

```bash
# Full deployment
./scripts/prod.sh deploy

# Check status
./scripts/prod.sh status
```

| Service     | Dev URL                    | Prod URL                 |
| ----------- | -------------------------- | ------------------------ |
| Backend API | http://localhost:8000      | http://localhost:80      |
| API Docs    | http://localhost:8000/docs | http://localhost:80/docs |
| Ollama      | http://localhost:11434     | Internal                 |
| ChromaDB    | http://localhost:8001      | Internal                 |

### Frontend Setup (Coming Soon)

```bash
cd frontend
npm install
npm run dev
```

## 🏗️ Architecture

```
Student speaks → Whisper (STT) → LLM + RAG → XTTS (Voice Clone) → Professor responds
```

## 📁 Project Structure

```
├── backend/
│   ├── main.py              # FastAPI application
│   ├── routers/             # API endpoints
│   │   └── interview.py     # Interview session management
│   └── services/
│       ├── stt_service.py   # Speech-to-Text (Whisper)
│       ├── tts_service.py   # Text-to-Speech (XTTS)
│       ├── llm_service.py   # LLM + RAG
│       └── eval_service.py  # Response scoring
├── frontend/                 # React/Next.js UI
├── data/
│   ├── professor_audio/     # Voice recordings
│   └── dsa_knowledge/       # Knowledge base documents
└── ml/                       # ML model training
```

## 🎯 Features

- **Voice-to-Voice**: Full audio conversation with AI interviewer
- **Voice Cloning**: AI speaks in your professor's voice
- **DSA Focus**: Knowledge grounded in data structures & algorithms
- **Real-time**: Low latency voice interactions
- **Scoring**: ML-powered evaluation of your responses

## 📊 Scoring Parameters

| Parameter          | Description                                      |
| ------------------ | ------------------------------------------------ |
| Technical Accuracy | Correctness of concepts and algorithms           |
| Clarity            | How well-structured and clear the explanation is |
| Depth              | Coverage of edge cases, complexity, trade-offs   |
| Confidence         | Speaking pace and hesitation patterns            |
| Communication      | Grammar, articulation, vocabulary                |

## 🛠️ Development

### Building Knowledge Base

```bash
cd backend
python -c "from services.llm_service import LLMService; s = LLMService(); s.build_knowledge_base()"
```

### Testing API

```bash
# Start interview session
curl -X POST http://localhost:8000/api/interview/start -H "Content-Type: application/json" -d '{"subject": "DSA"}'

# Check health
curl http://localhost:8000/health
```

## 📝 License

MIT License - Built for OJT Project
