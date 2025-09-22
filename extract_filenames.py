import os
import re
import sys
from pathlib import Path

def natural_sort_key(name):
    """
    生成自然排序键，使数字按数值大小而不是字母顺序排序
    例如：["2.txt", "10.txt", "1.txt"] 会排序为 ["1.txt", "2.txt", "10.txt"]
    
    参数:
        name: 文件名或文件夹名
        
    返回:
        用于排序的元组
    """
    # 使用正则表达式将名称拆分为数字和非数字部分
    parts = re.split(r'(\d+)', name)
    # 将数字部分转换为整数，非数字部分保持原样
    return tuple(int(part) if part.isdigit() else part.lower() for part in parts)

def get_current_folder_items():
    """
    获取当前文件夹中的所有文件和文件夹（不包括脚本自身）
    
    返回:
        files: 当前文件夹中所有文件的Path对象列表
        folders: 当前文件夹中所有文件夹的Path对象列表
    """
    current_dir = Path.cwd()
    script_name = Path(__file__).name
    
    files = []
    folders = []
    
    for item in current_dir.iterdir():
        if item.name == script_name:
            continue  # 跳过脚本自身
        
        if item.is_file():
            files.append(item)
        elif item.is_dir():
            folders.append(item)
    
    return files, folders

def process_items():
    """
    主处理函数：获取文件和文件夹、排序、生成输出并保存结果
    """
    try:
        # 1. 获取当前文件夹中的文件和文件夹
        files, folders = get_current_folder_items()
        
        # 2. 检查是否有内容
        if len(files) == 0 and len(folders) == 0:
            print("\n[提示] 当前文件夹中没有找到任何文件或文件夹。")
            print("[INFO] No files or folders found in the current folder.")
            return False
        
        # 3. 按自然顺序排序文件和文件夹
        files.sort(key=lambda x: natural_sort_key(x.name))
        folders.sort(key=lambda x: natural_sort_key(x.name))
        
        # 4. 准备各种输出格式
        # 文件名（带后缀）
        filenames_with_ext = [f.name for f in files]
        # 文件名（无后缀）
        filenames_no_ext = [f.stem for f in files]
        # 文件夹名
        folder_names = [f.name for f in folders]
        
        # 绝对路径（文件带后缀）
        abspath_files_with_ext = [str(f.resolve()) for f in files]
        # 绝对路径（文件无后缀）
        abspath_files_no_ext = [str(f.parent.resolve() / f.stem) for f in files]
        # 绝对路径（文件夹）
        abspath_folders = [str(f.resolve()) for f in folders]
        
        # 5. 生成BallonsTranslator命令（仅针对文件）
        if files:
            ballons_translator_cmd = (
                "python.exe "
                f'launch.py --headless --exec_dirs "{",".join(abspath_files_no_ext)},{",".join(abspath_folders)}"'
            )
        else:
            ballons_translator_cmd = "无文件可处理"
        
        # 6. 构建输出内容
        output_content = f"""文件列表（共 {len(files)} 个）：
{",".join(filenames_with_ext) if files else "无文件"}

文件名（无后缀）：
{",".join(filenames_no_ext) if files else "无文件"}

文件夹列表（共 {len(folders)} 个）：
{",".join(folder_names) if folders else "无文件夹"}

绝对路径（文件）：
{",".join(abspath_files_with_ext) if files else "无文件"}

绝对路径（文件无后缀）：
{",".join(abspath_files_no_ext) if files else "无文件"}

绝对路径（文件夹）：
{",".join(abspath_folders) if folders else "无文件夹"}

BallonsTranslator批处理命令（在ballontrans_pylibs_win根目录执行或自行修改为绝对路径）：
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
        
        # 9. 显示统计信息
        print(f"\n统计信息：")
        print(f"文件数量: {len(files)}")
        print(f"文件夹数量: {len(folders)}")
        print(f"总计: {len(files) + len(folders)} 个项目")
        
        return True
        
    except Exception as e:
        print(f"\n[错误] 处理过程中发生异常: {str(e)}")
        print(f"[ERROR] Exception occurred during processing: {str(e)}")
        return False

if __name__ == "__main__":
    # 设置控制台编码为UTF-8以支持中文显示
    if sys.stdout.encoding != 'utf-8':
        os.system('chcp 65001 > nul' if os.name == 'nt' else '')  # Windows代码页设置为UTF-8
    
    success = process_items()
    
    # 暂停以便用户查看结果（仅在Windows下）
    if os.name == 'nt':
        input("\n按Enter键退出...")
    
    sys.exit(0 if success else 1)