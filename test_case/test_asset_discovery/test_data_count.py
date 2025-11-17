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

@allure.feature('【首页】-【资产发现】-【流动数据总量】')
class TestCase:
    @classmethod
    def setup_class(cls):
        logger.info('========获取首页流动数据总量数据，测试开始==========')

    @classmethod
    def teardown_class(cls):
        logger.info('========获取首页流动数据总量数据，测试结束==========')

    @allure.severity('normal')
    @allure.story('【首页】-【流动数据总量】模块')
    def test_data_count(self, sc_login):
        """首页数据总量"""
        try:
            with allure.step('【资产】-【数据列表】接口'):
                url = f'https://{sc_ip}/apione/v2/data-assets'
                payload = {"page_num": 1, "page_size": 100000}
                headers = {'token': sc_login, 'Content-Type': 'application/json'}
                response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
                assert response.status_code == 200, f'接口请求失败，状态码：{response.status_code}'
                data_count_list = jsonpath(response.json(), '$.data.results[*].data_count')
                if data_count_list is False:
                    data_count = 0
                else:
                    data_count = sum(data_count_list)

            with allure.step('【首页】-【数据总量】接口'):
                url = f'https://{sc_ip}/apione/v2/data-assets/data-count'
                response = requests.request(method='GET', url=url, headers=headers, verify=False)
                assert response.status_code == 200, '首页数据总量请求响应失败'
                total_count = jsonpath(response.json(), '$.data.data_count')[0]
                assert total_count is not False, '未获取首页数据总量字段数据'
                assert data_count is not False, '未获取资产数据总量字段数据'
            with allure.step('首页数据总量和资产数据总量对比一致'):
                assert total_count == data_count, '首页数据总量与资产数据总量不一致'

        except JSONDecodeError as e:
            logger.error(f'提取JSON解析数据总量错误{e}')
            pytest.fail(f'提取JSON解析数据总量解析失败: {e}')
        except Exception as e:
            logger.error(f'请求数据发生异常{e}')
            pytest.fail(f'请求异常: {e}')
