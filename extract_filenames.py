import os
import re
import sys
from pathlib import Path

def natural_sort_key(filename):
    """
    生成自然排序键，使数字按数值大小而不是字母顺序排序
    例如：["2.txt", "10.txt", "1.txt"] 会排序为 ["1.txt", "2.txt", "10.txt"]
    """
    # 使用正则表达式将文件名拆分为数字和非数字部分[7](@ref)
    parts = re.split(r'(\d+)', filename)
    # 将数字部分转换为整数，非数字部分保持原样
    return tuple(int(part) if part.isdigit() else part.lower() for part in parts)

def get_current_folder_files():
    """
    获取当前文件夹中的所有文件（不包括子文件夹和脚本自身）
    
    返回:
        当前文件夹中所有文件的Path对象列表
    """
    current_dir = Path.cwd()
    # 获取所有文件，排除子目录和脚本自身[6,7](@ref)
    return [f for f in current_dir.iterdir() if f.is_file() and f.name != Path(__file__).name]

def process_files():
    """
    主处理函数：获取文件、排序、生成输出并保存结果
    """
    try:
        # 1. 获取当前文件夹中的文件
        files = get_current_folder_files()
        
        # 2. 检查是否有文件
        if len(files) == 0:
            print("\n[提示] 当前文件夹中没有找到任何文件。")
            print("[INFO] No files found in the current folder.")
            return False
        
        # 3. 按自然顺序排序文件
        files.sort(key=lambda x: natural_sort_key(x.name))
        
        # 4. 准备各种输出格式
        # 带后缀的文件名
        filenames_with_ext = [f.name for f in files]
        # 无后缀的文件名
        filenames_no_ext = [f.stem for f in files]
        # 带后缀的绝对路径（使用resolve()确保包含盘符）[3,5](@ref)
        abspath_with_ext = [str(f.resolve()) for f in files]
        # 无后缀的绝对路径
        abspath_no_ext = [str(f.parent.resolve() / f.stem) for f in files]
        
        # 5. 生成BallonsTranslator命令
        ballons_translator_cmd = (
            "python.exe "
            f'launch.py --headless --exec_dirs "{",".join(abspath_no_ext)}"'
        )
        
        # 6. 构建输出内容
        output_content = f"""文件名：
{",".join(filenames_with_ext)}

文件名（无后缀）：
{",".join(filenames_no_ext)}

绝对路径：
{",".join(abspath_with_ext)}

绝对路径（无后缀）：
{",".join(abspath_no_ext)}

BallonsTranslator批处理命令[在ballontrans_pylibs_win的根目录执行]：
{ballons_translator_cmd}"""
        
        # 7. 保存到文件（UTF-8编码确保支持中文）
        output_file = Path(__file__).parent / "extract_filenames_output.txt"
        output_file.write_text(output_content, encoding='utf-8')
        
        # 8. 在屏幕上显示结果
        print("\n" + "-" * 60 + " 结果 / Results " + "-" * 60)
        print(output_content)
        print("-" * 135)
        print(f"\n结果已保存到： {output_file}")
        print(f"Results have been saved to: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"\n[错误] 处理过程中发生异常: {str(e)}")
        print(f"[ERROR] Exception occurred during processing: {str(e)}")
        return False

if __name__ == "__main__":
    # 设置控制台编码为UTF-8以支持中文显示
    if sys.stdout.encoding != 'utf-8':
        os.system('chcp 65001 > nul' if os.name == 'nt' else '')  # Windows代码页设置为UTF-8[1](@ref)
    
    success = process_files()
    
    # 暂停以便用户查看结果（仅在Windows下）
    if os.name == 'nt':
        input("\n按Enter键退出...")
    
    sys.exit(0 if success else 1)