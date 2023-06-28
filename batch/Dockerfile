FROM python:3.10.11-slim-buster

RUN mkdir -p /src/

WORKDIR /src

COPY . /src/

RUN pip install -r requirements.txt

CMD ["python", "process.py"]