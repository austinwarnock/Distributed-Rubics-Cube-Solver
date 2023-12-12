FROM ubuntu:rolling

LABEL MAINTAINER=dev@austinwarnock.tech

RUN apt-get update && apt-get upgrade -y && apt-get install -y python3-pip ipython3

RUN apt-get install -y vim nmap iputils-ping ssh htop slurm net-tools

ENV GRPC_PYTHON_VERSION 1.15.0

RUN apt-get install -y libprotoc-dev protobuf-compiler

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages
COPY . /usr/src/app

# Create the protobuf files
# RUN protoc --python_out=. sudoku.proto # Code below works similarly
RUN python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. rubiks.proto
EXPOSE 22
EXPOSE 80
EXPOSE 50050-50100

# Unbuffer to see logs with docker logs <containername>
ENV PYTHONUNBUFFERED=1

# Run the node
CMD ["python3", "cube.py"]