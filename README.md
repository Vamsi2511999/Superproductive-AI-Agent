# Superproductive AI Agent

A unified platform for getting actionable insights from different productivity apps like Outlook, Microsoft Teams, and Microsoft Loop. The AI agent extracts tasks from these sources, prioritizes them, and displays them in a modern UI.

## 📚 Documentation

**New here? Start with these guides:**
- **[VISUAL_OVERVIEW.md](VISUAL_OVERVIEW.md)** - Visual diagrams and quick reference
- **[DELIVERY_CHECKLIST.md](DELIVERY_CHECKLIST.md)** - What's included and ready to use
- **[INDEX.md](INDEX.md)** - Complete documentation navigator

**Full Documentation Set:**
- [SETUP.md](SETUP.md) - Installation and configuration guide
- [USER_GUIDE.md](USER_GUIDE.md) - How to use the application
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical design and architecture
- [DIAGRAMS.md](DIAGRAMS.md) - System diagrams and data flows
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Complete feature breakdown
- [PROJECT_COMPLETE.md](PROJECT_COMPLETE.md) - Project overview

## Features

- **Multi-Source Task Extraction**: Extracts tasks from:
  - Outlook emails (email body, subject, sender)
  - Microsoft Loop/To-Do (actionable items with ETA dates)
  - Teams/Slack messages (with sender name)

- **AI-Powered Prioritization**: Uses AI to intelligently prioritize extracted tasks

- **Modern Dashboard UI**: 
  - View all prioritized tasks
  - Date-based filtering
  - Priority-based sorting
  - Source identification

- **Chat Interface**: Natural language interaction for task extraction and prioritization

## Project Structure

```
superproductive_AI_Agent/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── main.py      # FastAPI application
│   │   ├── ai_engine.py # AI task extraction & prioritization
│   │   ├── models.py    # Data models
│   │   └── routes.py    # API endpoints
│   ├── data/            # Dummy data sources
│   └── requirements.txt
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API services
│   │   └── App.jsx
│   └── package.json
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

5. Run the backend:
```bash
uvicorn app.main:app --reload
```

Backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

Frontend will run on `http://localhost:5173`

## Usage

1. Start both backend and frontend servers
2. Open `http://localhost:5173` in your browser
3. View extracted and prioritized tasks from all sources
4. Use date filters to narrow down tasks
5. Use the chat interface to ask questions or get insights

## API Endpoints

- `GET /api/tasks` - Get all extracted tasks
- `POST /api/tasks/extract` - Extract tasks from sources
- `POST /api/tasks/prioritize` - Prioritize tasks
- `POST /api/chat` - Chat with AI assistant
- `GET /api/tasks/filter?start_date=...&end_date=...` - Filter tasks by date

## Technologies Used

- **Backend**: Python, FastAPI, OpenAI API
- **Frontend**: React, Vite, Tailwind CSS
- **Data**: JSON format for dummy data
- **AI**: OpenAI GPT for task extraction and prioritization

## License

MIT
