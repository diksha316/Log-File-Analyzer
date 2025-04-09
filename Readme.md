Log File Analyzer (FastAPI + React)

This project is a full-stack AI-powered tool for analyzing `.log` and `.txt` files. Users can upload log files via a React frontend, and the FastAPI backend processes them using Google Gemini 1.5 Flash and vector search to generate a detailed error summary.

---

 Tech Stack

Frontend: React
Backend: FastAPI
AI Model: Google Gemini 1.5 Flash
Embeddings & Vector Store: HuggingFace + FAISS



 Backend Setup (FastAPI)

 Navigate to the backend directory:

```bash
cd backend
```

 Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

 Install dependencies:

```bash
pip install -r requirements.txt
```

 Run the FastAPI server:

```bash
uvicorn main:app --reload
```

---

 Frontend Setup (React)

 Navigate to the frontend directory:

```bash
cd frontend
```

 Install dependencies:

```bash
npm install
```

 Start the frontend app:

```bash
npm run dev  # or npm start
```

> The app runs on `http://localhost:3000` and interacts with the FastAPI backend at `http://localhost:8000`.

---

 Features

- Upload `.log` or `.txt` files from UI
- AI-based analysis and summary
- Error categorization and count
- Tabular status code report
- Clean, user-friendly interface



