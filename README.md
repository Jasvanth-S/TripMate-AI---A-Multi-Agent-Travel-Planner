<div align="center">

# ✈️ TripMate AI
### **Multi-Agent AI Travel Planner powered by LangGraph**

*Plan complete trips using AI-powered agents for flights, hotels, and intelligent itinerary generation.*

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-blueviolet?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-AI-green?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-LLM-orange?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/Open%20Source-MIT-success?style=for-the-badge)

</p>

---

### 🚀 Intelligent Travel Planning Through AI Agents

**TripMate AI** transforms a simple natural language travel request into a complete travel experience using a **LangGraph-powered multi-agent workflow**.

Instead of manually searching across multiple websites for flights, hotels, attractions, and schedules, TripMate AI coordinates specialized AI agents that collaborate to produce a practical, structured, and personalized travel plan.

</div>

---

# 🌍 Why TripMate AI?

Planning travel is fragmented.

You search flights on one website.

Hotels on another.

Tourist places elsewhere.

Then spend time organizing everything into an itinerary.

**TripMate AI automates the entire workflow.**

Simply ask:

> **"Plan a 5-day trip to Japan with a budget of $1800."**

TripMate AI will intelligently:

✅ Research flights

✅ Discover hotels

✅ Create daily itineraries

✅ Organize activities

✅ Produce a polished travel plan

—all within one AI workflow.

---

# ✨ Key Features

## ✈️ Flight Research Agent

- Searches available flights
- Uses AviationStack API
- Considers travel dates
- Finds suitable routes

---

## 🏨 Hotel Research Agent

- Searches hotels using Tavily
- Suggests accommodations
- Budget-aware recommendations
- Location-based results

---

## 🗺️ Itinerary Planning Agent

Generates:

- Daily schedules
- Attractions
- Restaurants
- Local transportation
- Time allocation
- Budget estimation

---

## 🤖 LangGraph Multi-Agent Workflow

Each agent has a dedicated responsibility.

```
          User Prompt
               │
               ▼
     ┌───────────────────┐
     │ LangGraph Router  │
     └─────────┬─────────┘
               │
     ┌─────────┼─────────┐
     ▼         ▼         ▼
 Flight     Hotel    Itinerary
 Agent      Agent      Agent
     └─────────┼─────────┘
               ▼
      Response Generator
               ▼
         Final Travel Plan
```

---

## 💾 Persistent Conversations

Supports:

- PostgreSQL checkpointing
- Conversation history
- Stateful travel planning
- Session persistence

---

## ⚡ Lightning Fast LLM Responses

Powered by **Groq LLMs** for:

- High-speed inference
- Intelligent reasoning
- Natural conversation
- Structured responses

---

# 🧠 Technology Stack

| Category | Technologies |
|-----------|--------------|
| Language | Python 3.10+ |
| Backend | FastAPI |
| AI Framework | LangGraph |
| LLM Framework | LangChain |
| LLM Provider | Groq |
| Flight Search | AviationStack API |
| Hotel Search | Tavily API |
| Database | PostgreSQL |
| Frontend | HTML • CSS • JavaScript • Jinja2 |

---

# 📂 Project Structure

```text
TripMate-AI/
│
├── app.py
├── backend.py
├── requirements.txt
│
├── static/
│   ├── css/
│   ├── js/
│   └── assets/
│
├── templates/
│   └── index.html
│
└── tools/
    ├── flights.py
    ├── hotels.py
    └── search.py
```

---

# ⚙️ Prerequisites

Before running the project, ensure you have:

- Python 3.10+
- PostgreSQL
- Groq API Key
- Tavily API Key
- AviationStack API Key

---

# 🔐 Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/travel_db

GROQ_API_KEY=your_groq_api_key

AVIATIONSTACK_API_KEY=your_api_key

TAVILY_API_KEY=your_api_key

DEFAULT_ORIGIN_IATA=DAC
```

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/tripmate-ai.git

cd tripmate-ai
```

Create virtual environment

```bash
python -m venv .venv
```

Activate

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:8000/
```

---

# 🚀 REST API

## Health Check

```http
GET /health
```

---

## Generate Travel Plan

```http
POST /api/travel
```

Example

```bash
curl -X POST http://127.0.0.1:8000/api/travel \
-H "Content-Type: application/json" \
-d '{
"message":"Plan a 3-day trip to Tokyo with a budget of $1200"
}'
```

---

# 🧩 Workflow

```text
User Request
      │
      ▼
LangGraph Supervisor
      │
      ├──────────────┐
      ▼              ▼
 Flight Agent   Hotel Agent
      │              │
      └──────┬───────┘
             ▼
     Itinerary Agent
             │
             ▼
     Response Formatter
             │
             ▼
   Complete Travel Plan
```

---

# 🌟 Example Prompt

```text
Plan a 7-day honeymoon trip to Switzerland from Chennai.

Budget:
₹2,50,000

Preferences:

Luxury Hotels

Mountain Views

Adventure Activities

Vegetarian Food

Train Travel
```

---

# 🎯 Future Roadmap

- ✅ Live Flight Booking
- ✅ Hotel Booking Integration
- ✅ Google Maps Integration
- ✅ Weather Forecast Agent
- ✅ Currency Converter
- ✅ Visa Requirement Agent
- ✅ Expense Tracker
- ✅ AI Packing Assistant
- ✅ Local Event Discovery
- ✅ Voice Assistant
- ✅ PDF Travel Guide Export
- ✅ Multi-language Support
- ✅ Mobile App
- ✅ AI Budget Optimizer

---

# 🤝 Contributing

Contributions are always welcome.

1. Fork the repository

2. Create your feature branch

```bash
git checkout -b feature/amazing-feature
```

3. Commit changes

```bash
git commit -m "Add amazing feature"
```

4. Push

```bash
git push origin feature/amazing-feature
```

5. Open a Pull Request

---

# 💡 Built With

- ❤️ LangGraph
- ❤️ LangChain
- ❤️ FastAPI
- ❤️ Groq
- ❤️ PostgreSQL
- ❤️ Tavily
- ❤️ AviationStack

---

# ⭐ Support the Project

If you found this project helpful,

please consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates future development.

---

<div align="center">

## ✈️ TripMate AI

### **Making Intelligent Travel Planning Effortless with Multi-Agent AI**

**Built with ❤️ using LangGraph, FastAPI & Groq**

⭐ Star the repository if you like this project!

</div>