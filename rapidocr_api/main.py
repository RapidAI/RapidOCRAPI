# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
import base64
import io
import os
import sys
from pathlib import Path
from typing import Dict, Optional

import numpy as np
import uvicorn
from fastapi import FastAPI, Form, UploadFile
from PIL import Image
from rapidocr import RapidOCR

sys.path.append(str(Path(__file__).resolve().parent.parent))


class OCRAPIUtils:
    def __init__(self) -> None:
        det_model_path = os.getenv("det_model_path", None)
        cls_model_path = os.getenv("cls_model_path", None)
        rec_model_path = os.getenv("rec_model_path", None)

        if det_model_path is None or cls_model_path is None or rec_model_path is None:
            self.ocr = RapidOCR()
        else:
            self.ocr = RapidOCR(
                params={
                    "Det.model_path": det_model_path,
                    "Cls.model_path": cls_model_path,
                    "Rec.model_path": rec_model_path,
                }
            )

    def __call__(
        self, ori_img: Image.Image, use_det=None, use_cls=None, use_rec=None, **kwargs
    ) -> Dict:
        img = np.array(ori_img)
        ocr_res = self.ocr(
            img, use_det=use_det, use_cls=use_cls, use_rec=use_rec, **kwargs
        )

        if ocr_res.boxes is None or ocr_res.txts is None or ocr_res.scores is None:
            return {}

        out_dict = {}
        for i, (boxes, txt, score) in enumerate(
            zip(ocr_res.boxes, ocr_res.txts, ocr_res.scores)
        ):
            out_dict[i] = {"rec_txt": txt, "dt_boxes": boxes.tolist(), "score": score}
        return out_dict


app = FastAPI()
processor = OCRAPIUtils()


@app.get("/")
def root():
    return {"message": "Welcome to RapidOCR API Server!"}


@app.post("/ocr")
def ocr(
    image_file: Optional[UploadFile] = None,
    image_data: str = Form(None),
    use_det: bool = Form(None),
    use_cls: bool = Form(None),
    use_rec: bool = Form(None),
):
    if image_file:
        img = Image.open(image_file.file)
    elif image_data:
        img_bytes = str.encode(image_data)
        img_b64decode = base64.b64decode(img_bytes)
        img = Image.open(io.BytesIO(img_b64decode))
    else:
        raise ValueError(
            "When sending a post request, data or files must have a value."
        )
    ocr_res = processor(img, use_det=use_det, use_cls=use_cls, use_rec=use_rec)

    return ocr_res


def main():
    parser = argparse.ArgumentParser("rapidocr_api")
    parser.add_argument("-ip", "--ip", type=str, default="0.0.0.0", help="IP Address")
    parser.add_argument("-p", "--port", type=int, default=9003, help="IP port")
    parser.add_argument(
        "-workers", "--workers", type=int, default=1, help="number of worker process"
    )
    args = parser.parse_args()

    # 修改 uvicorn 的默认日志配置
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s %(levelname)s %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s %(levelname)s %(message)s"

    uvicorn.run(
        "rapidocr_api.main:app",
        host=args.ip,
        port=args.port,
        reload=False,
        workers=args.workers,
        log_config=log_config,
    )


if __name__ == "__main__":
    main()
