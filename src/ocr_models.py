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