# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import base64
import time

import requests

url = "http://localhost:9003/ocr"
img_path = "tests/test_files/ch_en_num.jpg"

# 方式一：使用base64编码传
stime = time.perf_counter()
with open(img_path, "rb") as fa:
    img_str = base64.b64encode(fa.read())

payload = {"image_data": img_str}
response = requests.post(url, data=payload, timeout=180)

print(response.json())
elapse = time.perf_counter() - stime
print(f"用时:{elapse:.3f}秒")

print("-" * 40)

# 方式二：使用文件上传方式
stime = time.perf_counter()
with open(img_path, "rb") as f:
    file_dict = {"image_file": (img_path, f, "image/png")}
    response = requests.post(url, files=file_dict, timeout=180)
    print(response.json())

elapse = time.perf_counter() - stime
print(f"用时:{elapse:.3f}秒")
print("-" * 40)

# 方式三：控制是否使用检测、方向分类和识别这三部分的模型； 不使用检测模型:use_det=False
stime = time.perf_counter()
img_path = "tests/test_files/ch_en_num.jpg"

with open(img_path, "rb") as f:
    file_dict = {"image_file": (img_path, f, "image/png")}
    # 添加控制参数
    data = {"use_det": False, "use_cls": True, "use_rec": True}
    response = requests.post(url, files=file_dict, data=data, timeout=180)
    print(response.json())

elapse = time.perf_counter() - stime
print(f"用时:{elapse:.3f}秒")
print("-" * 40)
