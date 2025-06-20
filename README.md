<div align="center">
  <div align="center">
    <img src="https://github.com/RapidAI/RapidOCRAPI/releases/download/v0.1.5/LOGO.png"/>
  </div>
 <br/>
  <a href=""><img src="https://img.shields.io/badge/Python->=3.6-aff.svg"></a>
  <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
  <a href="https://github.com/RapidAI/RapidOCRAPI/graphs/contributors"><img src="https://img.shields.io/github/contributors/RapidAI/RapidOCRAPI?color=9ea"></a>
  <a href="https://github.com/RapidAI/RapidOCRAPI/stargazers"><img src="https://img.shields.io/github/stars/RapidAI/RapidOCRAPI?color=ccf" ></a>
  <a href="https://pepy.tech/project/rapidocr_api"><img src="https://static.pepy.tech/badge/rapidocr_api?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
  <a href="https://pypi.org/project/rapidocr_api/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapidocr_api"></a>
  <a href="https://choosealicense.com/licenses/apache-2.0/"><img src="https://img.shields.io/badge/License-Apache%202-dfd.svg"></a>
  <a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

</div>

### 简介

- 该包是将[rapidocr](./rapidocr/install.md)库做了API封装，采用[FastAPI](https://fastapi.tiangolo.com/) + [uvicorn](https://www.uvicorn.org/)实现。
- 定位是一个快速调用`rapidocr`的API接口，没有考虑多进程处理并发请求，如果有这需求的小伙伴，可以看看[gunicorn](https://gunicorn.org/)等。

### 安装

```bash linenums="1"
pip install rapidocr_api
```

### 使用

#### 启动服务

```bash
# 默认参数启动
rapidocr_api

# 指定参数：端口与进程数量；
rapidocr_api -ip 0.0.0.0 -p 9005 -workers 2
```

#### 调用服务

```bash
curl -F image_file=@1.png http://0.0.0.0:9003/ocr
```

Python脚本使用：

```python
import requests

url = 'http://localhost:9003/ocr'
img_path = 'tests/test_files/ch_en_num.jpg'

with open(img_path, 'rb') as f:
    file_dict = {'image_file': (img_path, f, 'image/png')}
    response = requests.post(url, files=file_dict, timeout=60)

print(response.json())
```

### 文档

完整文档请移步：[docs](https://rapidai.github.io/RapidOCRDocs/main/install_usage/rapidocr_api/usage/)
