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


@allure.feature('【首页】-【风险概览】-【风险用户总数】')
class TestCase:
    @classmethod
    def setup_class(cls):
        logger.info('========获取首页风险概览风险用户总数数据，测试开始==========')


    @classmethod
    def teardown_class(cls):
        logger.info('========获取首页风险概览风险用户总数数据，测试结束==========')

    @allure.story('【风险用户总数】')
    def test_risk_users(self, sc_login):
        """首页风险概览风险用户总数"""
        try:
            headers = {'token': sc_login}
            with allure.step('【用户】-【用户列表】接口'):
                url = f'https://{sc_ip}/apione/v2/users/list'
                payload = {"page_num": 1, "page_size": 10, "risk_levels": [2, 3, 4]}
                response = requests.post(url, json=payload, headers=headers, verify=False)
                assert response.status_code == 200, f'接口请求失败，状态码：{response.status_code}'

                user_row_count_list = jsonpath(response.json(), '$.data.row_count')
                if not user_row_count_list:
                    logger.error("row_count 字段提取失败或为空")
                    pytest.fail("setup_class: row_count 字段为空或未提取到")
                user_row_count = user_row_count_list[0]

            with allure.step('【风险用户总数】接口'):
                url = f'https://{sc_ip}/apione/v2/users/metrics'
                response = requests.get(url, headers=headers, verify=False)
                assert response.status_code == 200, '首页风险用户总数请求响应失败'

                metric_list = jsonpath(response.json(), '$.data.metric')
                if not metric_list:
                    logger.error("metric 字段提取失败或为空")
                    pytest.fail("未获取风险用户总数字段数据")
                metric = metric_list[0]

                user_risk_low = metric.get('risk_low_count', 0)
                user_risk_mid = metric.get('risk_mid_count', 0)
                user_risk_high = metric.get('risk_high_count', 0)
                user_risk_total = user_risk_low + user_risk_mid + user_risk_high

            with allure.step('首页风险用户总数与用户列表总数对比一致'):
                assert user_risk_total == user_row_count, (
                    f'首页风险用户总数({user_risk_total})与用户列表总数({user_row_count})不一致'
                )

        except JSONDecodeError as e:
            logger.error(f'提取JSON解析风险用户总数错误: {e}')
            pytest.fail(f'提取JSON解析风险用户总数解析失败: {e}')
        except Exception as e:
            logger.error(f'请求数据发生异常: {e}')
            pytest.fail(f'请求异常: {e}')
