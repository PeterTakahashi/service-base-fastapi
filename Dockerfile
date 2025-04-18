FROM python:3.10.16

RUN mkdir /myapp
WORKDIR /myapp

RUN apt update --yes \
    && apt install g++ wget ffmpeg libsm6 libxext6 gimp libvulkan1 --yes

# Gemfileの追加とインストール
COPY requirements.txt /myapp/requirements.txt
COPY requirements-dev.txt /myapp/requirements-dev.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

# アプリケーションの追加
COPY . /myapp

EXPOSE 8000
