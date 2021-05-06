FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /application
COPY . /application/
RUN pip install -r requirements.txt
