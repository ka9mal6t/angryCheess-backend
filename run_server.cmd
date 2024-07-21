@echo on
call .venv\Scripts\activate
start cmd /k uvicorn app.main:app --port 8000