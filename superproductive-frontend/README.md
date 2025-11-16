# Superproductive AI Agent - Angular Frontend (MVP)

## Quick start
1. Create a new Angular project: `ng new superproductive-frontend --routing=false --style=css` (skip if you already have one)
2. Copy the files from this document into `src/app` and `src/environments` (create directories if needed).
3. Install dependencies (Angular CLI already provides core deps). If you want local mock backend, run json-server or provide a simple FastAPI mock.

## Local mock JSON backend (quick)
Create `mock/tasks.json`:
```
{
  "tasks": [
    { "id": 1, "title": "Submit weekly report", "source": "email", "eta": "2025-11-18", "priority": "High" },
    { "id": 2, "title": "Prepare slides", "source": "todo", "eta": "2025-11-19", "priority": "Medium" }
  ]
}
```
Install `json-server`:
```
npm i -g json-server
json-server --watch mock/tasks.json --routes routes.json --port 8000
```
Use `routes.json` to map `/api/tasks` -> `/tasks` if needed.

## Notes
- Replace `environment.apiUrl` with your backend endpoint.
- The `ApiService` expects endpoints: `/api/tasks`, `/api/extract`, `/api/chat`.
- For MVP you can keep data local and mock API responses.