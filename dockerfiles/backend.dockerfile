FROM python:3.13-bookworm

WORKDIR /app

COPY ../requirements.txt ./
RUN pip install -r requirements.txt

COPY ../backend ./backend
COPY ../db ./db
COPY ../setup ./setup
COPY ../main.py ./

RUN ls


EXPOSE 8000

CMD ["uvicorn", "backend.API:app", "--host", "0.0.0.0", "--port", "8000"]
