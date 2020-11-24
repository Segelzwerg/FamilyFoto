FROM python:3.9-buster
COPY ./requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install -y libgl1-mesa-dev
RUN pip install -r requirements.txt
WORKDIR /app
ENV FLASK_APP family_foto
ENV FLASK_RUN_HOST 0.0.0.0
COPY . .
CMD ["flask", "run"]