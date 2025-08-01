import allure
from jsonpath import jsonpath
import requests
import pytest
import settings
from settings import var
from common.log_handler import setup_logger
import urllib3
import configparser
from ..test_pending_vul_event.vul_all_pending import vul_list_all_pending,vul_home_all_pending
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = setup_logger()

config = configparser.ConfigParser()
config.read(settings.INI_FILE, encoding='utf-8')
sc_ip = config.get('login', 'sc_ip')


@allure.feature('【首页】-【待处置事件】-【高危弱点待处置/已处置饼图】')
class TestCase:
    @classmethod
    def setup_class(cls):
        logger.info('========获取首页待处置事件高危弱点待处置/已处置饼图，测试开始==========')
        try:
            with allure.step('【弱点】-【弱点事件列表】接口'):
                token = getattr(var, "token", None)
                if not token:
                    logger.error("token 获取失败")
                    pytest.fail("setup_class: 未获取到 token")
                cls.headers = {'token': token}
                cls.base_url  = vul_list_all_pending(sc_url=sc_ip,headers=cls.headers, vul_level='4')
                logger.info(f'获取到弱点列表高危待处置数量：{cls.base_url["pending_total_count"]}，已处置数量：{cls.base_url["total_count"]}')
        except Exception as e:
            logger.error(f'setup_class 异常: {e}', exc_info=True)
            pytest.fail(f'setup_class 执行失败: {e}')

    @classmethod
    def teardown_class(cls):
        logger.info('========获取首页待处置事件高危弱点待处置/已处置饼图，测试结束==========')

    @allure.severity('normal')
    @allure.story('【待处置高危弱点总数】')
    def test_vul_high_pending(self):
        try:
            with allure.step('【待处置高危弱点总数】接口'):
                home_base_url = vul_home_all_pending(sc_url=sc_ip,headers=self.headers,vul_level='4',vul_grade="高危弱点")
                # 校验 setup_class 中保存的数据
                assert self.base_url["pending_total_count"] is not False, '弱点列表待处置高危弱点事件总数未获取'
                assert self.base_url["total_count"] is not False, '弱点列表高危弱点事件总数未获取'

            with allure.step('校验待处置数一致'):
                assert home_base_url["pending_count"] == self.base_url["pending_total_count"], \
                    f'待处置数不一致：首页待处置高危弱点为 {home_base_url["pending_count"]}，弱点列表待处置高危弱点为 {self.base_url["pending_total_count"]}'

            with allure.step('校验已处置数一致'):
                assert home_base_url["done_count"] == self.base_url["total_count"], \
                    f'已处置数不一致：首页已处置高危弱点为 {home_base_url["done_count"]}，弱点列表已处置高危弱点为 {self.base_url["total_count"]}'

        except Exception as e:
            logger.error(f'test_risk_high_pending 异常: {e}', exc_info=True)
            pytest.fail(f'测试失败：{e}')
