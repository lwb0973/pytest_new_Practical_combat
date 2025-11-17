import configparser
import json
from json import JSONDecodeError
import allure
from jsonpath import jsonpath
import requests
import pytest
import settings
from common.log_handler import setup_logger
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = setup_logger()
config = configparser.ConfigParser()
config.read(settings.INI_FILE, encoding='utf-8')
sc_ip = config.get('login', 'sc_ip')



@allure.feature('【首页】-【资产发现】-【应用总数】')
class TestCase:
    @classmethod
    def setup_class(cls):
        logger.info('======== 获取首页应用总数数据，测试开始 ==========')


    @classmethod
    def teardown_class(cls):
        logger.info('======== 获取首页应用总数数据，测试结束 ==========')

    @allure.severity('normal')
    @allure.story('【首页】-【应用总数】模块')
    def test_app_summary(self, sc_login):
        """首页应用总数"""
        try:
            with allure.step('【资产】-【应用列表】接口'):
                url = f'https://{sc_ip}/apione/v2/apps/list'
                headers = {'token': sc_login}
                payload = {
                    "page_size": 10,
                    "page_num": 1,
                    "business_ip_config_ids": [],
                    "time_layout": "2006-01-02 15:04:05",
                    "risk_level_ids": [],
                    "sort_name": 1,
                    "app_group_ids": [],
                    "data_label_ids": []
                }
                response = requests.post(url, json=payload, headers=headers, verify=False)
                assert response.status_code == 200, f'接口请求失败，状态码：{response.status_code}'

                row_count = jsonpath(response.json(), '$.data.row_count')
                if not row_count:
                    logger.error("row_count 字段提取失败")
                    pytest.fail("row_count 字段为空或未提取到")
                row_count_data = row_count[0]

            with allure.step('【首页】-【应用总数】接口'):
                url = f'https://{sc_ip}/apione/v2/apps/home/summary?period=7d'
                response = requests.get(url, headers=headers, verify=False)
                assert response.status_code == 200, '首页应用总数请求响应失败'
                total_count = jsonpath(response.json(), '$.data.metric.total_count')
                if not total_count:
                    logger.error("total_count 字段提取失败")
                    pytest.fail("total_count 字段为空或未提取到")
                total_count_data = total_count[0]

            with allure.step('首页应用总数和资产应用总数对比一致'):
                assert total_count_data == row_count_data, '首页应用总数与资产应用总数不一致'

        except JSONDecodeError as e:
            logger.error(f'提取JSON解析应用总数错误: {e}')
            pytest.fail(f'提取JSON解析应用总数解析失败: {e}')
        except Exception as e:
            logger.error(f'请求数据发生异常: {e}')
            pytest.fail(f'请求异常: {e}')
