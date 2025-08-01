import configparser
import json
from json import JSONDecodeError
import allure
from jsonpath import jsonpath
import requests
import pytest
import settings
from settings import var
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
        logger.info('========获取首页应用总数数据，测试开始==========')
        try:
            with allure.step('【资产】-【应用列表】接口'):
                url = f'https://{sc_ip}/apione/v2/apps/list'
                payload = {
                    "page_size": 10, "page_num": 1,
                    "business_ip_config_ids": [], "time_layout": "2006-01-02 15:04:05",
                    "risk_level_ids": [], "sort_name": 1,
                    "app_group_ids": [], "data_label_ids": []
                }
                token = getattr(var, "token", None)
                if not token:
                    logger.error("token 获取失败")
                    pytest.fail("setup_class: 未获取到 token")
                cls.headers = {'token': token}
                response = requests.post(url, data=json.dumps(payload), headers=cls.headers, verify=False)
                assert response.status_code == 200, f'接口请求失败，状态码：{response.status_code}'
                row_count = jsonpath(response.json(), '$.data.row_count')
                if not row_count:
                    logger.error("row_count 字段提取失败")
                    pytest.fail("setup_class: row_count 字段为空或未提取到")

                cls.row_count = row_count[0]
        except Exception as e:
            logger.error(f'setup_class 异常: {e}', exc_info=True)
            pytest.fail(f'setup_class 执行失败: {e}')

    @classmethod
    def teardown_class(cls):
        logger.info('========获取首页应用总数数据，测试结束==========')

    @allure.severity('normal')
    @allure.story('【首页】-【应用总数】模块')
    def test_app_summary(self):
        try:
            with allure.step('【首页】-【应用总数】接口'):
                url = f'https://{sc_ip}/apione/v2/apps/home/summary?period=7d'
                response = requests.request(method='GET', url=url, headers=self.headers, verify=False)
                assert response.status_code == 200, '首页应用总数请求响应失败'
                total_count = jsonpath(response.json(), '$.data.metric.total_count')[0]
                assert total_count is not False, '未获取首页应用总数字段数据'
                assert self.row_count is not False, '未获取资产应用总数字段数据'
            with allure.step('首页应用总数和资产应用总数对比一致'):
                assert total_count == self.row_count, '首页应用总数与资产应用总数不一致'

        except JSONDecodeError as e:
            logger.error(f'提取JSON解析应用总数错误{e}')
            pytest.fail(f'提取JSON解析应用总数解析失败: {e}')
        except Exception as e:
            logger.error(f'请求数据发生异常{e}')
            pytest.fail(f'请求异常: {e}')

