FROM multiarch/qemu-user-static:x86_64-aarch64 as qemu

FROM arm64v8/python:3.9-bullseye
COPY --from=qemu /usr/bin/qemu-aarch64-static /usr/bin
COPY ./requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg -y
RUN pip install --default-timeout=1000 -r requirements.txt
WORKDIR /app
ENV FLASK_APP family_foto
ENV FLASK_RUN_HOST 0.0.0.0
COPY . .
CMD ["flask", "run"]
