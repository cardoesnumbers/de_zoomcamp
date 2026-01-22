#Week 1 Homework


Question 1. Understanding Docker images

Run docker with the python:3.13 image. Use an entrypoint bash to interact with the container.

I need a docker container of python 3.13 (in this case using the relevant Debian version), use bash as entrypoint, interactive. What I need to do:
- Pull the image
- command RUN + -it (interactive terminal) + setting the entrypoint + [docker image] (from Video)
- interact with it :)

@cardoesnumbers ➜ /workspaces/de_zoomcamp/w1_docker_terraform/w1_homework (main) $ docker --version
Docker version 28.5.1-1, build e180ab8ab82d22b7895a3e6e110cf6dd5c45f1d7
@cardoesnumbers ➜ /workspaces/de_zoomcamp/w1_docker_terraform/w1_homework (main) $ docker pull python:3.13-slim-bookworm
3.13-slim-bookworm: Pulling from library/python
c02d17997ce3: Pull complete 
147314ac1e23: Pull complete 
b6e251ce53ea: Pull complete 
5c2c99400009: Pull complete 
Digest: sha256:97e9392d12279f8c180eb80f0c7c0f3dfe5650f0f2573f7ad770aea58f75ed12
Status: Downloaded newer image for python:3.13-slim-bookworm
docker.io/library/python:3.13-slim-bookworm
@cardoesnumbers ➜ /workspaces/de_zoomcamp/w1_docker_terraform/w1_homework (main) $ docker run -it --entrypoint batch python:3.13-slim-bookworm
docker: Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: error during container init: exec: "batch": executable file not found in $PATH: unknown
Run 'docker run --help' for more information

@cardoesnumbers ➜ /workspaces/de_zoomcamp/w1_docker_terraform/w1_homework (main) $ docker run -it --entrypoint bash python:3.13-slim-bookw
orm

root@6b59de9441d8:/# python --version
Python 3.13.11
root@6b59de9441d8:/# which python
/usr/local/bin/python

root@6b59de9441d8:/# pip list
Package Version
------- -------
pip     25.3

root@6b59de9441d8:/# cat /etc/os-release
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
VERSION="12 (bookworm)"
VERSION_CODENAME=bookworm
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
root@6b59de9441d8:/# echo 'print("Hola desde  Docker!")' > hello.py                   
root@6b59de9441d8:/# python hello.py
Hola desde  Docker!

root@6b59de9441d8:/# exit
exit



Question 2. Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

- In Docker compose files the containers or services are automatically connected (to the same network) using their service names (pgadmin or db in this case). 
- When it comes to the port data, I get port information is: [port to access in local machine]:[port inside the container]
- Containers inside a (the same?) Docker network will connect to their ports inside the container.

All that accounted pgadmin should use the db (service name) : 5432 (default postgres port).


Question 3. Preparing the data.
- I downloaded the data locally, will try the script now. 
- Before I want to make sure I understand what I am doing. 

