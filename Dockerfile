FROM python:3.11-slim-bullseye

COPY app /app

RUN pip install pyserial

ENTRYPOINT ["python", "/app/Main.py"]