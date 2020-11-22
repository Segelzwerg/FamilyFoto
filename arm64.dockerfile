FROM multiarch/qemu-user-static:x86_64-aarch64 as qemu

FROM arm64v8/python:3.9-slim
COPY --from=qemu /usr/bin/qemu-aarch64-static /usr/bin
COPY ./requirements.txt requirements.txt
RUN uname -a
RUN apt-get update -qq
RUN apt-get install build-essential git -yq
# this is temporary until opencv-python is released on pypi with arm64 support
RUN pip install --default-timeout=1000 git+https://github.com/skvark/opencv-python.git
RUN pip install --default-timeout=1000 -r requirements.txt
WORKDIR /app
ENV FLASK_APP family_foto
ENV FLASK_RUN_HOST 0.0.0.0
COPY . .
CMD ["flask", "run"]