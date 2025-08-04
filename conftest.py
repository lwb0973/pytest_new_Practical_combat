# conftest.py
import os
import platform
from datetime import datetime
import settings
import configparser
import json



config = configparser.ConfigParser()
config.read(settings.INI_FILE, encoding='utf-8')
project_name = config.get('allure','Project')
config_ip = config.get('login','sc_ip')


def to_unicode_escape(s: str) -> str:
    """将中文等非 ASCII 字符转为 \\uXXXX 编码"""
    return ''.join(f'\\u{ord(c):04x}' if ord(c) > 127 else c for c in s)

def create_environment_file():
    """自动创建 environment.properties 文件"""
    # 获取当前环境信息
    env_info = {
        "ENV": os.environ.get("ENV", "unknown"),
        "OS": f"{platform.system()} {platform.release()}",
        "Python": platform.python_version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "RunTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "User": os.environ.get("USERNAME") or os.environ.get("USER", "unknown"),
        "Project": project_name
    }

    # allure 结果目录
    allure_result_dir = settings.RESULT_FILE
    os.makedirs(allure_result_dir, exist_ok=True)
    # 写入 environment.properties
    env_file = os.path.join(allure_result_dir, "environment.properties")
    with open(env_file, "w", encoding="utf-8") as f:
        for key, value in env_info.items():
            safe_value = to_unicode_escape(value)
            f.write(f"{key}={safe_value}\n")


# pytest 会在测试会话开始前调用这个钩子
def pytest_sessionstart(session):
    create_environment_file()


# allure测试报告写入运行器信息
# 写入 executor.json
executor_info = {
    "name": "卢生",
    "type": "local",
    "url": "https://"+config_ip,
    "buildOrder": 1,
    "buildName": "首页准确性测试",
    "buildUrl": "https://"+config_ip,
    "reportUrl": "https://"+config_ip
}
os.makedirs(settings.RESULT_FILE, exist_ok=True)
with open(f"{settings.RESULT_FILE}/executor.json", "w", encoding="utf-8") as f:
    json.dump(executor_info, f, ensure_ascii=False, indent=2)



