FROM public.ecr.aws/docker/library/python:3.13-slim-bookworm@sha256:01f42367a0a94ad4bc17111776fd66e3500c1d87c15bbd6055b7371d39c124fb

WORKDIR /task

# Install pinned dependencies
RUN pip install --no-cache-dir pytest==8.3.2 flask==3.1.0 requests==2.32.3

# Explicit COPY — no bulk COPY
COPY solution/ /task/solution/
COPY instruction.md /task/instruction.md
COPY task.toml /task/task.toml
COPY environment/ /task/environment/
COPY tests/cases.json /task/tests/cases.json
COPY tests/output.json /task/tests/output.json
