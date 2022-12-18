FROM python:3.10.7

WORKDIR /app

COPY . /app/
COPY .env /app/.env

RUN pip install -r requirements.txt

RUN chmod +x startup.sh

EXPOSE 8000 2222

# RUN python main.py > main.log &

# ENTRYPOINT ["python", "server.py"]

ENTRYPOINT [ "/app/startup.sh" ]