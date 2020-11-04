# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.145.1/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version: 3, 3.9, 3.8, 3.7, 3.6
ARG VARIANT="3.7"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# Install pip requirements
COPY requirements/* /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/testing.txt \
   && rm -rf /tmp/pip-tmp
