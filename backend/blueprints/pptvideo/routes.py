import os
import uuid
import json
from flask import request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
import threading
from .test2 import convert_ppt_to_video
from .config import PPTvConfig
from . import bp

# 存储转换任务的状态
conversion_tasks = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['ppt', 'pptx']

def process_conversion(task_id, ppt_path, output_path, params):
    """在后台线程中处理PPT转换任务"""
    try:
        conversion_tasks[task_id]['status'] = 'processing'
        
        # 检查输出文件名是否以连字符开头
        output_filename = os.path.basename(output_path)
        output_dir = os.path.dirname(output_path)
        
        # 如果文件名以连字符开头，使用不带连字符的安全文件名
        safe_output_path = output_path
        if output_filename.startswith('-'):
            print(f"警告: 文件名 '{output_filename}' 以连字符开头，这可能导致FFMPEG问题")
            safe_filename = f"safe_{output_filename}"
            safe_output_path = os.path.join(output_dir, safe_filename)
            print(f"使用安全文件名: {safe_filename}")
        
        # 调用转换函数
        convert_ppt_to_video(
            ppt_path=ppt_path,
            output_path=safe_output_path,
            slide_duration=int(params.get('slide_duration', 5)),
            lang=params.get('lang', 'zh-cn'),
            use_generated_script=params.get('use_generated_script', False),
            script_style=params.get('script_style', '标准'),
            target_audience=params.get('target_audience', '通用'),
            total_duration=params.get('total_duration', '中等'),
            subject=params.get('subject', '通用'),
            speed=int(params.get('speed', 50)),
            vcn=params.get('vcn', 'x4_mingge'),
            volume=int(params.get('volume', 50)),
            pitch=int(params.get('pitch', 50))
        )
        
        # 如果使用了安全文件名，重命名回原来的文件名
        if safe_output_path != output_path:
            if os.path.exists(output_path):
                os.remove(output_path)
            os.rename(safe_output_path, output_path)
        
        # 更新任务状态为完成
        conversion_tasks[task_id]['status'] = 'completed'
        # 使用直接访问静态资源的URL，这样更容易在前端播放
        filename = os.path.basename(output_path)
        conversion_tasks[task_id]['video_url'] = f'/api/pptvideo/static/outputs/{task_id}/{filename}'
    except Exception as e:
        # 转换失败
        conversion_tasks[task_id]['status'] = 'failed'
        conversion_tasks[task_id]['error'] = str(e)
        print(f"转换任务失败: {e}")

@bp.route('/upload', methods=['POST'])
def upload_file():
    """接收上传的PPT文件"""
    if 'file' not in request.files:
        return jsonify({'error': '没有文件上传'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if file and allowed_file(file.filename):
        # 生成唯一任务ID
        task_id = str(uuid.uuid4())
        
        # 安全地获取文件名并保存
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(PPTvConfig.UPLOAD_FOLDER, task_id)
        os.makedirs(upload_folder, exist_ok=True)
        
        ppt_path = os.path.join(upload_folder, filename)
        file.save(ppt_path)
        
        # 创建任务记录
        conversion_tasks[task_id] = {
            'status': 'pending',
            'filename': filename,
            'ppt_path': ppt_path
        }
        
        return jsonify({
            'task_id': task_id,
            'status': 'pending',
            'message': '文件上传成功'
        })
    
    return jsonify({'error': '不支持的文件类型'}), 400

@bp.route('/convert/<task_id>', methods=['POST'])
def convert_ppt(task_id):
    """开始转换任务"""
    if task_id not in conversion_tasks:
        return jsonify({'error': '找不到任务'}), 404
    
    if conversion_tasks[task_id]['status'] != 'pending':
        return jsonify({'error': '任务已在处理中或已完成'}), 400
    
    # 获取参数
    params = request.json
    
    # 准备输出路径
    output_folder = os.path.join(PPTvConfig.OUTPUT_FOLDER, task_id)
    os.makedirs(output_folder, exist_ok=True)
    
    # 文件名使用原文件名但扩展名改为mp4
    filename = conversion_tasks[task_id]['filename']
    base_name = os.path.splitext(filename)[0]
    output_filename = f"{base_name}.mp4"
    output_path = os.path.join(output_folder, output_filename)
    
    # 更新任务信息
    conversion_tasks[task_id]['output_path'] = output_path
    conversion_tasks[task_id]['params'] = params
    
    # 启动转换线程
    conversion_thread = threading.Thread(
        target=process_conversion,
        args=(task_id, conversion_tasks[task_id]['ppt_path'], output_path, params)
    )
    conversion_thread.start()
    
    return jsonify({
        'task_id': task_id,
        'status': 'processing',
        'message': '开始转换任务'
    })

@bp.route('/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """获取任务状态"""
    if task_id not in conversion_tasks:
        return jsonify({'error': '找不到任务'}), 404
    
    task = conversion_tasks[task_id]
    response = {
        'task_id': task_id,
        'status': task['status'],
        'filename': task['filename']
    }
    
    if task['status'] == 'completed':
        response['video_url'] = task['video_url']
    elif task['status'] == 'failed':
        response['error'] = task.get('error', '未知错误')
    
    return jsonify(response)

@bp.route('/videos/<task_id>', methods=['GET'])
def get_video(task_id):
    """获取生成的视频文件"""
    if task_id not in conversion_tasks:
        return jsonify({'error': '找不到任务'}), 404
    
    task = conversion_tasks[task_id]
    if task['status'] != 'completed':
        return jsonify({'error': '视频尚未生成完成'}), 400
    
    output_folder = os.path.dirname(task['output_path'])
    filename = os.path.basename(task['output_path'])
    
    # 根据请求参数决定是下载还是流式播放
    as_attachment = request.args.get('download', 'false').lower() == 'true'
    
    response = send_from_directory(output_folder, filename, as_attachment=as_attachment)
    
    # 如果是下载模式，添加必要的响应头
    if as_attachment:
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

# 添加直接访问静态视频文件的路由
@bp.route('/static/outputs/<path:task_id>/<path:filename>', methods=['GET'])
def serve_output_file(task_id, filename):
    """直接访问输出文件夹中的文件"""
    output_folder = os.path.join(PPTvConfig.OUTPUT_FOLDER, task_id)
    
    # 检查是否为下载请求
    as_attachment = request.args.get('download', 'false').lower() == 'true'
    
    response = send_from_directory(output_folder, filename, as_attachment=as_attachment)
    
    # 如果是下载模式，添加必要的响应头
    if as_attachment:
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.headers['Content-Type'] = 'application/octet-stream'
    
    return response

# 初始化必要的文件夹
os.makedirs(PPTvConfig.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PPTvConfig.OUTPUT_FOLDER, exist_ok=True)
