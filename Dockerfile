FROM python:3.10-slim

COPY . /agc_kb_tg_bot

WORKDIR /agc_kb_tg_bot

RUN mkdir -m 777 /var/log/agc_bot_logs/
RUN pip install -r requirements.txt
RUN git config --global --add safe.directory .
RUN git config --global --add safe.directory /var/log/agc_bot_logs/

CMD ["python", "/agc_kb_tg_bot/main.py"]




