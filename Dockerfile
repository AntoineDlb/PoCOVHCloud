FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_PORT=8501

WORKDIR /app

RUN addgroup --system appgroup && adduser --system --ingroup appgroup --home /app appuser

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py README.md .env.example ./

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]