import os
import json
import logging
from flask import request, jsonify
from . import bp
from .xfPPT_service import PPTGenerator
from .xfPPT_demo import AIPPT

# 配置参数
APP_ID = "b341104d"
API_SECRET = "YWI5ZDRhNTdmNGZjNmVjYjg3OWMwZGUz"
TEMP_DIR = os.path.join(os.path.dirname(__file__), 'tmp')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'md'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建临时目录
os.makedirs(TEMP_DIR, exist_ok=True)

def allowed_file(filename):
    """验证文件扩展名是否合法"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/templates', methods=['GET'])
def get_templates():
    """获取PPT模板列表"""
    try:
        # 解析请求参数
        current_page = request.args.get('currentPage', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        style = request.args.get('style', '')
        color = request.args.get('color', '')

        # 调用模板接口
        generator = AIPPT(APP_ID, API_SECRET, "", "")
        raw_data = generator.getTheme(current_page, page_size, style, color)
        templates = json.loads(raw_data)

        # 处理响应数据
        if templates.get('code', 0) != 0:
            return jsonify({
                "code": 500,
                "error": templates.get('desc', '模板获取失败')
            }), 500

        # 格式化模板数据
        formatted_templates = []
        for t in templates.get('data', {}).get('records', []):
            try:
                detail_image = json.loads(t.get("detailImage", "{}"))
                formatted_templates.append({
                    "id": t.get("templateIndexId"),
                    "name": f"{t.get('style', '未知')}-{t.get('industry', '通用')}",
                    "cover": detail_image.get("titleCoverImageLarge", "")
                })
            except Exception as e:
                logger.error(f"模板记录解析失败: {str(e)}")

        return jsonify({
            "code": 0,
            "data": {
                "list": formatted_templates,
                "total": templates.get('data', {}).get('total', 0)
            }
        })

    except Exception as e:
        logger.error(f"模板加载失败: {str(e)}")
        return jsonify({
            "code": 500,
            "error": f"服务器错误: {str(e)}"
        }), 500

@bp.route('/generate', methods=['POST'])
def generate_ppt():
    # 验证必要参数
    if 'templateId' not in request.form:
        return jsonify({"code": 400, "error": "缺少模板ID参数"}), 400
        
    template_id = request.form['templateId']
    generator = PPTGenerator(APP_ID, API_SECRET, template_id)
    """处理PPT生成请求"""
    try:
        # 文件处理逻辑
        if 'file' in request.files:
            file = request.files['file']
            if not file or file.filename == '':
                return jsonify({"code": 400, "error": "请选择有效文件"}), 400

            # 验证文件类型
            if not allowed_file(file.filename):
                return jsonify({
                    "code": 400,
                    "error": f"不支持的文件类型，允许类型: {', '.join(ALLOWED_EXTENSIONS)}"
                }), 400

            # 保存临时文件
            temp_path = os.path.join(TEMP_DIR, file.filename)
            try:
                file.save(temp_path)
            except Exception as e:
                logger.error(f"文件保存失败: {str(e)}")
                return jsonify({
                    "code": 500,
                    "error": "文件上传失败，请重试"
                }), 500

            # 生成大纲
            try:
                outline_gen = AIPPT(APP_ID, API_SECRET, "", "")
                outline_res = outline_gen.createOutlineByDoc(
                    fileName=file.filename,
                    filePath=temp_path
                )
                outline_data = json.loads(outline_res)
                
                if outline_data.get('code', 1) != 0:
                    error_msg = outline_data.get('desc', '大纲生成失败')
                    logger.error(f"大纲生成失败: {error_msg}")
                    return jsonify({
                        "code": 500,
                        "error": f"大纲生成失败: {error_msg}"
                    }), 500

            except Exception as e:
                logger.error(f"大纲生成异常: {str(e)}")
                return jsonify({
                    "code": 500,
                    "error": "大纲生成服务异常"
                }), 500
            finally:
                # 清理临时文件
                if os.path.exists(temp_path):
                    os.remove(temp_path)

            # 通过大纲生成PPT
            try:
                description = request.form.get('query', '').strip()
                task_id = generator.createPptByOutline(
                    outline=outline_data['data']['outline'],
                    query=description or f"基于文件《{file.filename}》生成"  # 添加默认描述
                )
            except Exception as e:
                logger.error(f"PPT生成失败: {str(e)}")
                return jsonify({
                    "code": 500,
                    "error": "PPT生成服务异常"
                }), 500

        else:
            description = request.form.get('query', '').strip()
            # 文本生成逻辑
            if not description:
                return jsonify({
                    "code": 400,
                    "error": "请输入内容描述或选择文件"
                }), 400

            if len(description) > 8000:
                return jsonify({
                    "code": 400,
                    "error": "内容描述超过8000字限制"
                }), 400

            try:
                task_id = generator.create_task(description)
            except Exception as e:
                logger.error(f"文本生成失败: {str(e)}")
                return jsonify({
                    "code": 500,
                    "error": "PPT生成服务异常"
                }), 500

        return jsonify({
            "code": 0,
            "task_id": task_id
        })

    except Exception as e:
        logger.error(f"生成异常: {str(e)}", exc_info=True)
        return jsonify({
            "code": 500,
            "error": "服务器内部错误"
        }), 500

@bp.route('/status/<sid>', methods=['GET'])
def check_status(sid):
    """检查PPT生成状态"""
    try:
        if not sid or len(sid) != 32:
            return jsonify({
                "code": 400,
                "error": "无效任务ID"
            }), 400

        generator = PPTGenerator(APP_ID, API_SECRET, "")
        status = generator.get_progress(sid)
        
        # 确保返回标准格式
        return jsonify({
            "code": status.get('code', 0),
            "data": status.get('data', {}),
            "error": status.get('error', '')
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "error": f"状态查询失败: {str(e)}",
            "data": {}
        }), 500
