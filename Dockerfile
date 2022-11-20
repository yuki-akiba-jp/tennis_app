FROM python:3.9

WORKDIR /app

ENV FLASK_DEBUG=development

COPY . .

RUN apt update && apt install -y sqlite3 vim less
RUN pip install -r requirements.txt


CMD [ "python", "setup.py" ]
