FROM python:3.10.4-bullseye

COPY src /opt/kubernetes-integration

# cd to kubernetes-integration src dir for pip install
WORKDIR /opt/kubernetes-integration/

# pip install kubernetes integration
RUN pip install -e .

