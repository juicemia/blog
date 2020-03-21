FROM ubuntu:18.04

RUN apt-get update && apt-get install -y git tree curl
RUN curl -L -o /bin/caddy https://github.com/caddyserver/caddy/releases/download/v2.0.0-beta.13/caddy2_beta13_linux_amd64 && chmod 744 /bin/caddy

VOLUME "/work"
