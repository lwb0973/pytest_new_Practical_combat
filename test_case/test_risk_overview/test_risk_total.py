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


@allure.feature('【首页】-【风险概览】-【风险api总数】')
class TestCase:
    @classmethod
    def setup_class(cls):
        logger.info('========获取首页风险概览风险api总数数据，测试开始==========')


    @classmethod
    def teardown_class(cls):
        logger.info('========获取首页风险概览风险api总数数据，测试结束==========')

    @allure.severity('normal')
    @allure.story('【风险api总数】')
    def test_risk_total(self, sc_login):
        """首页风险概览风险api总数"""
        try:
            headers = {'token': sc_login}
            with allure.step('【资产】-【api列表】接口'):
                url = f'https://{sc_ip}/apione/v2/assets/list'
                payload = {
                    "risk_level_ids": [2, 3, 4],
                    "page_num": 1,
                    "page_size": 10,
                    "time_layout": "2006-01-02 15:04:05",
                    "sort": -1
                }
                response = requests.post(url, json=payload, headers=headers, verify=False)
                assert response.status_code == 200, f'接口请求失败，状态码：{response.status_code}'

                row_count_list = jsonpath(response.json(), '$.data.row_count')
                if not row_count_list:
                    logger.error("未提取到 row_count 字段或其值为空")
                    pytest.fail("setup_class: row_count 字段为空或未提取到")
                row_count = row_count_list[0]

            with allure.step('【风险api总数】接口'):
                url = f'https://{sc_ip}/apione/v2/api-assets/home/summary?period=7d'
                response = requests.get(url, headers=headers, verify=False)
                assert response.status_code == 200, '首页风险api总数请求响应失败'

                metric_list = jsonpath(response.json(), '$.data.metric')
                if not metric_list:
                    logger.error("未获取到 metric 字段或其值为空")
                    pytest.fail("未获取风险api总数字段数据")
                metric = metric_list[0]

                risk_high = metric.get('risk_high_count', 0)
                risk_mid = metric.get('risk_mid_count', 0)
                risk_low = metric.get('risk_low_count', 0)
                risk_total = risk_high + risk_mid + risk_low

            with allure.step('首页风险api总数与资产api列表风险api总数对比一致'):
                assert risk_total == row_count, (
                    f'首页风险api总数({risk_total})与资产api列表风险api总数({row_count})不一致'
                )

        except JSONDecodeError as e:
            logger.error(f'提取JSON解析风险api总数错误: {e}')
            pytest.fail(f'提取JSON解析风险api总数解析失败: {e}')
        except Exception as e:
            logger.error(f'请求数据发生异常: {e}')
            pytest.fail(f'请求异常: {e}')
