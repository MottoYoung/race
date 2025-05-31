# 保留原有AIPPT类核心逻辑，修改为更简洁的封装
import time
import json
import requests
from .xfPPT_demo import AIPPT  # 用户提供的原始代码



class PPTGenerator:
    def __init__(self, app_id, api_secret, template_id):
        self.app_id = app_id
        self.api_secret = api_secret
        self.template_id = template_id  # 存储模板ID
    def createPptByOutline(self, outline, query=""):
        # 确保query有默认值
        generator = AIPPT(
            self.app_id,
            self.api_secret,
            Text=query or "基于文档生成PPT",  # 添加默认值
            templateId=self.template_id
        )
        task_id = generator.createPptByOutline(outline)
        return task_id

    def create_task(self, description):
        generator = AIPPT(
            app_id=self.app_id,
            api_secret=self.api_secret,
            Text=description,
            templateId=self.template_id  # 传递模板ID
        )
        task_id = generator.create_task()
        return task_id

    def get_progress(self, task_id):
        try:
            # 每次请求都重新生成有效的header
            generator = AIPPT(self.app_id, self.api_secret, "", self.template_id)
            
            response = requests.get(
                f"https://zwapi.xfyun.cn/api/ppt/v2/progress?sid={task_id}",
                headers=generator.getHeaders()  # 改用动态生成的header
            )
            
            # 添加响应状态码检查
            if response.status_code != 200:
                return {"code": 500, "error": "服务不可用"}
                
            data = response.json()
            
            # 规范化响应格式
            return {
                "code": 0,
                "data": data.get('data', {})
            }
            
        except Exception as e:
            return {"code": 500, "error": str(e)}