FROM python:3.9

WORKDIR /app

ENV FLASK_APP=app.py 

ENV FLASK_DEBUG=development

COPY . .

RUN apt update && apt install -y sqlite3 vim less
RUN pip install -r requirements.txt


RUN flask db init
RUN flask db migrate -m "init"
RUN flask db upgrade
CMD [ "python", "app.py" ]
