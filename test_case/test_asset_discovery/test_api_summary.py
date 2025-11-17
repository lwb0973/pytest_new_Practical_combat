import json
from json import JSONDecodeError
import allure
from jsonpath import jsonpath
import requests
import pytest
import settings
from common.log_handler import setup_logger
import urllib3
import configparser

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = setup_logger()
config = configparser.ConfigParser()
config.read(settings.INI_FILE, encoding='utf-8')
sc_ip = config.get('login', 'sc_ip')

@allure.feature('【首页】-【资产发现】-【api总数】')
class TestCase:
    @classmethod
    def setup_class(cls):
        logger.info("======== 获取首页 API 总数数据，测试开始 ==========")


    @classmethod
    def teardown_class(cls):
        logger.info("======== 获取首页 API 总数数据，测试结束 ==========")

    @allure.story("【首页】-【API 总数】模块")
    def test_api_summary(self, sc_login):
        """首页API总数"""
        try:
            # Step 1: 获取资产 API 列表
            with allure.step("【资产】-【API 列表】接口"):
                url = f"https://{sc_ip}/apione/v2/assets/list"
                payload = {"page_num": 1, "page_size": 10, "time_layout": "2006-01-02 15:04:05", "sort": -1}
                headers = {"token": sc_login, "Content-Type": "application/json"}
                response = requests.post(url, json=payload, headers=headers, verify=False)
                assert response.status_code == 200, f"接口请求失败，状态码：{response.status_code}"
                row_count_data = jsonpath(response.json(), "$.data.row_count")[0]

            # Step 2: 获取首页 API 总数
            with allure.step("【首页】-【API 总数】接口"):
                url = f"https://{sc_ip}/apione/v2/api-assets/home/summary?period=7d"
                response = requests.get(url, headers=headers, verify=False)
                assert response.status_code == 200, "首页 API 总数请求响应失败"
                total_count = jsonpath(response.json(), "$.data.metric.total_count")[0]

            # Step 3: 比较两个接口的 API 总数
            with allure.step("对比首页 API 总数与资产 API 总数是否一致"):
                assert total_count == row_count_data, "首页 API 总数与资产 API 总数不一致"

        except JSONDecodeError as e:
            logger.error(f"JSON 解析错误: {e}")
            pytest.fail(f"JSON 解析失败: {e}")

        except Exception as e:
            logger.error(f"请求发生异常: {e}")
            pytest.fail(f"请求异常: {e}")
