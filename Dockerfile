FROM python:3.6-alpine

WORKDIR /app

COPY [ "./requeriments.txt" , "/app" ]

RUN mkdir -p /app/uploads
RUN pip install -r requeriments.txt

COPY . /app

EXPOSE 4444
EXPOSE 4545

CMD [ "python" , "main.py" ]