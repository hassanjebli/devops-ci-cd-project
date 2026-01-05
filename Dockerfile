FROM python:3.9

WORKDIR /app

ENV PYTHONPATH=/app

COPY . .

RUN pip install flask pytest

CMD ["python", "app/app.py"]
