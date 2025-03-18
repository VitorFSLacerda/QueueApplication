FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && pip3 install twisted==22.10.0

WORKDIR /app

COPY . .

EXPOSE 5678

CMD ["python3", "callCenterServer.py"]