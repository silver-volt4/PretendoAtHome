FROM docker.io/alpine:latest
RUN apk add ansible
RUN apk add openssh

RUN ansible-galaxy collection install community.mongodb
RUN apk add py3-mongo

RUN ansible-galaxy collection install community.postgresql
RUN apk add py3-psycopg2

RUN ansible-galaxy collection install dubzland.minio
RUN apk add minio-client

ENTRYPOINT [ "ansible" ]