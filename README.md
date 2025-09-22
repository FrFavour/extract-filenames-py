# 程序使用说明

## 前言

原项目：[WeMingT/extract-filenames](https://github.com/WeMingT/extract-filenames)

该程序为对原项目的 Python 重构，并添加了新的功能，适用于无法执行 bat 脚本的设备。

该程序运行不需要原项目，但如果没有它，我的程序是不可能的，请支持它。

## 工具简介

`extract_filenames.py` 是一个用于提取**同级目录**下所有**文件名**以及所有**文件夹名**的脚本程序。该程序会自动获取与该程序处于同级目录下的文件和文件夹名称并输出。

## 功能特点

- 获取同级目录中所有**文件**的文件名以及**文件夹**的文件夹名
- 获取的名称按升序排序
- 获取的名称按英文逗号分割
- 同时提取名称和绝对路径
- 支持带后缀和无后缀的文件名输出
- 支持带后缀和无后缀的文件名的绝对路径输出
- 支持生成 [BallonsTranslator](https://github.com/dmMaze/BallonsTranslator) 批处理命令行
- 输出内容会于终端显示并保存到 `extract_filenames_output.txt` 文件
- 不包括子文件夹，只提取本目录的文件、文件夹
- 支持中文文件名，无乱码问题
- 文件和文件夹数量统计
- 具有错误处理机制

## 使用方法

### 1. 安装 Python

安装 [Python](https://www.python.org/downloads/release/python-31011) **<= 3.12**，若设备中已有 python 环境，可跳过此步骤。

> **验证安装：**
>
> Win + R 打开 cmd 终端，输入 `python` ，如果有显示 python 版本信息并进入 python 执行模式，则安装成功。

### 2. 程序放置

将 `extract_filenames.py` 放置在目标文件夹中。

例如：

```txt
目标文件夹/
├── extract_filenames.py         # 脚本程序自身
├── 文档1.docx					# 文件
├── 文档2.docx					# 文件
├── 文件夹                        # 文件夹
├── 图像.jpg                      # 文件夹
└── 压缩文件.rar                  # 文件
```

### 3. 运行程序

在目标文件夹中打开 `cmd` 终端

执行以下代码运行程序：

```powershell
python extract_filenames.py
```

### 4. 查看结果

- 程序运行后会在终端上显示所有文件以及文件夹名和绝对路径（用英文逗号分隔）
- 同时会在程序所在目录生成 `extract_filenames_output.txt` 文件保存结果

## 输出示例

假设目标文件夹中有以下文件：
```txt
目标文件夹/
├── extract_filenames.py         # 脚本程序自身
├── 文档1.docx					# 文件
├── 文档2.docx					# 文件
├── 文件夹                        # 文件夹
├── 图像.jpg                      # 文件夹
└── 压缩文件.rar                  # 文件
```
程序输出：

```powershell
E:\目标文件夹>python extract_filenames.py

------------------------------------- 结果 / Results ---------------------------------
文件列表（共 4 个）：
压缩文件.rar,图像.jpg,文档1.docx,文档2.docx

文件名（无后缀）：
压缩文件,图像,文档

文件夹列表（共 1 个）：
文件夹

绝对路径（文件）：
E:\目标文件夹\压缩文件.rar,E:\目标文件夹\图像.jpg,E:\目标文件夹\文档1.docx,E:\目标文件夹\文档2.docx

绝对路径（文件无后缀）：
E:\目标文件夹\压缩文件,E:\目标文件夹\图像,E:\目标文件夹\文档1,E:\目标文件夹\文档2

绝对路径（文件夹）：
E:\目标文件夹\文件夹

BallonsTranslator批处理命令（在ballontrans_pylibs_win根目录执行或自行修改为绝对路径）：
python.exe launch.py --headless --exec_dirs "E:\目标文件夹\压缩文件,E:\目标文件夹\图像,E:\目标文件夹\文档1,E:\目标文件夹\文档2,E:\目标文件夹\文件夹"
--------------------------------------------------------------------------------------

结果已保存到： E:\目标文件夹\extract_filenames_output.txt
Results have been saved to: E:\目标文件夹\extract_filenames_output.txt

统计信息：
文件数量: 4
文件夹数量: 1
总计: 5 个项目
```

## BallonsTranslator 集成功能

程序集成 [BallonsTranslator](https://github.com/dmMaze/BallonsTranslator) 批处理命令行生成功能，可以直接生成用于 BallonsTranslator 的命令行：

```text
python.exe launch.py --headless --exec_dirs "绝对路径（无后缀）"
```

适用于批量处理图像翻译任务，可以直接复制生成的命令行到终端运行。

需在 BallonsTranslator 根目录下的 ballontrans_pylibs_win 目录执行该命令行，或自行将执行路径修改为 ballontrans_pylibs_win 目录下 python.exe 程序的绝对路径。

## 注意事项

1. 程序只提取程序所在目录的文件及文件夹名称，不包括子文件夹
2. 如果目录不存在或没有文件，程序会显示相应提示
3. 输出结果保存在程序同目录下的 `extract_filenames_output.txt` 文件中

## 故障排除

**[提示]"当前文件夹中没有找到任何文件或文件夹"**：

检查程序是否放在正确的位置，确认目标文件夹中确实存在文件

**[提示]程序无法运行**：

尝试以管理员权限运行 cmd 终端或检查文件的权限

**[提示]python : 无法将“python”项识别为 cmdlet、函数、脚本文件或可运行程序的名称...**

确保 python 被正确地安装并将 path 添加到环境变量中
