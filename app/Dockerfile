FROM python:3.11-slim-bullseye

COPY . /app

RUN pip install pyserial paho-mqtt

CMD ["python", "/app/Main.py"]