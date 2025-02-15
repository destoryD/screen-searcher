from openai import OpenAI
import base64
from config import config
class OCR_MODEL:
    def __init__(self, name, model):
        self.name = name
        self.model = model
    
    def recognize(self,image):
        pass
    
    def process_image(self,image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
        
class Qwen_MODEL(OCR_MODEL):
    def __init__(self,api_key=""):
        super().__init__("通义百炼OCR", "qwen-vl-ocr")
        self.api_key = api_key
    def recognize(self, image_path=None):
        if image_path is None:
            image_path = config.get("screenshot_filename")
        image = self.process_image(image_path)
        client = OpenAI(
            api_key=self.api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        completion = client.chat.completions.create(
            model="qwen-vl-ocr",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image}"},
                            "min_pixels": 28 * 28 * 4,
                            "max_pixels": 28 * 28 * 1280
                        },
                        # 为保证识别效果，目前模型内部会统一使用"Read all the text in the image."进行识别，用户输入的文本不会生效。
                        {"type": "text", "text": "Read all the text in the image."},
                    ]
                }
            ])
        return completion.choices[0].message.content
class PaddleOCR_MODEL(OCR_MODEL):
    def __init__(self,ocr_version="PP-OCRv4"):
        super().__init__("PaddleOCR", "paddleocr")
        from paddleocr import PaddleOCR
        print(ocr_version)
        self.ocr_model = PaddleOCR(use_gpu=False,ocr_version=ocr_version)
    def recognize(self, image_path=None):
        if image_path is None:
            image_path = config.get("screenshot_filename")
        result = self.ocr_model.ocr(image_path,det=True)
        res = self.resolve_context(result)
        return res
    
    def resolve_context(self,result):
        res = ""
        for lines in result:
            for item in lines:
                res += item[-1][0]
                res +='\n'
        return res

class Sili_MODEL(OCR_MODEL):
    def __init__(self,api_key="",model="Pro/Qwen/Qwen2-VL-7B-Instruct"):
        super().__init__("硅基流动", "sili-ocr")
        self.api_key = api_key
        self.model = model
    def recognize(self, image_path=None):
        if image_path is None:
            image_path = config.get("screenshot_filename")
        image = self.process_image(image_path)
        client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.siliconflow.cn/v1",
        )
        completion = client.chat.completions.create(
            model=self.model,
            max_tokens=1024,
            temperature=0.7,
            top_p=0.7,
            frequency_penalty=0.0,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image}"},
                        },
                        {"type": "text", "text": "Read all the text in the image with no other outputs."},
                    ]
                }
            ])
        return completion.choices[0].message.content

class Zhipu_MODEL(OCR_MODEL):
    def __init__(self,api_key="",model="GLM-4V-Flash"):
        super().__init__("智谱AI", "zhipu-ocr")
        self.api_key = api_key
        self.model = model
    def recognize(self, image_path=None):
        if image_path is None:
            image_path = config.get("screenshot_filename")
        image = self.process_image(image_path)
        client = OpenAI(
            api_key=self.api_key,
            base_url="https://open.bigmodel.cn/api/paas/v4/",
        )
        completion = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image}"},
                        },
                        {"type": "text", "text": "Read all the text in the image with no other outputs."},
                    ]
                }
            ])
        return completion.choices[0].message.content