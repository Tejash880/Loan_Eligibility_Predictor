FROM python:3.10-slim
 
WORKDIR /app
 
COPY . /app
 
RUN pip install --no-cache-dir -r requirements.txt
 
RUN python model_train.py
 
EXPOSE 10000
 
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
 
