import PyInstaller.__main__
import os
import sys
import shutil
import platform

# 获取当前操作系统
SYSTEM = platform.system()
print(f"当前操作系统: {SYSTEM}")

# 获取脚本所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 切换到脚本目录
os.chdir(current_dir)

# 创建dist目录（如果不存在）
if not os.path.exists("dist"):
    os.makedirs("dist")

# 根据操作系统设置不同的分隔符和打包选项
if SYSTEM == "Windows":
    # Windows使用:作为分隔符
    separator = ":"
    exe_extension = ".exe"
    output_name = "CursorPatcher"
elif SYSTEM == "Darwin":  # macOS
    # macOS使用:作为分隔符
    separator = ":"
    exe_extension = ""
    output_name = "CursorPatcher"
elif SYSTEM == "Linux":
    # Linux使用:作为分隔符
    separator = ":"
    exe_extension = ""
    output_name = "CursorPatcher"
else:
    print(f"不支持的操作系统: {SYSTEM}")
    sys.exit(1)

# 定义依赖文件
data_files = [
    f"_utils.py{separator}.",
]

# 构建PyInstaller命令行参数
pyinstaller_args = [
    "patcher.py",
    "--onefile",  # 生成单个可执行文件
    "--clean",  # 清理临时文件
    "--noconfirm",  # 不确认覆盖
    f"--name={output_name}",  # 指定输出文件名
    "--icon=NONE",  # 无图标
]

# 添加依赖文件
for data_file in data_files:
    pyinstaller_args.append(f"--add-data={data_file}")

# 运行PyInstaller打包
print(f"正在打包Python脚本为可执行文件...")
PyInstaller.__main__.run(pyinstaller_args)

output_path = os.path.join("dist", output_name + exe_extension)
if os.path.exists(output_path):
    print(f"打包完成！可执行文件位于: {output_path}")
else:
    print("打包过程中出现错误，未生成可执行文件。")
