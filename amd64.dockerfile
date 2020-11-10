FROM python:3.9-buster
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR /app
ENV FLASK_APP family_foto/__init__.py
ENV FLASK_RUN_HOST 0.0.0.0
COPY /family_foto .
CMD ["flask", "run"]