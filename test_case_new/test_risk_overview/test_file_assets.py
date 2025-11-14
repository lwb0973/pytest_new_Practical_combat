from json import JSONDecodeError
import allure
from jsonpath import jsonpath
import requests
import pytest
import settings
from settings import var
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
        try:
            with allure.step('【资产】-【文件列表】接口'):
                url = f'https://{sc_ip}/apione/v2/file-assets'
                payload ={"page_num":1,"page_size":10,"time_layout":"2006-01-02 15:04:05","sort":-1,"sens_level_ids":[2,3,4]}
                token = getattr(var, "token", None)
                if not token:
                    logger.error("token 获取失败")
                    pytest.fail("setup_class: 未获取到 token")
                cls.headers = {'token': token}
                response = requests.post(url, json=payload, headers=cls.headers, verify=False)
                assert response.status_code == 200, f'接口请求失败，状态码：{response.status_code}'
                file_row_count = jsonpath(response.json(), '$.data.row_count')
                if not file_row_count:
                    logger.error("row_count 字段提取失败")
                    pytest.fail("setup_class: row_count 字段为空或未提取到")
                cls.file_row_count = file_row_count[0]
        except Exception as e:
            logger.error(f'setup_class 异常: {e}', exc_info=True)
            pytest.fail(f'setup_class 执行失败: {e}')

    @classmethod
    def teardown_class(cls):
        logger.info('========获取首页风险概览敏感文件总数数据，测试结束==========')

    @allure.severity('normal')
    @allure.story('【敏感文件总数】')
    def test_file_assets(self):
        try:
            with allure.step('【敏感文件总数】接口'):
                url = f'https://{sc_ip}/apione/v2/file-assets/count'
                response = requests.request(method='GET', url=url, headers=self.headers, verify=False)
                assert response.status_code == 200, '首页敏感文件总数请求响应失败'
                sens_count = jsonpath(response.json(), '$.data.sens_count')[0]
                assert sens_count is not False, '未获取敏感文件总数字段数据'
                assert self.file_row_count is not False, '未获取文件列表敏感文件总数字段数据'
            with allure.step(f'首页敏感文件总数和用户-文件列表敏感文件总数对比一致，首页总数:{sens_count},文件列表总数:{self.file_row_count}'):
                assert sens_count == self.file_row_count, '首页敏感文件总数与文件列表的敏感文件总数不一致'

        except JSONDecodeError as e:
            logger.error(f'提取JSON解析敏感文件总数错误{e}')
            pytest.fail(f'提取JSON解析敏感文件总数解析失败: {e}')
        except Exception as e:
            logger.error(f'请求数据发生异常{e}')
            pytest.fail(f'请求异常: {e}')
