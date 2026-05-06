FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r backend/requirements.txt

# Train model at build time (dataset must be present)
RUN python backend/model_train.py

EXPOSE 10000

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--chdir", "backend", "app:app"]
