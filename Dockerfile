FROM python:3.10.11-slim-buster
# FROM python:3.10.11-slim-bookworm
# FROM python:3.11-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# 设置工作目录
WORKDIR /app

# 安装vim，如果不需要临时修改容器文件，此步骤可以删
# RUN apt-get update && \
#    apt-get install -y --no-install-recommends vi && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    pip install --no-cache-dir rapidocr_api pillow rapidocr-onnxruntime==1.3.25 -i https://mirrors.aliyun.com/pypi/simple && \
    pip uninstall -y opencv-python && \
    pip install --no-cache-dir opencv-python-headless -i https://mirrors.aliyun.com/pypi/simple

COPY start_api.sh /app
RUN chmod +x /app/start_api.sh

EXPOSE 9003

ENV WORKERS=2

CMD ["bash", "start_api.sh"]
