[![codecov](https://codecov.io/gh/Segelzwerg/FamilyFoto/branch/master/graph/badge.svg?token=G695SHB57X)](https://codecov.io/gh/Segelzwerg/FamilyFoto)
![Python Check](https://github.com/Segelzwerg/FamilyFoto/workflows/Python%20Check/badge.svg)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/Segelzwerg/FamilyFoto.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Segelzwerg/FamilyFoto/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Segelzwerg/FamilyFoto.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Segelzwerg/FamilyFoto/context:python)

![Lines of code](https://img.shields.io/tokei/lines/github/segelzwerg/familyfoto)
![GitHub repo size](https://img.shields.io/github/repo-size/Segelzwerg/FamilyFoto)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/segelzwerg/family-foto/arm64?label=image%3Aarm64)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/segelzwerg/family-foto/amd64?label=image%3Aamd64)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/segelzwerg/familyfoto)](https://github.com/segelzwerg/familyfoto/releases)
# FamilyFoto
A self hosting photo sharing server.

## Setup
Currently we provide docker images for amd64 and arm64 architectures. They easiest way to deploy
 your own instance is to download one of the two docker-compose files. After that you need to create
 a folder where the app can store it's data. By default it execpts this path to be `/media/usb
 /familyfoto`, but you can change that by changing the path in the docker-compose file
 
 ```dockerfile
volumes:
      - /media/usb/familyfoto:/app/instance
```
to 

 ```dockerfile
volumes:
      - /path/you/like:/app/instance
```
After that you can start it by

```shell script
docker-compose -f docker-compose.ARCHITECTURE.yml up
```

with `ARCHITECTURE` being one of `{"amd64", "arm64"}`.

:warning: This will use the latest version of Family Foto, if you want to use a specific version
 change the image tag in the docker-compose file to
 
 ```dockerfile
    image: segelzwerg/family-foto:arm64-vX.X.X
```
However this is only supported for up from `v0.3.0`. All tags can e found
[here](https://hub.docker.com/r/segelzwerg/family-foto/tags).