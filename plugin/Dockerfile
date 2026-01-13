FROM python:3.11-slim

ENV TZ=America/Sao_Paulo

RUN apt-get update && apt-get install -y tzdata

WORKDIR /app
COPY . .

RUN pip install flask

CMD ["python", "main.py"]

