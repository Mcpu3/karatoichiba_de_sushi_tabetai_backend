FROM python:3.10.7

WORKDIR /app

EXPOSE 8000

COPY . /app/

RUN pip install -r requirements.txt

# RUN python main.py > main.log &

CMD ["python", "server.py"]