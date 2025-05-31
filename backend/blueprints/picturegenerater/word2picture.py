# encoding: UTF-8
import requests
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import json
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time

class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg

class Url:
    def __init__(self, host, path, schema):
        self.host = host
        self.path = path
        self.schema = schema

def sha256base64(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return base64.b64encode(sha256.digest()).decode('utf-8')

def parse_url(request_url):
    stidx = request_url.index("://")
    host = request_url[stidx + 3:]
    schema = request_url[:stidx + 3]
    edidx = host.index("/")
    if edidx <= 0:
        raise AssembleHeaderException("Invalid URL")
    path = host[edidx:]
    host = host[:edidx]
    return Url(host, path, schema)

def assemble_ws_auth_url(request_url, method, api_key, api_secret):
    u = parse_url(request_url)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    signature_origin = f"host: {host}\ndate: {date}\n{method} {path} HTTP/1.1"
    signature_sha = hmac.new(api_secret.encode('utf-8'), 
                            signature_origin.encode('utf-8'), 
                            digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(signature_sha).decode('utf-8')
    authorization_origin = f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')
    return f"{request_url}?{urlencode({'host': host, 'date': date, 'authorization': authorization})}"

def get_body(appid, text, width, height):
    return {
        "header": {"app_id": appid},
        "parameter": {"chat": {"domain": "general", "width": width, "height": height}},
        "payload": {"message": {"text": [{"role": "user", "content": text}]}}
    }

def generate_image(text, appid, apikey, apisecret, width=512, height=512):
    host = 'https://spark-api.cn-huabei-1.xf-yun.com/v2.1/tti'
    url = assemble_ws_auth_url(host, 'POST', apikey, apisecret)
    body = get_body(appid, text, width, height)
    response = requests.post(url, json=body, headers={'Content-Type': 'application/json'})
    return parse_response(response.text)

def parse_response(response_text):
    data = json.loads(response_text)
    if data['header']['code'] != 0:
        raise Exception(f"API Error {data['header']['code']}: {data['header']['message']}")
    return data['payload']['choices']['text'][0]['content']