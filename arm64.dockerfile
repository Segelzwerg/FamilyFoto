FROM arm64v8/python:3.9-slim
COPY ./requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install cmake
RUN pip install --default-timeout=1000 -r requirements.txt
WORKDIR /app
ENV FLASK_APP family_foto
ENV FLASK_RUN_HOST 0.0.0.0
COPY . .
CMD ["flask", "ruuupdatepdaten"]