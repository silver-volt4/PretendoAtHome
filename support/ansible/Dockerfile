FROM docker.io/alpine:latest
RUN apk add ansible
RUN apk add openssh

# MongoDB support
RUN ansible-galaxy collection install community.mongodb
RUN apk add py3-mongo

ENTRYPOINT [ "ansible" ]