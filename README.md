# Superproductive AI Agent

A unified platform for getting actionable insights from different productivity apps like Outlook, Microsoft Teams, and Microsoft Loop. The AI agent extracts tasks from these sources, prioritizes them, and displays them in a modern UI.

## 📚 Documentation

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

4. Run the backend:
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
- **AI**: Hugging face transformer for task extraction and prioritization

## License

MIT

