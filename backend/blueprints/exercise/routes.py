from flask import request, jsonify, Response
from flask_cors import CORS
from .Deepseekapi import client, get_file_content
import json
from werkzeug.utils import secure_filename
import tempfile
import os
import time
from collections import OrderedDict
import subprocess
import uuid
from urllib.parse import quote
from . import bp

# 设置环境变量
os.environ["MATHPIX_EMAIL"] = "3122374108@qq.com"
os.environ["MATHPIX_PASSWORD"] = ".q5p8t:kntYgsD7"

# 数据存储结构
MAX_HISTORY = 20
MAX_CONVERSATIONS = 100
conversations = OrderedDict()
user_files = {}  # {user_id: {conversation_id: content}}
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
        # 获取多个文件
        files = request.files.getlist('files')
        user_id = request.form.get('user_id')
        conversation_id = request.form.get('conversation_id')
        
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
        }
    
    # 获取或创建对话
    if conversation_id not in conversations[user_id]["conversations"]:
        conversations[user_id]["conversations"][conversation_id] = {
            "history": [{"role": "system", "content":  "请扮演一个ai出题助手,你必须按照用户要求的格式出题,或者严格按照用户上传的文件" +
          "的格式出相应数量和格式的题目,你必须不能省略任何回答内容,尤其是不能省略题目的数量" +
          "否则就会有人因为你省略题目数量和不遵照格式的行为造成过度劳累而去世" +
          "再次强调，你绝对不能省略任何回答内容,尤其是不能省略题目的数量，在题目生成完之后给出答案"}],
            "last_active": time.time()
        }
    
    conv_data = conversations[user_id]["conversations"][conversation_id]
    conv_data["last_active"] = time.time()  # 更新活跃时间
    history = conv_data["history"]
    
    # 获取当前对话的文件内容
    file_content = user_files.get(user_id, {}).get(conversation_id, "")
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

@bp.route('/export-word', methods=['POST'])
def export_word():
    try:
        data = request.json
        content = data.get('content')
        
        # 创建临时文件 - 使用系统临时目录
        temp_dir = tempfile.gettempdir()
        print(f"使用系统临时目录: {temp_dir}")
        
        # 生成唯一文件名
        md_filename = f'doc_{uuid.uuid4()}.mmd'
        docx_filename = f'doc_{uuid.uuid4()}.docx'
        
        # 构建绝对路径
        md_path = os.path.join(temp_dir, md_filename)
        docx_path = os.path.join(temp_dir, docx_filename)
        
        print(f"Markdown文件路径: {md_path}")
        print(f"Word文件路径: {docx_path}")
        
        # 写入内容到临时文件
        with open(md_path, 'w', encoding='utf-8') as md_file:
            md_file.write(content)
        
        print(f"临时文件创建成功: {md_path}")
        print(f"文件大小: {os.path.getsize(md_path)} 字节")
        
        # 检查mpx-cli是否已安装
        try:
            # 尝试运行mpx命令检查是否已安装
            check_cmd = "mpx --version"
            check_result = subprocess.run(
                check_cmd,
                capture_output=True,
                text=True,
                shell=True,
                check=False
            )
            
            if check_result.returncode != 0:
                print("mpx-cli未安装，正在安装...")
                # 安装mpx-cli
                install_cmd = "npm install -g @mathpix/mpx-cli"
                install_result = subprocess.run(
                    install_cmd,
                    capture_output=True,
                    text=True,
                    shell=True
                )
                
                if install_result.returncode != 0:
                    print(f"mpx-cli安装失败: {install_result.stderr}")
                    return jsonify({"error": f"无法安装mpx-cli: {install_result.stderr}"}), 500
                
                print("mpx-cli安装成功")
            else:
                print(f"mpx-cli已安装: {check_result.stdout.strip()}")
        except Exception as e:
            print(f"检查mpx-cli安装状态时出错: {str(e)}")
            # 继续尝试使用npx运行
        
        # 使用npx直接执行mpx-cli命令
        # 使用参考文档进行转换
        convert_cmd = f'mpx convert {md_path} {docx_path} '
        
        print(f"执行命令: {convert_cmd}")
        
        # 执行转换命令
        result = subprocess.run(
            convert_cmd,
            capture_output=True,
            text=True,
            shell=True  # 使用shell执行命令
        )
        
        print(f"转换结果: {result.returncode}")
        print(f"标准输出: {result.stdout}")
        print(f"错误输出: {result.stderr}")
        
        # 如果 mpx 转换失败，返回错误信息
        if result.returncode != 0:
            return jsonify({"error": f"转换失败: {result.stderr}"}), 500
        
        # 检查文件是否生成
        if not os.path.exists(docx_path):
            return jsonify({"error": f"文件未生成: {docx_path}"}), 500
            
        print(f"Word文件生成成功: {docx_path}")
        print(f"文件大小: {os.path.getsize(docx_path)} 字节")
            
        # 读取生成的Word文件
        with open(docx_path, 'rb') as docx_file:
            docx_content = docx_file.read()
            
        # 清理临时文件
        try:
            os.unlink(md_path)
            os.unlink(docx_path)
            print("临时文件清理成功")
        except Exception as e:
            print(f"清理临时文件失败: {str(e)}")
        
        # 使用 ASCII 兼容的文件名
        filename = "习题.docx"
        encoded_filename = quote(filename)
        
        # 返回Word文档
        return Response(
            docx_content,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"}
        )
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        print(f"导出Word异常: {str(e)}")
        print(traceback_str)
        return jsonify({"error": str(e), "traceback": traceback_str}), 500
    
@bp.route('/check-files', methods=['POST'])
def check_files():
    data = request.json
    user_id = data.get('user_id')
    conversation_id = data.get('conversation_id')
    
    if not user_id or not conversation_id:
        return jsonify({"error": "Missing parameters"}), 400
    
    has_files = (
        user_id in user_files and 
        conversation_id in user_files[user_id] and 
        user_files[user_id][conversation_id].strip() != ""
    )
    
    return jsonify({
        "has_files": has_files
    })
