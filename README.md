# SD_Assignment1
Grades Tracker App

# Grade & What-If Tracker

Simple app to track course assessments, compute current weighted grade, show remaining weight, and run what-if targets.

## Run backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
cd ..
uvicorn backend.app:app --reload

Open 
http://127.0.0.1:8000/

Testing:
run pytest -q
