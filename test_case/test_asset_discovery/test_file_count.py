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



@allure.feature('【首页】-【资产发现】-【文件总数】')
class TestCase:
    @classmethod
    def setup_class(cls):
        logger.info('======== 获取首页文件总数数据，测试开始 ==========')


    @classmethod
    def teardown_class(cls):
        logger.info('======== 获取首页文件总数数据，测试结束 ==========')

    @allure.story('【首页】-【文件总数】模块')
    def test_file_count(self, sc_login):
        """首页文件总数"""
        try:
            with allure.step('【资产】-【文件列表】接口'):
                headers = {'token': sc_login, 'Content-Type': 'application/json'}
                url = f'https://{sc_ip}/apione/v2/file-assets'
                payload = {
                    "page_num": 1,
                    "page_size": 10,
                    "time_layout": "2006-01-02 15:04:05",
                    "sort": -1
                }
                response = requests.post(url, json=payload, headers=headers, verify=False)
                assert response.status_code == 200, f'接口请求失败，状态码：{response.status_code}'
                row_count = jsonpath(response.json(), '$.data.row_count')
                if not row_count:
                    logger.error("row_count 字段提取失败")
                    pytest.fail("row_count 字段为空或未提取到")
                row_count_data = row_count[0]

            with allure.step('【首页】-【文件总数】接口'):
                url = f'https://{sc_ip}/apione/v2/file-assets/count'
                response = requests.get(url, headers=headers, verify=False)
                assert response.status_code == 200, '首页文件总数请求响应失败'
                total_count = jsonpath(response.json(), '$.data.count')
                if not total_count:
                    logger.error("total_count 字段提取失败")
                    pytest.fail("total_count 字段为空或未提取到")
                total_count_data = total_count[0]

            with allure.step('首页文件总数和资产文件总数对比一致'):
                assert total_count_data == row_count_data, '首页文件总数与资产文件总数不一致'

        except JSONDecodeError as e:
            logger.error(f'提取 JSON 解析文件总数错误: {e}')
            pytest.fail(f'提取 JSON 解析文件总数解析失败: {e}')
        except Exception as e:
            logger.error(f'请求数据发生异常: {e}')
            pytest.fail(f'请求异常: {e}')

