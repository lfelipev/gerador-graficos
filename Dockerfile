FROM python:3.9

EXPOSE 5000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

CMD gunicorn -b :$PORT main:app
