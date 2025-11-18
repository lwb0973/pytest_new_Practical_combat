import os
from common.find_allure import find_allure

allure_path = find_allure()
# 获取项目根路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 获取测试数据路径
DATA_FILE = os.path.join(BASE_DIR, 'test_data', 'testcase.xlsx')
# 获取存放日志路径
TEST_DATA_FILE = os.path.join(BASE_DIR, 'logs/api.log')
# 读取yaml文件路路径
READ_YAML_FILE = os.path.join(BASE_DIR, 'config.yaml')
# allure测试数据路径
RESULT_FILE = os.path.join(BASE_DIR, 'result')
# allure测试报告路径
REPORT_DIR = os.path.join(BASE_DIR, 'report')
# 存储ini文件路径
INI_FILE = os.path.join(BASE_DIR, 'config.ini')
# 测试用例路径
TEST_PATH = os.path.join(BASE_DIR, 'test_case')
# 本地allure路径
# ALLURE_COMMAND = r'D:\allure\allure-2.34.1\bin\allure.bat'
# allure动态路径
ALLURE_COMMAND = allure_path


