FROM ubuntu:latest
LABEL authors="pavel.potseluyev"

ENTRYPOINT ["top", "-b"]