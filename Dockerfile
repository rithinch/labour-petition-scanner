FROM python:3.9.10-slim-buster
RUN apt-get update && apt-get install python-tk python3-tk tk-dev -y

# Create app directory
RUN mkdir -p /usr/src/app

COPY ./requirements.txt /usr/src/app
WORKDIR /usr/src/app

RUN pip install -r requirements.txt
COPY . /usr/src/app

EXPOSE 80

CMD ["streamlit", "run", "app.py", "--server.port", "80", "--server.enableXsrfProtection", "false"]