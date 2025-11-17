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


@allure.feature('【首页】-【风险概览】-【涉敏数据量】')
class TestCase:
    @classmethod
    def setup_class(cls):
        logger.info('========获取首页风险概览涉敏数据量，测试开始==========')

    @classmethod
    def teardown_class(cls):
        logger.info('========获取首页风险概览涉敏数据量，测试结束==========')

    @allure.severity('normal')
    @allure.story('【涉敏数据量】')
    def test_data_assets(self, sc_login):
        """首页风险概览涉敏数据量"""
        try:
            headers = {'token': sc_login}
            with allure.step('【资产】-【数据列表】接口'):
                url = f'https://{sc_ip}/apione/v2/data-assets'
                payload = {"page_num": 1, "page_size": 10000, "sensitive_level": [2, 3, 4]}
                response = requests.post(url, json=payload, headers=headers, verify=False)
                assert response.status_code == 200, f'接口请求失败，状态码：{response.status_code}'
                data_count_list = jsonpath(response.json(), '$.data.results[*].data_count')
                data_count = sum(data_count_list) if data_count_list else 0

            with allure.step('【涉敏数据量】接口'):
                url = f'https://{sc_ip}/apione/v2/data-assets/data-count'
                response = requests.get(url, headers=headers, verify=False)
                assert response.status_code == 200, '首页涉敏数据量请求响应失败'
                sens_count = jsonpath(response.json(), '$.data.sens_data_count')
                assert sens_count, '未获取涉敏数据量字段数据'
                sens_count = sens_count[0]

            with allure.step('首页涉敏数据量和资产-数据列表涉敏数据量对比一致'):
                assert sens_count == data_count, (
                    f'首页涉敏数据量({sens_count})与数据列表涉敏数据量({data_count})不一致'
                )

        except JSONDecodeError as e:
            logger.error(f'提取JSON解析涉敏数据量错误: {e}')
            pytest.fail(f'提取JSON解析涉敏数据量解析失败: {e}')
        except Exception as e:
            logger.error(f'请求数据发生异常: {e}')
            pytest.fail(f'请求异常: {e}')
