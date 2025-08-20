from json import JSONDecodeError
import allure
from jsonpath import jsonpath
import requests
import pytest
import settings
from settings import var
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
        try:
            with allure.step('【资产】-【api列表】接口'):
                url = f'https://{sc_ip}/apione/v2/assets/list'
                payload = {"risk_level_ids": [2, 3, 4], "page_num": 1, "page_size": 10,
                           "time_layout": "2006-01-02 15:04:05",
                           "sort": -1}
                token = getattr(var, "token", None)
                if not token:
                    logger.error("token 获取失败")
                    pytest.fail("setup_class: 未获取到 token")
                cls.headers = {'token': token}
                response = requests.post(url, json=payload, headers=cls.headers, verify=False)
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
        logger.info('========获取首页风险概览风险api总数数据，测试结束==========')

    @allure.severity('normal')
    @allure.story('【风险api总数】')
    def test_risk_total(self):
        try:
            with allure.step('【风险api总数】接口'):
                url = f'https://{sc_ip}/apione/v2/api-assets/home/summary?period=7d'
                response = requests.request(method='GET', url=url, headers=self.headers, verify=False)
                assert response.status_code == 200, '首页风险api总数请求响应失败'
                metric = jsonpath(response.json(), '$.data.metric')[0]
                risk_high = metric.get('risk_high_count',0)
                risk_mid = metric.get('risk_mid_count',0)
                risk_low = metric.get('risk_low_count',0)
                risk_total = risk_high + risk_mid + risk_low
                assert risk_total is not False, '未获取风险api总数字段数据'
                assert self.row_count is not False, '未获取资产风险api总数字段数据'
            with allure.step(f'首页风险api总数和资产风险api总数对比一致，首页总数:{risk_total},api列表总数:{self.row_count}'):
                assert risk_total == self.row_count, '首页风险api总数与资产api列表的风险api总数不一致'

        except JSONDecodeError as e:
            logger.error(f'提取JSON解析风险api总数错误{e}')
            pytest.fail(f'提取JSON解析风险api总数解析失败: {e}')
        except Exception as e:
            logger.error(f'请求数据发生异常{e}')
            pytest.fail(f'请求异常: {e}')
