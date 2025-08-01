from json import JSONDecodeError
import allure
import requests
import pytest
import settings
from settings import var
from common.log_handler import setup_logger
import urllib3
from ..test_risk_distribution.risk_all import risk_api_list,home_risk_api
import configparser

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = setup_logger()

config = configparser.ConfigParser()
config.read(settings.INI_FILE, encoding='utf-8')
sc_ip = config.get('login', 'sc_ip')



@allure.feature('【首页】-【风险api分布饼图】-【高风险api总数】')
class TestCase:
    @classmethod
    def setup_class(cls):
        logger.info('========获取首页风险api分布饼图高风险api总数数据，测试开始==========')
        try:
            with allure.step('【资产】-【api列表】接口'):
                payload ={"page_num":1,"page_size":10,"sort":-1,"time_layout":"2006-01-02 15:04:05","risk_level_ids":[4]}
                token = getattr(var, "token", None)
                if not token:
                    logger.error("token 获取失败")
                    pytest.fail("setup_class: 未获取到 token")
                cls.headers = {'token': token}
                cls.high_row_count = risk_api_list(sc_url=sc_ip,headers=cls.headers,payload=payload)
        except Exception as e:
            logger.error(f'setup_class 异常: {e}', exc_info=True)
            pytest.fail(f'setup_class 执行失败: {e}')

    @classmethod
    def teardown_class(cls):
        logger.info('========获取首页风险api分布饼图高风险api总数数据，测试结束==========')

    @allure.severity('normal')
    @allure.story('【高风险api总数】')
    def test_risk_high(self):
        try:
            with allure.step('【高风险api总数】接口'):
                risk_high_count = home_risk_api(sc_url=sc_ip,headers=self.headers,all_risk_count='risk_high_count',risk_name='高危风险')
                assert risk_high_count is not False, '未获取高风险api总数字段数据'
                assert self.high_row_count is not False, '未获取api列表高风险api总数字段数据'
            with allure.step('首页高风险api总数和资产-api列表高风险api总数对比一致'):
                assert risk_high_count == self.high_row_count, '首页高风险api总数与api列表的高风险api总数不一致'
        except JSONDecodeError as e:
            logger.error(f'提取JSON解析高风险api总数错误{e}')
            pytest.fail(f'提取JSON解析高风险api总数解析失败: {e}')
        except Exception as e:
            logger.error(f'请求数据发生异常{e}')
            pytest.fail(f'请求异常: {e}')
