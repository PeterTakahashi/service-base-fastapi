FROM ubuntu:24.04

RUN mkdir /myapp
WORKDIR /myapp

RUN apt update --yes \
    && apt install -y curl g++ wget ffmpeg libsm6 libxext6 gimp libvulkan1 cargo libpq-dev

RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/root/.local/bin" sh
ENV PATH="/root/.local/bin:$PATH"

COPY requirements.txt /myapp/requirements.txt
COPY requirements-dev.txt /myapp/requirements-dev.txt

RUN uv python install 3.10.16

RUN uv venv --python 3.10.16 \
    && uv pip install -r requirements.txt \
    && uv pip install -r requirements-dev.txt

COPY . /myapp

EXPOSE 8000