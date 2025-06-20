FROM python:3.13-bookworm

WORKDIR /app
COPY ../ ./

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "backend.API:app", "--host", "0.0.0.0", "--port", "8000"]
