# conftest.py
import os
import platform
from datetime import datetime
import settings
import configparser
import json
import socket
import requests



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


# # pytest 会在测试会话开始前调用这个钩子
# def pytest_sessionstart(session):
#     create_environment_file()


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


def get_local_ip():
    """获取本机 IP 地址"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def send_wechat_report(key, url):
    """发送企业微信通知 URL"""
    api = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"
    data = {"msgtype": "text","text": {"content": f"🎉 首页自动化准确性测试完成\n\n📊 Allure 测试报告已生成\n➡ {url}\n\n请点击上方链接查看完整可视化报告"}}
    r = requests.post(api, json=data)
    return r.json()


def start_http_server(directory, port):
    """启动 HTTP 服务，用于访问 Allure 报告"""
    import http.server
    import socketserver

    os.chdir(directory)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Allure 报告服务器已启动: http://{get_local_ip()}:{port}")
        httpd.serve_forever()