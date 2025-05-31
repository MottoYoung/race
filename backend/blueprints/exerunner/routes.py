import subprocess
import logging
from flask import request, jsonify
from . import bp

# 配置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@bp.route('', methods=['POST'])
def run_exe():
    """执行EXE文件并返回输出"""
    try:
        data = request.get_json()
        
        if not data or 'path' not in data:
            logger.error("请求中缺少path参数")
            return jsonify({"error": "缺少路径参数"}), 400
            
        path = data['path']
        logger.info(f"准备执行程序: {path}")
        
        # 执行EXE文件
        process = subprocess.Popen(
            path, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            shell=True  # 允许命令行参数，注意安全风险
        )
        
        # 获取输出
        stdout, stderr = process.communicate()
        
        # 检查执行结果
        if process.returncode != 0:
            logger.error(f"程序执行失败: {stderr}")
            return jsonify({
                "error": f"执行错误: {stderr}",
                "success": False
            }), 500
            
        logger.info(f"程序执行成功，退出码: {process.returncode}")
        return jsonify({
            "success": True,
            "output": stdout,
            "error": stderr
        })
        
    except Exception as e:
        logger.exception("执行过程中发生异常")
        return jsonify({
            "success": False,
            "error": f"服务器错误: {str(e)}"
        }), 500
