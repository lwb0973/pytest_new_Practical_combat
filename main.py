import os
import shutil
import subprocess
import time
import settings
import multiprocessing
import pytest


ALLURE_COMMAND = settings.ALLURE_COMMAND

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
        "--reruns=3",
        # 重跑间隔时间
        "--reruns-delay=1",
        # 生成 Allure 原始结果在 result/ 目录
        "--alluredir=result",
        # 跳过指定用例
        "-k", "not test_05",
        # 跳过指定py文件
        # "--ignore=testcase/test_demo1.py"
    ])
    subprocess.run([ALLURE_COMMAND, "generate", "result", "-o", "report", "--clean"])
    subprocess.run([ALLURE_COMMAND, "open", "report"])


if __name__ == "__main__":
    run_tests()