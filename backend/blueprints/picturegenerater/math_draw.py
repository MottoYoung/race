# math_draw.py 修改后完整代码
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from mpl_toolkits.mplot3d import Axes3D  # 新增导入

def execute_math_code(code: str) -> str:
    """安全执行数学绘图代码并返回base64图片"""
    plt.close('all')
    
    # 扩展允许的本地变量
    allowed_locals = {
        'plt': plt,
        'np': np,
        'Axes3D': Axes3D,  # 显式提供3D绘图支持
        'sns': __import__('seaborn')  # 允许seaborn
    }
    
    try:
        # 使用受限的builtins
        safe_builtins = {
            '__import__': __import__,
            'range': range,
            'list': list,
            'dict': dict,
            'tuple': tuple
        }
        
        # 执行时传入必要的builtins
        exec(code, {'__builtins__': safe_builtins}, allowed_locals)
        
        # 确保图形已生成
        if len(plt.get_fignums()) == 0:
            raise RuntimeError("未生成任何图形")
            
        # 保存图像
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        plt.close()
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')
    except Exception as e:
        plt.close()
        raise RuntimeError(f"代码执行错误: {str(e)}")