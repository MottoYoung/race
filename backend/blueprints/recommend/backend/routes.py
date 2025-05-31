from flask import Blueprint, render_template, jsonify, redirect, url_for, session, request, send_file
import os
import tempfile
import subprocess
import pickle
import json
import time
import random
import requests
from .model import VideoRecommender, ExerciseRecommender

# 创建蓝图文件所在的目录
bp = Blueprint('recommend', __name__, url_prefix='/api/recommend',
               template_folder='../frontend/templates',
               static_folder='../frontend/static')

# 配置
needed_video_num = 15
display_video_num = 9
top_k = 2 * needed_video_num

# 获取当前文件所在的目录
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RECOMMEND_DIR = os.path.dirname(CURRENT_DIR)

# 修改路径定义
THUMBNAIL_CACHE_DIR = os.path.join(RECOMMEND_DIR, 'frontend', 'static', 'thumbnails')
models_path = os.path.join(RECOMMEND_DIR, 'models')
resources_path = os.path.join(RECOMMEND_DIR, 'resources')

# 指定FFmpeg路径
FFMPEG_PATHS = [
    "ffmpeg",  # 系统PATH中的ffmpeg
    "D:\\app\\daily\\FFmpeg\\ffmpeg-7.1.1-full_build\\bin\\ffmpeg.exe",  # 已知可用的路径
]

# 推荐缓存
video_recommendation_cache = {}
CACHE_EXPIRY = 3000  # 缓存过期时间，单位为秒

# 检查哪个FFmpeg路径可用
def get_ffmpeg_path():
    for path in FFMPEG_PATHS:
        try:
            result = subprocess.run([path, '-version'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE, 
                                  check=False)
            if result.returncode == 0:
                return path
        except:
            continue
    return FFMPEG_PATHS[0]

# 设置FFmpeg路径
FFMPEG_PATH = get_ffmpeg_path()

# 禁用日志函数
def log_info(message):
    # 什么都不做
    pass

def log_error(message):
    # 只在严重错误时打印
    pass

# 加载用户ID映射文件
def load_user_mapping():
    user_map_path = os.path.join(models_path, 'user2idx_ex.pkl')
    try:
        with open(user_map_path, 'rb') as f:
            user_map = pickle.load(f)
        return user_map
    except Exception as e:
        print(f"加载用户映射文件失败: {str(e)}")
        print(f"尝试加载的路径: {os.path.abspath(user_map_path)}")
        print(f"当前工作目录: {os.getcwd()}")
        return {}

# 加载习题数据
def load_exercises():
    resource_path = resources_path
    
    if os.path.exists(os.path.join(resource_path, 'exercises.pkl')):
        try:
            with open(os.path.join(resource_path, 'exercises.pkl'), 'rb') as f:
                exercise_data = pickle.load(f)
                return exercise_data
        except Exception as e:
            print(f"加载习题数据出错: {str(e)}")
    else:
        try:
            with open(os.path.join(resource_path, 'problem.json'), 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.strip().split('\n')
                exercise_data = {}
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        item = json.loads(line)
                        if 'exercise_id' in item:
                            exercise_data[item['exercise_id']] = item
                    except json.JSONDecodeError:
                        print(f"无法解析JSON行: {line[:50]}...")
                pickle.dump(exercise_data, open(os.path.join(resource_path, 'exercises.pkl'), 'wb'))
            return exercise_data
        except FileNotFoundError:
            print(f"problem.json 文件未找到，路径: {os.path.abspath(os.path.join(resource_path, 'problem.json'))}")
        except Exception as e:
            print(f"加载习题数据出错: {str(e)}")
    return {}

# 加载pm_id到exercise_id的映射
def load_pm_id_exercise_id_map():
    resource_path = resources_path
    pm_id_exercise_id_map = {}
    try:
        with open(os.path.join(resource_path, 'exercise-problem.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                (val, key) = line.split()
                pm_id_exercise_id_map[key] = val
    except FileNotFoundError:
        print(f"exercise-problem.txt 文件未找到，路径: {os.path.abspath(os.path.join(resource_path, 'exercise-problem.txt'))}")
    return pm_id_exercise_id_map

# 加载视频信息
def load_video_info():
    resource_path = resources_path
    
    if os.path.exists(os.path.join(resource_path, 'video_info.pkl')):
        try:
            with open(os.path.join(resource_path, 'video_info.pkl'), 'rb') as f:
                video_info = pickle.load(f)
                return video_info
        except Exception as e:
            print(f"加载视频信息出错: {str(e)}")
    else:
        try:
            video_info = {}
            with open(os.path.join(resource_path, 'course.json'), 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        course = json.loads(line)
                        if 'resource' in course:
                            for item in course['resource']:
                                if item.get('resource_id', '').startswith('V_'):
                                    titles = item.get('titles', {})
                                    chapter_title = titles[0] if len(titles) > 0 else ''
                                    section_title = titles[1] if len(titles) > 1 else ''
                                    video_title = titles[2] if len(titles) > 2 else ''
                                    
                                    course_name = course.get('name', '') or '未知课程'
                                    chapter_title = chapter_title or '未知章节'
                                    section_title = section_title or '未知节'
                                    video_title = video_title or '未知视频'
                                    video_about = course.get('about', '') or '未知简介'
                                    video_chapter = item.get('chapter', '') or ''
                                    
                                    video_info[item['resource_id']] = {
                                        'course_name': course_name,
                                        'chapter_title': chapter_title,
                                        'section_title': section_title,
                                        'video_title': video_title,
                                        'video_about': video_about,
                                        'video_chapter': video_chapter
                                    }
                    except json.JSONDecodeError:
                        print(f"无法解析JSON行: {line[:50]}...")
                pickle.dump(video_info, open(os.path.join(resource_path, 'video_info.pkl'), 'wb'))
            return video_info
        except FileNotFoundError:
            print(f"course.json 文件未找到，路径: {os.path.abspath(os.path.join(resource_path, 'course.json'))}")
        except Exception as e:
            print(f"加载视频信息出错: {str(e)}")
    return {}

# 初始化全局变量
user_id_mapping = load_user_mapping()
user_ids = list(user_id_mapping.keys()) if user_id_mapping else []
pm_id_exercise_id_map = load_pm_id_exercise_id_map()
exercises_data = load_exercises()
video_info = load_video_info()

# 初始化推荐器
video_model_path = os.path.join(models_path, 'model_video.pt')
video_embedding_path = os.path.join(models_path, 'node_embeddings_video.pt')
user2idx_path = os.path.join(models_path, 'user2idx.pkl')
video2idx_path = os.path.join(models_path, 'video2idx.pkl')

exercise_model_path = os.path.join(models_path, 'ktm_lc_model.pt')
exercise_embedding_path = os.path.join(models_path, 'node_embeddings_exercises.pt')
user2idx_ex_path = os.path.join(models_path, 'user2idx_ex.pkl')
problem2idx_path = os.path.join(models_path, 'problem2idx.pkl')

video_recommender = VideoRecommender(
    model_path=video_model_path,
    embedding_path=video_embedding_path,
    user2idx_path=user2idx_path,
    video2idx_path=video2idx_path
)

exercises_recommender = ExerciseRecommender(
    model_path=exercise_model_path,
    embedding_path=exercise_embedding_path,
    user2idx_path=user2idx_ex_path,
    problem2idx_path=problem2idx_path
)

# 检查图片是否全黑或接近全黑
def check_if_image_is_black(image_path):
    try:
        from PIL import Image
        import numpy as np
        
        img = Image.open(image_path)
        img_gray = img.convert('L')
        img_array = np.array(img_gray)
        
        avg_brightness = np.mean(img_array)
        return avg_brightness < 20  # 阈值可以根据实际情况调整
    except:
        return False

# 生成彩色占位图
def generate_color_placeholder(ccid, output_path):
    try:
        from PIL import Image, ImageDraw
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # 为每个ccid创建一个独特的颜色
        color_seed = sum(ord(c) for c in ccid)
        r = (color_seed * 13) % 200 + 55
        g = (color_seed * 17) % 200 + 55
        b = (color_seed * 19) % 200 + 55
        
        # 创建图片
        img = Image.new('RGB', (480, 270), color=(r, g, b))
        draw = ImageDraw.Draw(img)
        
        # 添加播放图标
        play_button_radius = 40
        center_x, center_y = 480//2, 270//2
        
        # 绘制圆形按钮背景
        draw.ellipse((center_x-play_button_radius, center_y-play_button_radius, 
                     center_x+play_button_radius, center_y+play_button_radius), 
                     fill=(50, 50, 50, 200))
        
        # 绘制播放三角形
        triangle_points = [(center_x-15, center_y-15), 
                          (center_x-15, center_y+15), 
                          (center_x+20, center_y)]
        draw.polygon(triangle_points, fill=(255, 255, 255))
        
        # 保存图片
        img.save(output_path, 'JPEG', quality=90)
        
        return send_file(output_path, mimetype='image/jpeg')
    except Exception as e:
        log_error(f"生成占位图失败: {str(e)}")
        # 如果失败，返回基本图像
        import io
        buffer = io.BytesIO()
        buffer.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
        buffer.seek(0)
        return send_file(buffer, mimetype='image/png')

# 路由
@bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@bp.route('/login', methods=['POST'])
def login():
    student_name = request.form.get('studentName', '').strip()
    
    if not student_name:
        return render_template('login.html', error='请输入您的姓名')
    
    # 根据姓名生成一个0-999的随机数
    random_number = random.randint(0, 999)
    
    # 如果有用户ID列表，从中选择一个
    selected_user_id = None
    if user_ids:
        # 使用随机数作为索引选择用户ID
        index = random_number % len(user_ids)
        selected_user_id = user_ids[index]
    else:
        # 如果没有用户ID列表，使用默认ID
        selected_user_id = f"U_{random_number}"
    
    # 保存用户信息到session
    session['student_name'] = student_name
    session['user_id'] = selected_user_id
    
    print(f"用户 '{student_name}' 登录，分配ID: {selected_user_id}")
    
    # 重定向到视频推荐页面
    return redirect(url_for('recommend.index'))

@bp.route('/recommendations')
def index():
    # 检查用户是否已登录
    if 'user_id' not in session:
        return redirect(url_for('recommend.login_page'))
    
    user_id = session.get('user_id')
    student_name = session.get('student_name', '用户')
    
    # 检查缓存中是否有当前用户的推荐结果
    cache_key = f"video_rec_{user_id}"
    current_time = time.time()
    
    if cache_key in video_recommendation_cache and current_time - video_recommendation_cache[cache_key]['timestamp'] < CACHE_EXPIRY:
        # 使用缓存数据
        cache_data = video_recommendation_cache[cache_key]
        return render_template('video_recommendations.html',
                              student_name=student_name,
                              recommended_video_ccids=cache_data['recommended_video_ccids'],
                              video_thumbnails=cache_data['video_thumbnails'],
                              video_metadata=cache_data['video_metadata'])
    
    # 如果没有缓存或缓存已过期，重新获取推荐
    rec_videos, _ = video_recommender.recommend(user_id, top_k=top_k)
    video_ccid_map = {}
    
    try:
        with open(os.path.join(resources_path, 'video_id-ccid.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                (key, val) = line.split()
                video_ccid_map[key] = val
    except FileNotFoundError:
        return jsonify({"error": "video_id-ccid.txt not found"}), 404

    recommended_video_ccids = {}
    video_thumbnails = {}
    video_metadata = {}
    
    # 课程计数
    course_count = 0
    
    for video_id in rec_videos:
        if video_id in video_ccid_map:
            ccid = video_ccid_map[video_id]
            recommended_video_ccids[video_id] = ccid
            video_thumbnails[video_id] = url_for('recommend.video_thumbnail', ccid=ccid)
            
            # 从resource_to_course_map中获取视频元数据
            if video_id in video_info:
                video_metadata[video_id] = {
                    'course_name': video_info[video_id].get('course_name', '未知课程'),
                    'chapter_title': video_info[video_id].get('chapter_title', '未知章节'),
                    'section_title': video_info[video_id].get('section_title', '未知节'),
                    'video_title': video_info[video_id].get('video_title', '未知视频'),
                    'video_about': video_info[video_id].get('video_about', '未知简介'),
                    'video_chapter': video_info[video_id].get('video_chapter', '')
                }
            else:
                # 如果在course.json中找不到，使用默认值
                video_metadata[video_id] = {
                    'course_name': '未知课程',
                    'chapter_title': '未知章节',
                    'section_title': '未知节',
                    'video_title': '未知视频',
                    'video_about': '未知简介',
                    'video_chapter': ''
                }
            # 课程计数增加
            course_count += 1
            if course_count >= display_video_num:  # 限制显示数量
                break
                
    # 更新缓存
    video_recommendation_cache[cache_key] = {
        'timestamp': current_time,
        'recommended_video_ccids': recommended_video_ccids,
        'video_thumbnails': video_thumbnails,
        'video_metadata': video_metadata
    }

    return render_template('video_recommendations.html',
                          student_name=student_name, 
                          recommended_video_ccids=recommended_video_ccids,
                          video_thumbnails=video_thumbnails,
                          video_metadata=video_metadata)

@bp.route('/proxy/video_url/<ccid>')
def proxy_video_url(ccid):
    try:
        response = requests.get(f'https://www.xuetangx.com/api/v1/lms/service/playurl/{ccid}/?appid=10000')
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/play_video/<ccid>')
def play_video(ccid):
    try:
        response = requests.get(f'https://www.xuetangx.com/api/v1/lms/service/playurl/{ccid}/?appid=10000')
        data = response.json()
        
        if data.get('success') and data.get('data') and data.get('data').get('sources'):
            sources = data['data']['sources']
            
            video_url = None
            if sources.get('quality20') and len(sources['quality20']) > 0:
                video_url = sources['quality20'][0]
            elif sources.get('quality10') and len(sources['quality10']) > 0:
                video_url = sources['quality10'][0]
            
            # 设置默认视频信息
            course_name = '未知课程'
            chapter_title = '未知章节'
            section_title = '未知节'
            video_title = '未知视频'
            video_about = '该课程没有简介~'
            video_chapter = ''
            
            # 查找对应的视频ID
            video_id = None
            cache_key = f"video_rec_{session.get('user_id', '')}"
            
            if cache_key in video_recommendation_cache:
                cache_data = video_recommendation_cache[cache_key]
                
                # 反向查找 - 通过ccid找到video_id
                for v_id, cached_ccid in cache_data['recommended_video_ccids'].items():
                    if cached_ccid == ccid:
                        video_id = v_id
                        
                        # 从缓存中获取视频元数据
                        if v_id in cache_data['video_metadata']:
                            metadata = cache_data['video_metadata'][v_id]
                            course_name = metadata.get('course_name') or course_name
                            chapter_title = metadata.get('chapter_title') or chapter_title
                            section_title = metadata.get('section_title') or section_title
                            video_title = metadata.get('video_title') or video_title
                            video_about = metadata.get('video_about') or video_about
                            video_chapter = metadata.get('video_chapter') or video_chapter
                            break
            
            # 如果在缓存中找不到，尝试从所有缓存中查找
            if course_name == '未知课程':
                for key, cache_data in video_recommendation_cache.items():
                    for v_id, cached_ccid in cache_data['recommended_video_ccids'].items():
                        if cached_ccid == ccid and v_id in cache_data['video_metadata']:
                            metadata = cache_data['video_metadata'][v_id]
                            course_name = metadata.get('course_name') or course_name
                            chapter_title = metadata.get('chapter_title') or chapter_title
                            section_title = metadata.get('section_title') or section_title
                            video_title = metadata.get('video_title') or video_title
                            video_about = metadata.get('video_about') or video_about
                            video_chapter = metadata.get('video_chapter') or video_chapter
                            video_id = v_id
                            break
                    if course_name != '未知课程':
                        break
                
            # 如果在缓存中找不到，但我们知道视频ID，尝试从video_info中获取
            if video_id and video_id in video_info:
                resource_info = video_info[video_id]
                course_name = resource_info.get('course_name') or course_name
                chapter_title = resource_info.get('chapter_title') or chapter_title
                section_title = resource_info.get('section_title') or section_title
                video_title = resource_info.get('video_title') or video_title
                video_about = resource_info.get('video_about') or video_about
                video_chapter = resource_info.get('video_chapter') or video_chapter
            
            # 直接从video_info中查找所有视频，看是否有匹配的ccid
            if course_name == '未知课程':
                try:
                    with open(os.path.join(resources_path, 'video_id-ccid.txt'), 'r', encoding='utf-8') as f:
                        for line in f:
                            try:
                                (key, val) = line.split()
                                if val == ccid and key in video_info:
                                    resource_info = video_info[key]
                                    course_name = resource_info.get('course_name') or course_name
                                    chapter_title = resource_info.get('chapter_title') or chapter_title
                                    section_title = resource_info.get('section_title') or section_title
                                    video_title = resource_info.get('video_title') or video_title
                                    video_about = resource_info.get('video_about') or video_about
                                    video_chapter = resource_info.get('video_chapter') or video_chapter
                                    break
                            except:
                                continue
                except Exception as e:
                    print(f"查找ccid时出错: {str(e)}")
                
            if video_url:
                return render_template('video_player.html',
                                      video_url=video_url, 
                                      ccid=ccid,
                                      course_name=course_name,
                                      chapter_title=chapter_title,
                                      section_title=section_title,
                                      video_title=video_title,
                                      video_about=video_about,
                                      video_chapter=video_chapter)
            else:
                return jsonify({"error": "No video source found"}), 404
        else:
            return jsonify({"error": "Invalid API response"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/video_thumbnail/<ccid>')
def video_thumbnail(ccid):
    log_info(f"请求视频 {ccid} 的缩略图")
    
    # 确保缓存目录存在
    thumbnails_dir = os.path.abspath(THUMBNAIL_CACHE_DIR)
    if not os.path.exists(thumbnails_dir):
        os.makedirs(thumbnails_dir, exist_ok=True)
    
    # 缓存路径
    cache_path = os.path.join(thumbnails_dir, f'{ccid}.jpg')
    
    # 如果缓存存在，直接返回
    if os.path.exists(cache_path):
        log_info(f"从缓存返回缩略图: {cache_path}")
        return send_file(cache_path, mimetype='image/jpeg')
    
    try:
        log_info(f"开始为视频 {ccid} 生成缩略图")
        response = requests.get(f'https://www.xuetangx.com/api/v1/lms/service/playurl/{ccid}/?appid=10000')
        data = response.json()
        
        if data.get('success') and data.get('data') and data.get('data').get('sources'):
            sources = data['data']['sources']
            
            # 获取视频URL
            video_url = None
            if sources.get('quality20') and len(sources['quality20']) > 0:
                video_url = sources['quality20'][0]
            elif sources.get('quality10') and len(sources['quality10']) > 0:
                video_url = sources['quality10'][0]
            
            if video_url:
                # 创建临时文件
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                    thumbnail_path = temp_file.name
                
                # 尝试多个时间点，直到找到非黑色的帧
                time_points = ['5','10','15']
                
                for time_point in time_points:
                    try:
                        log_info(f"尝试从时间点 {time_point} 提取帧")
                        
                        # 请求头
                        headers = (
                            f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36\r\n"
                            f"Referer: https://www.xuetangx.com/\r\n"
                        )
                        
                        # FFmpeg命令
                        ffmpeg_cmd = [
                            FFMPEG_PATH,
                            '-y',
                            '-headers', headers,
                            '-ss', time_point,
                            '-i', video_url,
                            '-frames:v', '1',
                            '-q:v', '2',
                            thumbnail_path
                        ]
                        
                        process = subprocess.run(ffmpeg_cmd, 
                                               stdout=subprocess.PIPE, 
                                               stderr=subprocess.PIPE,
                                               text=True)
                        
                        # 检查是否成功生成缩略图
                        if os.path.exists(thumbnail_path) and os.path.getsize(thumbnail_path) > 0:
                            # 检查生成的图片是否全黑
                            is_black = check_if_image_is_black(thumbnail_path)
                            if not is_black:
                                # 将缩略图保存到缓存
                                import shutil
                                shutil.copy(thumbnail_path, cache_path)
                                log_info(f"缩略图已保存到缓存: {cache_path}")
                                return send_file(cache_path, mimetype='image/jpeg')
                            else:
                                log_info("生成的帧是黑色的，尝试下一个时间点")
                    except Exception as e:
                        log_info(f"尝试从时间点 {time_point} 提取缩略图失败: {str(e)}")
                        continue
                
                # 尝试其他方法获取缩略图
                return generate_color_placeholder(ccid, cache_path)
        
        # 如果所有方法都失败，返回彩色占位图
        log_info("所有方法均失败，返回彩色占位图")
        return generate_color_placeholder(ccid, cache_path)
    except Exception as e:
        log_info(f"获取视频缩略图时出错: {str(e)}")
        return generate_color_placeholder(ccid, cache_path)
    finally:
        # 尝试删除临时文件
        try:
            if 'thumbnail_path' in locals() and os.path.exists(thumbnail_path):
                os.unlink(thumbnail_path)
        except:
            pass

@bp.route('/static/images/video-placeholder.jpg')
def default_placeholder():
    """提供默认占位图，避免404错误"""
    from PIL import Image, ImageDraw
    import io
    
    # 创建一个深灰色背景的占位图
    img = Image.new('RGB', (480, 270), color=(40, 40, 40))
    draw = ImageDraw.Draw(img)
    
    # 绘制播放按钮
    play_radius = 40
    draw.ellipse((240-play_radius, 135-play_radius, 240+play_radius, 135+play_radius), fill=(80, 80, 80))
    draw.polygon([(230, 115), (230, 155), (265, 135)], fill=(200, 200, 200))
    
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/jpeg')

@bp.route('/exercises')
def exercises():
    # 检查用户是否已登录
    if 'user_id' not in session:
        return redirect(url_for('recommend.login_page'))
    
    user_id = session.get('user_id')
    student_name = session.get('student_name', '用户')
    
    # 获取推荐习题
    recommended_exercises = []
    try:
        # 获取推荐的习题ID
        rec_pm_ids, _ = exercises_recommender.recommend(user_id, top_k=top_k)
        
        # 将pm_id转换为exercise_id并获取习题内容
        for pm_id in rec_pm_ids:
            if pm_id in pm_id_exercise_id_map:
                exercise_id = pm_id_exercise_id_map[pm_id]
                if exercise_id in exercises_data:
                    recommended_exercises.append(exercises_data[exercise_id])
            
            # 限制习题数量
            if len(recommended_exercises) >= 10:
                break
    except Exception as e:
        print(f"获取习题推荐时出错: {str(e)}")

    # 渲染习题页面
    return render_template('exercises.html', 
                          student_name=student_name,
                          recommended_exercises=recommended_exercises)

@bp.route('/clear_cache')
def clear_cache():
    """清除缩略图缓存"""
    try:
        thumbnails_dir = os.path.abspath(THUMBNAIL_CACHE_DIR)
        if os.path.exists(thumbnails_dir):
            for file_name in os.listdir(thumbnails_dir):
                file_path = os.path.join(thumbnails_dir, file_name)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
        
        return jsonify({
            "success": True,
            "message": "缩略图缓存已清除",
            "cache_dir": thumbnails_dir
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"清除缓存失败: {str(e)}"
        })

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('recommend.login_page'))

@bp.route('/clear_recommendation_cache')
def clear_recommendation_cache():
    global video_recommendation_cache
    video_recommendation_cache = {}
    return jsonify({"success": True, "message": "推荐缓存已清除"})
