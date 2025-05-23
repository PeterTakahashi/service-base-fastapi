FROM ubuntu:24.04

RUN mkdir /myapp
WORKDIR /myapp

RUN apt update --yes \
    && apt install -y curl g++ cargo libpq-dev git

RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/root/.local/bin" sh
ENV PATH="/root/.local/bin:$PATH"

COPY . /myapp

RUN uv python install 3.11.11

RUN uv venv --python 3.11.11 \
    && uv pip install . \
    && uv pip install --group dev

EXPOSE 8000

SHELL ["/bin/bash", "-c"]
CMD source .venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000
