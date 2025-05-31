from flask import request, jsonify, Response
from flask_cors import CORS
from .Deepseekapi import client, get_file_content
import json
from werkzeug.utils import secure_filename
import tempfile
import os
import time
from collections import OrderedDict
from . import bp

# 数据存储结构
MAX_HISTORY = 20
MAX_CONVERSATIONS = 100
conversations = OrderedDict()
user_files = OrderedDict()
active_streams = {}

def get_user_conversation(user_id, conversation_id):
    """获取指定用户的对话历史"""
    if user_id not in conversations:
        return None
    return conversations[user_id]["conversations"].get(conversation_id)

def cleanup_conversations():
    """定期清理超过1小时未活动的会话"""
    current_time = time.time()
    for user_id in list(conversations.keys()):
        user_data = conversations[user_id]
        # 清理用户下的对话
        expired_conv = [
            cid for cid, conv in user_data["conversations"].items()
            if current_time - conv["last_active"] > 3600
        ]
        for cid in expired_conv:
            user_data["conversations"].pop(cid, None)
    
        # 如果用户没有对话则移除用户
        if not user_data["conversations"]:
            conversations.pop(user_id, None)
            user_files.pop(user_id, None)

@bp.route('/upload', methods=['POST'])
def upload_file():
    try:
        files = request.files.getlist('files')
        user_id = request.form.get('user_id')
        conversation_id = request.form.get('conversation_id')  # 新增对话ID
        if not files or not user_id or not conversation_id:
                return jsonify({"status": "error", "message": "缺少必要参数"}), 400
        
        # 初始化用户和对话的文件存储结构
        if user_id not in user_files:
            user_files[user_id] = {}
        
        if conversation_id not in user_files[user_id]:
            user_files[user_id][conversation_id] = ""
        
        all_content = []
        
        for uploaded_file in files:
            with tempfile.NamedTemporaryFile(suffix=os.path.splitext(uploaded_file.filename)[1].lower(), delete=False) as temp_file:
                uploaded_file.save(temp_file.name)
                file_content = get_file_content(temp_file.name)
                all_content.append(file_content)
        
        # 合并所有文件内容并存储
        combined_content = "\n\n".join(all_content)
        user_files[user_id][conversation_id] = combined_content
        
        return jsonify({
            "status": "success",
            "message": f"成功上传 {len(files)} 个文件",
            "content_preview": combined_content[:200] + "..." if len(combined_content) > 200 else combined_content
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@bp.route('/abort', methods=['POST'])
def abort_stream():
    data = request.json
    user_id = data.get('user_id')
    conversation_id = data.get('conversation_id')
    stream_id = f"{user_id}_{conversation_id}"
    
    if stream_id in active_streams:
        active_streams[stream_id] = False
        return jsonify({"status": "success"})
    return jsonify({"status": "stream not found"}), 404

@bp.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get('user_id')
    conversation_id = data.get('conversation_id')
    message = data.get('message')
    
    # 参数校验
    if not all([user_id, conversation_id, message]):
        return jsonify({"error": "Missing parameters"}), 400

    # 初始化数据结构
    if user_id not in conversations:
        conversations[user_id] = {
            "conversations": OrderedDict(),
            "files": ""
        }
    
    # 获取或创建对话
    if conversation_id not in conversations[user_id]["conversations"]:
        conversations[user_id]["conversations"][conversation_id] = {
            "history": [{"role": "system", "content":    "请扮演一个特别擅长编写教学设计的资深教师" +
          "你编写的教学设计必须包括教学内容,教学活动安排,时间分配,预期成果" +
          "其他内容你可以自行斟酌但是一定要保证至少3个互动环节" +
          "互动环节必须有趣，不能只是简单的回答问题或者复习" +
          "你必须严格遵守以上要求,否则会造成及其严重的后果",}],
            "last_active": time.time()
        }
    
    conv_data = conversations[user_id]["conversations"][conversation_id]
    conv_data["last_active"] = time.time()  # 更新活跃时间
    history = conv_data["history"]
    
    file_content = user_files.get(user_id, {}).get(conversation_id, "")
    
    # 优化：如果文件内容很大，可以考虑截断或摘要
    if file_content and len(file_content) > 10000:  # 如果文件内容超过10K字符
        file_content = file_content[:10000] + "\n\n[文件内容过长，已截断]"
    
    full_content = f"{message}\n\n{file_content}".strip() if file_content else message
    
    # 添加用户消息（保留最近MAX_HISTORY条）
    history.append({"role": "user", "content": full_content})
    if len(history) > MAX_HISTORY:
        history[:] = history[-MAX_HISTORY:]

    def generate():
        full_response = ""
        stream_id = f"{user_id}_{conversation_id}"
        active_streams[stream_id] = True  # 标记当前会话有活跃流
        try:
            stream = client.chat.completions.create(
                model="deepseek-r1",
                messages=history[-MAX_HISTORY:], # 传入最近的对话历史
                stream=True
            )
            # 这里替换为实际的AI流式调用
            for chunk in stream:
                if not active_streams.get(stream_id, False):
                    break
                if chunk.choices:
                    delta = chunk.choices[0].delta
                    reasoning_content = getattr(delta, 'reasoning_content', '')
                    content = getattr(delta, 'content', '')
                    if reasoning_content:
                        yield f"data: {json.dumps({'reasoning_content': reasoning_content})}\n\n".encode('utf-8')
                    if content:
                        full_response += content
                        yield f"data: {json.dumps({'content': content})}\n\n".encode('utf-8')
            
            # 添加助手回复到历史
            history.append({"role": "assistant", "content": full_response})
            active_streams.pop(stream_id, None)
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n".encode('utf-8')
        finally:
            active_streams.pop(stream_id, None)

    # 添加必要的响应头，禁止缓冲
    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache, no-transform',
        'X-Accel-Buffering': 'no',  # 针对Nginx代理的设置
        'Connection': 'keep-alive'
    }
    
    return Response(generate(), 
                  mimetype='text/event-stream',
                  headers=headers,
                  direct_passthrough=True)  # 启用直接传递，避免WSGI缓冲
