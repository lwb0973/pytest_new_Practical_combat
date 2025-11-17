from json import JSONDecodeError
import allure
from jsonpath import jsonpath
import requests
import pytest
import settings
from common.log_handler import setup_logger
import configparser
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = setup_logger()
config = configparser.ConfigParser()
config.read(settings.INI_FILE, encoding='utf-8')
sc_ip = config.get('login', 'sc_ip')


@allure.feature('【首页】-【风险概览】-【敏感文件总数】')
class TestCase:
    @classmethod
    def setup_class(cls):
        logger.info('========获取首页风险概览敏感文件总数数据，测试开始==========')


    @classmethod
    def teardown_class(cls):
        logger.info('========获取首页风险概览敏感文件总数数据，测试结束==========')

    @allure.story('【敏感文件总数】')
    def test_file_assets(self, sc_login):
        """首页风险概览敏感文件总数"""
        try:
            headers = {'token': sc_login}
            with allure.step('【资产】-【文件列表】接口'):
                url = f'https://{sc_ip}/apione/v2/file-assets'
                payload = {
                    "page_num": 1,
                    "page_size": 10,
                    "time_layout": "2006-01-02 15:04:05",
                    "sort": -1,
                    "sens_level_ids": [2, 3, 4]
                }

                response = requests.post(url, json=payload, headers=headers, verify=False)
                assert response.status_code == 200, f'接口请求失败，状态码：{response.status_code}'

                file_row_count_list = jsonpath(response.json(), '$.data.row_count')
                if not file_row_count_list:
                    logger.error("未提取到 row_count 字段或其值为空")
                    pytest.fail("setup_class: row_count 字段为空或未提取到")
                file_row_count = file_row_count_list[0]

            with allure.step('【敏感文件总数】接口'):
                url = f'https://{sc_ip}/apione/v2/file-assets/count'
                response = requests.get(url, headers=headers, verify=False)
                assert response.status_code == 200, '首页敏感文件总数请求响应失败'

                sens_count_list = jsonpath(response.json(), '$.data.sens_count')
                if not sens_count_list:
                    logger.error("未获取到 sens_count 字段或其值为空")
                    pytest.fail("未获取到敏感文件总数字段数据")
                sens_count = sens_count_list[0]

            with allure.step('首页敏感文件总数和用户-文件列表敏感文件总数对比一致'):
                assert sens_count == file_row_count, \
                    f'首页敏感文件总数({sens_count})与文件列表敏感文件总数({file_row_count})不一致'

        except JSONDecodeError as e:
            logger.error(f'提取JSON解析敏感文件总数错误: {e}')
            pytest.fail(f'提取JSON解析敏感文件总数解析失败: {e}')
        except Exception as e:
            logger.error(f'请求数据发生异常: {e}')
            pytest.fail(f'请求异常: {e}')
