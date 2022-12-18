FROM python:3.10.7

WORKDIR /app

EXPOSE 8000

COPY . /app/
COPY .env /app/.env

RUN pip install -r requirements.txt

RUN chmod +x startup.sh

# RUN python main.py > main.log &

# ENTRYPOINT ["python", "server.py"]

ENTRYPOINT [ "sh", "startup.sh" ]