from flask import request, jsonify
from zhipuai import ZhipuAI
import time
import base64
from . import bp

# 初始化 ZhipuAI 客户端，填写您的 API 密钥
client = ZhipuAI(api_key="3f29f735972641eea247413ef035ed44.18B04xjjzbdjv1L9")

@bp.route('/generate-video', methods=['POST'])
def generate_video():
    data = request.json

    # 获取前端传来的参数
    prompt = data.get('prompt', '')
    image_file = data.get('image', None)
    quality = data.get('quality', 'speed')
    with_audio = data.get('with_audio', False)
    size = data.get('size', '1920x1080')
    fps = data.get('fps', 30)

    # 如果有图片文件，将其编码为 Base64
    base64_encoded = None
    if image_file:
        image_data = image_file.split(',')[1]  # 前端传来的图片是 data:image/jpeg;base64,xxxxx 格式
        base64_encoded = image_data

    # 调用视频生成接口
    response = client.videos.generations(
        model="cogvideox-2",
        prompt=prompt,
        image_url=f"data:image/jpeg;base64,{base64_encoded}" if base64_encoded else None,
        quality=quality,
        with_audio=with_audio,
        size=size,
        fps=fps
    )

    # 获取任务 ID
    task_id = response.id

    # 查询视频生成结果
    result = None
    while True:
        result = client.videos.retrieve_videos_result(id=task_id)
        if result.task_status in ["SUCCESS", "FAIL"]:
            break
        time.sleep(5)  # 等待5秒后重试

    return jsonify({
        "status": result.task_status,
        "result": result.video_result[0].url if result.task_status == "SUCCESS" else None,
        "cover_image_url": result.video_result[0].cover_image_url if result.task_status == "SUCCESS" else None
    })
