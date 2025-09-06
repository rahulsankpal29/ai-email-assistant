# AI Email Assistant

This is my hackathon project — an **AI-powered email assistant**.

## What it does
- Reads emails from Gmail/Outlook (via IMAP)
- Finds support/query/help requests
- Marks emails as **urgent** or **not urgent**
- Checks **sentiment** (positive/negative/neutral)
- Generates **AI reply drafts**
- Shows everything on a simple **React dashboard**

## Tech Stack
- **Backend:** FastAPI (Python)
- **Frontend:** React (JavaScript)
- **Database:** SQLite
- **AI Models:** OpenAI / Hugging Face

## How to Run
### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
