# VC Discovery Platform

AI-powered startup discovery and enrichment platform built using **Next.js + FastAPI + LLM integration**.

This application allows users to:

- Add startup/company profiles  
- Store structured metadata (industry, stage, location, website)  
- Enrich companies using AI + website scraping  
- Cache enrichment results to avoid repeated LLM calls  
- Deploy fully in production (Vercel + Render)

---

## 🚀 Live Demo

Frontend:  
[Vercel App](https://vc-search.vercel.app/)

Backend API:  
[Render Project](https://vc-discovery-final.onrender.com)

---

## 🧠 Problem Statement

Investors and founders often struggle to quickly understand what a startup actually does from limited data.

This platform solves that by:

- Scraping the company website  
- Sending structured prompts to an LLM  
- Extracting structured intelligence  
- Caching results in the database  

---

## 🏗 Architecture Overview

### Frontend
- Next.js (App Router)
- TypeScript
- Tailwind CSS
- Client-side + server-side data fetching

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- REST API architecture

### AI Layer
- Gemini API (LLM)
- Structured JSON prompting
- Output parsing + validation

### Deployment
- Frontend → Vercel
- Backend → Render
- Environment-based configuration

---

## ✨ Features

- Create & manage company profiles
- AI-powered enrichment from website URL
- Structured output:
  - Summary
  - What they do
  - Keywords
  - Signals
  - Sources
- Caching of enrichment results
- Production-ready environment variable handling
- Clean separation of frontend & backend
- Error handling for scraping + LLM failures

---

## 📦 Project Structure

```

vc-discovery/
│
├── frontend/          # Next.js app
│   ├── app/
│   ├── components/
│   └── ...
│
├── backend/           # FastAPI app
│   ├── models.py
│   ├── routes.py
│   ├── enrichment.py
│   └── db.py
│
└── README.md

````

---

## 🛠 Local Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/sagnik-create/VC-Discovery-final
cd VC-Discovery-final
````

---

### 2️⃣ Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file:

```
DATABASE_URL=sqlite:///./vc_scout.db
GEMINI_API_KEY=your_api_key_here
```

Run server:

```bash
uvicorn main:app --reload
```

Backend runs at:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### 3️⃣ Frontend Setup

```bash
cd frontend
npm install
```

Create `.env.local`:

```
NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000
```

Run:

```bash
npm run dev
```

Frontend runs at:
[http://localhost:3000](http://localhost:3000)

---

## 🌍 Production Deployment

### Vercel Environment Variable

```
NEXT_PUBLIC_API_BASE=https://your-backend.onrender.com
```

### Render Environment Variables

```
DATABASE_URL=sqlite:///./vc_scout.db
GEMINI_API_KEY=your_api_key
```

---

## 🔐 Design Decisions

* Used structured JSON prompting to reduce hallucination
* Implemented caching to avoid repeated LLM cost
* Separated enrichment logic from route handlers
* Used environment-based configuration for portability
* Avoided tight coupling between frontend and backend

---

## 🧪 Future Improvements

* PostgreSQL migration
* Background task queue (Celery / Redis)
* Vector embeddings for semantic search
* Authentication layer
* Investor dashboard analytics
* Rate limiting

---

## 📈 What This Demonstrates

* Full-stack engineering
* API design
* LLM integration
* Production deployment
* Environment management
* Debugging real-world deployment issues
* CORS handling
* Error resilience

---

## 👤 Author

Sagnik Dey
Computer Science & AI Student
Full-stack Developer
AI Systems Builder
