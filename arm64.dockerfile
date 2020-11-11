FROM arm64v8/python:3.9-alpine
COPY ./requirements.txt requirements.txt
RUN apk update
RUN apk add cmake
RUN pip install --default-timeout=1000 -r requirements.txt
WORKDIR /app
ENV FLASK_APP family_foto
ENV FLASK_RUN_HOST 0.0.0.0
COPY . .
CMD ["flask", "ruuupdatepdaten"]