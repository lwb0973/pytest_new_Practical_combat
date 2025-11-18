import os
import subprocess
import settings
import multiprocessing
import pytest
import configparser
import requests
import socket
from conftest import get_local_ip, send_wechat_report,start_http_server




config = configparser.ConfigParser()
config.read(settings.INI_FILE, encoding='utf-8')
project_name = config.get('allure', 'Project')
WECHAT_KEY = config.get('WECHAT_WEBHOOK', 'webchat_key')
ALLURE_COMMAND = settings.ALLURE_COMMAND

# HTTP 服务端口
HTTP_PORT = 8888


def run_tests():
    # multiprocessing自动获取CPU核心数
    cpu_count = multiprocessing.cpu_count()
    pytest.main([
        "-v",
        # 自动根据 CPU 数量设置并发进程数,xdist分布式执行
        #  "-n", str(cpu_count),
        # 重复执行用例
        # "--count=1",
        # 失败用例重跑
        # "--reruns=3",
        # 重跑间隔时间
        "--reruns-delay=1",
        # 生成 Allure 原始结果在 result/ 目录
        "--alluredir=result",
        # 跳过指定用例
        # "-k", "not test_05",
        # 跳过指定py文件
        # "--ignore=testcase/.py",
        # 跳过整个包路径
        # "--ignore-glob=testcase/test_risk_overview/.py"

    ])

    # ----------------- 生成 Allure 报告 -----------------
    subprocess.run([ALLURE_COMMAND,"generate", "result","-o", "report","--clean", "--report-name", project_name])

    # ----------------- 推送企业微信 -----------------

    report_url = f"http://{get_local_ip()}:{HTTP_PORT}"
    send_wechat_report(WECHAT_KEY,report_url)

    # ----------------- 启动 HTTP 服务 -----------------
    print("启动本地 HTTP 服务以访问 Allure 报告...")
    start_http_server("report", HTTP_PORT)


if __name__ == "__main__":
    run_tests()