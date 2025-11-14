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


@allure.feature('【首页】-【风险概览】-【涉敏数据量】')
class TestCase:
    @classmethod
    def setup_class(cls):
        logger.info('========获取首页风险概览涉敏数据量，测试开始==========')
        try:
            with allure.step('【资产】-【数据列表】接口'):
                url = f'https://{sc_ip}/apione/v2/data-assets'
                payload ={"page_num":1,"page_size":10000,"sensitive_level":[2,3,4]}
                token = getattr(var, "token", None)
                if not token:
                    logger.error("token 获取失败")
                    pytest.fail("setup_class: 未获取到 token")
                cls.headers = {'token': token}
                response = requests.post(url, json=payload, headers=cls.headers, verify=False)
                assert response.status_code == 200, f'接口请求失败，状态码：{response.status_code}'
                data_count_list = jsonpath(response.json(), '$.data.results[*].data_count')
                if not data_count_list:
                    data_count = 0
                else:
                    data_count = sum(data_count_list)
                cls.data_count = data_count
        except Exception as e:
            logger.error(f'setup_class 异常: {e}', exc_info=True)
            pytest.fail(f'setup_class 执行失败: {e}')

    @classmethod
    def teardown_class(cls):
        logger.info('========获取首页风险概览涉敏数据量，测试结束==========')

    @allure.severity('normal')
    @allure.story('【涉敏数据量】')
    def test_data_assets(self):
        try:
            with allure.step('【涉敏数据量】接口'):
                url = f'https://{sc_ip}/apione/v2/data-assets/data-count'
                response = requests.request(method='GET', url=url, headers=self.headers, verify=False)
                assert response.status_code == 200, '首页涉敏数据量请求响应失败'
                sens_count = jsonpath(response.json(), '$.data.sens_data_count')[0]
                assert sens_count is not False, '未获取涉敏数据量字段数据'
                assert self.data_count is not False, '未获取数据列表涉敏数据量字段数据'
            with allure.step(f'首页涉敏数据量和资产-数据列表涉敏数据量对比一致,首页总数:{sens_count},数据列表总数:{self.data_count}'):
                assert sens_count == self.data_count, '首页涉敏数据量与数据列表的涉敏数据量不一致'
        except JSONDecodeError as e:
            logger.error(f'提取JSON解析涉敏数据量错误{e}')
            pytest.fail(f'提取JSON解析涉敏数据量解析失败: {e}')
        except Exception as e:
            logger.error(f'请求数据发生异常{e}')
            pytest.fail(f'请求异常: {e}')
