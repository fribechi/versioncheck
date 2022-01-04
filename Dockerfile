#FROM ubuntu:20.04
FROM icr.io/continuous-delivery/pipeline/pipeline-base-image:2.12

RUN apt update && apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt install -y python3 python3-pip

RUN apt install -y git
RUN apt-get install -y curl
RUN apt-get -y install jq

RUN pip3 install GitPython

RUN mkdir -p /versioncheck
ADD versioncheck /versioncheck
ENV PYTHONPATH=/

