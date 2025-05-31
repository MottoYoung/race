# sparkAPI.py
# coding: utf-8
import base64
import datetime
import hashlib
import hmac
import json
import ssl
from urllib.parse import urlparse, urlencode
from time import mktime
from wsgiref.handlers import format_date_time
import websocket

class Ws_Param:
    def __init__(self, APPID, APIKey, APISecret, gpt_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        parsed_url = urlparse(gpt_url)
        self.host = parsed_url.netloc
        self.path = parsed_url.path
        self.gpt_url = gpt_url

    def create_url(self):
        # 1.2.1 生成RFC1123格式的date
        now = datetime.datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        
        # 1.2.2 生成authorization
        # 步骤2：构造签名串
        signature_str = f"host: {self.host}\ndate: {date}\nGET {self.path} HTTP/1.1"
        
        # 步骤3：进行hmac-sha256加密
        signature_sha = hmac.new(
            self.APISecret.encode('utf-8'),
            signature_str.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        
        # 步骤4：base64编码得到signature
        signature = base64.b64encode(signature_sha).decode(encoding='utf-8')
        
        # 步骤5：拼接authorization_origin
        authorization_origin = (
            f'api_key="{self.APIKey}", algorithm="hmac-sha256", '
            f'headers="host date request-line", signature="{signature}"'
        )
        
        # 步骤6：base64编码得到最终authorization
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode()
        
        # 1.2.3 生成最终URL
        query_params = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        encoded_params = urlencode(query_params, safe='/=')
        return f"{self.gpt_url}?{encoded_params}"

def on_error(ws, error):
    print(f"WebSocket Error: {error}")

def on_close(ws, close_status, close_msg):
    print("### Connection Closed ###")

def on_open(ws):
    try:
        # 严格遵循接口要求的请求格式
        request_body = {
            "header": {
                "app_id": ws.appid,
                "uid": "1234"
            },
            "parameter": {
                "chat": {
                    "domain": ws.domain,
                    "temperature": 0.5,
                    "max_tokens": 4096,
                    "auditing": "default"  # 必需字段
                }
            },
            "payload": {
                "message": {
                    "text": [  # 必须为数组格式
                        {"role": "user", "content": ws.query}
                    ]
                }
            }
        }
        ws.send(json.dumps(request_body, ensure_ascii=False))
    except Exception as e:
        print(f"Open Error: {str(e)}")
        ws.close()

def on_message(ws, message):
    try:
        data = json.loads(message)
        print(f"Received data: {data}")  # 添加日志信息
        
        if data["header"]["code"] != 0:
            print(f"API Error [{data['header']['code']}]: {data['header']['message']}")
            ws.close()
            return
        
        choices = data["payload"]["choices"]
        content = choices["text"][0]["content"]
        ws.code_result.append(content)
        
        if choices["status"] == 2:
            ws.close()
    except Exception as e:
        print(f"Message Handling Error: {str(e)}")
        ws.close()

def generate_code(prompt, appid, api_key, api_secret):
    """严格遵循星火API文档的代码生成函数"""
    # 验证接口版本对应关系
    ws_param = Ws_Param(
        appid, 
        api_key,
        api_secret,
        "wss://spark-api.xf-yun.com/v4.0/chat"  # Max版本
    )
    
    # 构造系统提示（保持与API要求一致）
    system_prompt = """你是一个Python数据分析专家，专门生成数学函数绘图代码。要求：
1. 根据用户需求自动选择二维或三维绘图
2. 仅当用户明确要求三维时，才导入Axes3D并使用projection='3d'
3. 二维绘图使用标准plt.plot或plt.scatter
4. 必须包含完整绘图代码结构：
   - 数据生成（使用numpy）
   - 图形初始化（fig = plt.figure()）
   - 样式设置（sns.set()）
   - 坐标轴标签和标题
5. 禁止包含plt.show()或文件保存语句
用户需求："""
    
    ws = websocket.WebSocketApp(
        ws_param.create_url(),
        header={
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    
    # 设置必要属性
    ws.appid = appid
    ws.query = system_prompt + prompt
    ws.domain = "4.0Ultra"  # 必须与URL版本对应
    ws.code_result = []
    
    # 运行连接
    ws.run_forever(
        sslopt={
            "cert_reqs": ssl.CERT_NONE,
            "check_hostname": False  # 避免主机名验证问题
        }
    )
    
    return "".join(ws.code_result)