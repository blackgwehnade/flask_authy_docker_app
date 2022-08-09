FROM python:3.8

COPY app /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 4000

CMD ["python", "app.py"]