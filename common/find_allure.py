import os
import shutil
import platform

def find_allure():
    """
    自动查找 Allure 可执行文件路径（Windows/Linux/Mac通用）。
    优先顺序：
    1. 环境变量 ALLURE_HOME/bin/allure(.bat)
    2. 系统 PATH
    """
    system_platform = platform.system().lower()

    # 1. 从环境变量 ALLURE_HOME 查找
    allure_home = os.environ.get("ALLURE_HOME")
    if allure_home:
        if system_platform == "windows":
            exe = os.path.join(allure_home, "bin", "allure.bat")
        else:
            exe = os.path.join(allure_home, "bin", "allure")
        if os.path.exists(exe):
            return exe

    # 2. 从 PATH 中查找
    if system_platform == "windows":
        exe_name = "allure.bat"
    else:
        exe_name = "allure"
    exe = shutil.which(exe_name)
    if exe:
        return exe

    # 3. Windows 常见安装路径（可选）
    if system_platform == "windows":
        for path in [r"D:\allure", r"C:\allure"]:
            exe = os.path.join(path, "bin", "allure.bat")
            if os.path.exists(exe):
                return exe

    # 4. Linux/Mac 常见安装路径（可选）
    else:
        for path in ["/usr/local/bin/allure", "/opt/allure/bin/allure"]:
            if os.path.exists(path):
                return path

    raise FileNotFoundError(
        "找不到 Allure 可执行文件，请安装 Allure 并设置 ALLURE_HOME 或加入 PATH"
    )

# # 使用方法
# ALLURE_COMMAND = find_allure()
# print("Allure 可执行文件路径:", ALLURE_COMMAND)
