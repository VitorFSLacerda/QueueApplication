FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    openssh-server \
    && pip3 install twisted==22.10.0

RUN mkdir /var/run/sshd

RUN echo 'root:rootpassword' | chpasswd

RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

WORKDIR /app

COPY . .

EXPOSE 22

CMD service ssh start && python3 callCenterClient.py
