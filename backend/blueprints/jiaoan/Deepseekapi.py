from openai import OpenAI
import os
import PyPDF2
import docx
import markdown
from markdown import markdown
from io import StringIO
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor
# 初始化OpenAI客户端

client = OpenAI(
     # 请用知识引擎原子能力API Key将下行替换为：api_key="sk-xxx",
    api_key="sk-YjWqwufd8oH0EWTaS3Kfts8rWcPpp9GNqsnblVKQ9fCj8vNt",  # 如何获取API Key：https://cloud.tencent.com/document/product/1772/115970
    base_url="https://api.lkeap.cloud.tencent.com/v1",
)

# 读取PDF文件内容
def read_pdf(file_path):
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

# 读取Word文件内容
def read_word(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# 读取txt文件内容
def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# 读取Markdown文件内容
def read_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    html = markdown.markdown(md_content)
    return html  # 返回HTML格式文本，或你可以继续提取纯文本

# 添加内存缓存装饰器
from functools import lru_cache

@lru_cache(maxsize=100)
def get_file_content(file_path: str) -> str:
    """增强版文件解析（添加缓存和异常处理）"""
    try:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext == '.pdf':
            return read_pdf(file_path)
        elif ext == '.docx':
            return read_word(file_path)
        elif ext == '.txt':
            return read_txt(file_path)
        elif ext == '.md':
            return read_md(file_path)
        else:
            raise ValueError(f"不支持的文件类型: {ext}")
            
    except Exception as e:
        raise RuntimeError(f"文件解析失败: {str(e)}")


def main():
    reasoning_content = ""  # 定义完整思考过程
    answer_content = ""  # 定义完整回复
    is_answering = False  # 判断是否结束思考过程并开始回复

    # 读取文件内容
    # file_path = "E:\Documents\AI辅助的教师备课系统构建.pdf"  # 请替换为你实际的文件路径
    # file_content = get_file_content(file_path)

    # 用户输入信息
    user_input = input("请输入你的信息：")

    # 选择是否上传文件
    file_path = input("是否上传文件？请输入文件路径或直接回车跳过：")
    file_content = ""

    if file_path:
        try:
            file_content = get_file_content(file_path)
        except Exception as e:
            print(f"文件读取失败：{e}")
            file_content = ""

    # 合并用户输入文本和文件内容
    full_content = user_input + "\n\n" + file_content
    print("\n" + "=" * 20 + "完整输入" + "=" * 20 + "\n")
    print(full_content)
    # 创建聊天完成请求
    stream = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1",  # 此处以 deepseek-r1 为例，可按需更换模型名称
        messages=[
            {"role": "user", "content": full_content}
        ],
        stream=True
    )

    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

    for chunk in stream:
        # 处理usage信息
        if not getattr(chunk, 'choices', None):
            print("\n" + "=" * 20 + "Token 使用情况" + "=" * 20 + "\n")
            print(chunk.usage)
            continue

        delta = chunk.choices[0].delta

        # 处理空内容情况
        if not getattr(delta, 'reasoning_content', None) and not getattr(delta, 'content', None):
            continue

        # 处理开始回答的情况
        if not getattr(delta, 'reasoning_content', None) and not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
            is_answering = True

        # 处理思考过程
        if getattr(delta, 'reasoning_content', None):
            print(delta.reasoning_content, end='', flush=True)
            reasoning_content += delta.reasoning_content
        # 处理回复内容
        elif getattr(delta, 'content', None):
            print(delta.content, end='', flush=True)
            answer_content += delta.content


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"发生错误：{e}")