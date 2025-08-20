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


@allure.feature('【首页】-【风险api分布饼图】-【中危弱点api总数】')
class TestCase:
    @classmethod
    def setup_class(cls):
        logger.info('========获取首页风险api分布饼图中危弱点api总数数据，测试开始==========')
        try:
            with allure.step('【资产】-【api列表】接口'):
                url = f'https://{sc_ip}/apione/v2/assets/list'
                payload = {"vul_level_ids": [3], "page_num": 1, "page_size": 10, "time_layout": "2006-01-02 15:04:05",
                           "sort": -1}
                token = getattr(var, "token", None)
                if not token:
                    logger.error("token 获取失败")
                    pytest.fail("setup_class: 未获取到 token")
                cls.headers = {'token': token}
                response = requests.post(url, json=payload, headers=cls.headers, verify=False)
                assert response.status_code == 200, f'接口请求失败，状态码：{response.status_code}'
                mid_row_count = jsonpath(response.json(), '$.data.row_count')
                if not mid_row_count:
                    logger.error("row_count 字段提取失败")
                    pytest.fail("setup_class: row_count 字段为空或未提取到")
                cls.mid_row_count = mid_row_count[0]
        except Exception as e:
            logger.error(f'setup_class 异常: {e}', exc_info=True)
            pytest.fail(f'setup_class 执行失败: {e}')

    @classmethod
    def teardown_class(cls):
        logger.info('========获取首页风险api分布饼图中危弱点api总数数据，测试结束==========')

    @allure.severity('normal')
    @allure.story('【中危弱点api总数】')
    def test_vul_mid(self):
        try:
            with allure.step('【中危弱点api总数】接口'):
                url = f'https://{sc_ip}/apione/v2/api-assets/home/summary?period=7d'
                response = requests.request(method='GET', url=url, headers=self.headers, verify=False)
                assert response.status_code == 200, '首页中危弱点api总数请求响应失败'
                risk_mid_count = jsonpath(response.json(), '$.data.metric.vul_mid_count')[0]
                assert risk_mid_count is not False, '未获取中危弱点api总数字段数据'
                assert self.mid_row_count is not False, '未获取api列表中危弱点api总数字段数据'
            with allure.step(f'首页中危弱点api总数和资产-api列表中危弱点api总数对比一致,首页总数:{risk_mid_count},api列表总数:{self.mid_row_count}'):
                assert risk_mid_count == self.mid_row_count, '首页中危弱点api总数与api列表的中危弱点api总数不一致'

        except JSONDecodeError as e:
            logger.error(f'提取JSON解析中危弱点api总数错误{e}')
            pytest.fail(f'提取JSON解析中危弱点api总数解析失败: {e}')
        except Exception as e:
            logger.error(f'请求数据发生异常{e}')
            pytest.fail(f'请求异常: {e}')
