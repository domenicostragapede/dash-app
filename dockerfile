FROM python:3

COPY requirements.txt /
RUN pip install -r /requirements.txt

RUN mkdir /crossnova
WORKDIR /crossnova
COPY ./ ./

EXPOSE 8050
CMD ["python", "./app.py"]
