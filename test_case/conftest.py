import pytest
import requests
from jsonpath import jsonpath
import json
import settings
import datetime
import os
import configparser
from common.base64_handler import get_login_captcha_info,recognize_captcha_from_base64,rsa_encrypt
from common.crypto_md5 import md5enc
import getpass
import socket
import platform
import sys
import subprocess

# 读取ini配置文件
config = configparser.ConfigParser()
config.read(settings.INI_FILE, encoding='utf-8')
sc_ip = config.get('login', 'sc_ip')
username = config.get('login','username')
password = config.get('login','password')
# 登录接口获取token
@pytest.fixture(scope="session")
def sc_login():
    """
    获取 token
    :param sc_ip:
    :return:
    """
    res = requests.get("https://{}/api/v1.2/randString".format(sc_ip), verify=False)
    rand_str = res.json().get('data').get('rand')
    captcha_base64, captcha_id = get_login_captcha_info(sc_ip)
    captcha_code = recognize_captcha_from_base64(captcha_base64)
    info = ''
    if rand_str:
        temp_str = {
            "username": username,
            "password": md5enc(password),
            "uuid": rand_str,
            "captcha": captcha_code,
            "captchaId": captcha_id
        }
        info = rsa_encrypt(json.dumps(temp_str))
    info = {"info": info}
    res = requests.post(url='https://{}/api/v1.2/login'.format(sc_ip), json=info, verify=False).json()
    return res['data']['token']



def get_git_branch():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL  # 抑制错误输出，防止报错
        ).decode().strip()
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        return None


def get_environment_info():
    """
    自动获取环境信息内容
    :return:
    """
    # 如果是 GitLab CI
    if os.getenv("CI_PROJECT_NAME"):
        return f"GitLab CI: {os.getenv('CI_PROJECT_NAME')} | Branch: {os.getenv('CI_COMMIT_BRANCH')} | User: {os.getenv('GITLAB_USER_NAME')}"

    # 如果是 GitHub Actions
    elif os.getenv("GITHUB_REPOSITORY"):
        return f"GitHub Actions: {os.getenv('GITHUB_REPOSITORY')} | Branch: {os.getenv('GITHUB_REF_NAME')} | Actor: {os.getenv('GITHUB_ACTOR')}"

    # 本地 Git 项目
    elif get_git_branch():
        return f"Local Git | Branch: {get_git_branch()} | User: {getpass.getuser()}@{socket.gethostname()}"

    # 非 Git、本地运行
    else:
        return f"{getpass.getuser()}@{socket.gethostname()} | {platform.system()} {platform.release()} | Python {sys.version.split()[0]}"


def to_unicode_escape(s: str) -> str:
    """
    allure测试报告环境信息转换格式显示中文
    :param s:
    :return:
    """
    return s.encode("unicode_escape").decode("ascii")


# allure测试报告配置信息
def write_allure_metadata():
    os.makedirs(settings.RESULT_FILE, exist_ok=True)
    env_info = get_environment_info()

    # 写 environment.properties
    env_path = os.path.join(settings.RESULT_FILE, "environment.properties")
    with open(env_path, "w", encoding="ascii") as f:
        f.write(f"project={to_unicode_escape('首页项目')}\n")
        f.write(f"environment={to_unicode_escape(env_info)}\n")
        f.write(f"datetime={to_unicode_escape(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\n")

    # 写 executor.json（设置标题）
    executor_path = os.path.join(settings.RESULT_FILE, "executor.json")
    executor_data = {
        "name": "卢炜飚",
        "type": "local",
        "reportName": "首页功能测试报告",
        "buildName": f"构建时间 {datetime.datetime.now().strftime('%Y-%m-%d')}",
        "buildUrl": "",
        "reportUrl": ""
    }
    with open(executor_path, "w", encoding="utf-8") as f:
        json.dump(executor_data, f, indent=4, ensure_ascii=False)

    print(f"[DEBUG] Allure metadata 已写入至：{env_path}, {executor_path}")


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    """测试运行结束后自动生成 Allure metadata"""
    write_allure_metadata()



# def get_git_branch():
#     try:
#         return subprocess.check_output(
#             ["git", "rev-parse", "--abbrev-ref", "HEAD"]
#         ).decode().strip()
#     except Exception:
#         return None
#
# def get_environment_info():
#     """
#     自动获取环境信息内容
#     :return:
#     """
#     # 如果是 GitLab CI
#     if os.getenv("CI_PROJECT_NAME"):
#         return f"GitLab CI: {os.getenv('CI_PROJECT_NAME')} | Branch: {os.getenv('CI_COMMIT_BRANCH')} | User: {os.getenv('GITLAB_USER_NAME')}"
#     # 如果是 GitHub Actions
#     elif os.getenv("GITHUB_REPOSITORY"):
#         return f"GitHub Actions: {os.getenv('GITHUB_REPOSITORY')} | Branch: {os.getenv('GITHUB_REF_NAME')} | Actor: {os.getenv('GITHUB_ACTOR')}"
#     # 本地 Git 项目
#     elif get_git_branch():
#         return f"Local Git | Branch: {get_git_branch()} | User: {getpass.getuser()}@{socket.gethostname()}"
#     # 非 Git、本地运行
#     else:
#         return f"{getpass.getuser()}@{socket.gethostname()} | {platform.system()} {platform.release()} | Python {sys.version.split()[0]}"
#
#
# def to_unicode_escape(s: str) -> str:
#     """
#     allure测试报告环境信息转换格式显示中文
#     :param s:
#     :return:
#     """
#     return s.encode("unicode_escape").decode("ascii")
# # allure测试报告配置信息
# def write_allure_metadata():
#     os.makedirs(settings.RESULT_FILE, exist_ok=True)
#     env_info = get_environment_info()
#     # 写 environment.properties
#     env_path = os.path.join(settings.RESULT_FILE, "environment.properties")
#     with open(env_path, "w", encoding="ascii") as f:
#         f.write(f"project={to_unicode_escape('首页项目')}\n")
#         f.write(f"environment={to_unicode_escape(env_info)}\n")
#         f.write(f"datetime={to_unicode_escape(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\n")
#
#     # 写 executor.json（设置标题）
#     executor_path = os.path.join(settings.RESULT_FILE, "executor.json")
#     executor_data = {
#         "name": "卢炜飚",
#         "type": "local",
#         "reportName": "首页功能测试报告",
#         "buildName": f"构建时间 {datetime.datetime.now().strftime('%Y-%m-%d')}",
#         "buildUrl": "",
#         "reportUrl": ""
#     }
#     with open(executor_path, "w", encoding="utf-8") as f:
#         json.dump(executor_data, f, indent=4, ensure_ascii=False)
#
#     print(f"[DEBUG] Allure metadata 已写入至：{env_path}, {executor_path}")
#
#
# @pytest.hookimpl(tryfirst=True)
# def pytest_sessionfinish(session, exitstatus):
#     """测试运行结束后自动生成 Allure metadata"""
#     write_allure_metadata()


#
# def pytest_collection_modifyitems(items):
#     """
#     自定义模块和模块内文件顺序
#     """
#     module_order = {
#         "test_pending_risk_event": ["test_risk_high.py", "test_risk_low.py", "test_risk_mid.py"],
#         "test_pending_vul_event": ["test_vul_high.py", "test_vul_low.py", "test_vul_mid.py"],
#         "test_risk_overview": ["test_risk_total.py", "test_vul_total.py", "test_risk_users.py", "test_risk_user.py", "test_file_assets.py", "test_data_assets.py"],
#         "test_asset_discovery": ["test_app_summary.py", "test_api_summary.py", "test_file_count.py", "test_data_count.py"],
#         "test_risk_distribution": ["test_risk_high.py", "test_risk_low.py", "test_risk_mid.py"],
#         "test_vul_distribution": ["test_vul_high.py", "test_vul_low.py", "test_vul_mid.py"]
#     }
#
#     def get_sort_key(item):
#         nodeid = item.nodeid.replace("\\", "/")  # 兼容 Windows 路径
#         for module_index, (module, file_list) in enumerate(module_order.items()):
#             if f"/{module}/" in nodeid:
#                 for file_index, filename in enumerate(file_list):
#                     if f"/{module}/{filename}" in nodeid:
#                         return (module_index, file_index, nodeid)
#                 return (module_index, len(file_list), nodeid)  # 未在文件列表中，排最后
#         return (len(module_order), 0, nodeid)  # 未在模块列表中，整体排最后
#
#     items.sort(key=get_sort_key)
#
#     print("\n[DEBUG] 自定义执行顺序:")
#     for i, item in enumerate(items, 1):
#         print(f"{i}. {item.nodeid}")
