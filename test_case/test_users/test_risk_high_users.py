import allure
import pytest
import settings
from common.log_handler import setup_logger
import urllib3
import configparser
from test_case.test_users.users_list_risk import users_list_risk
from test_case.test_users.home_user_risk import home_user_risk

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = setup_logger()
config = configparser.ConfigParser()
config.read(settings.INI_FILE, encoding='utf-8')
sc_ip = config.get('login', 'sc_ip')



@allure.feature('【首页】-【用户分析】-【高风险用户总数】')
class TestCase:
    @classmethod
    def setup_class(cls):
        logger.info('========获取首页用户分析高风险用户总数，测试开始==========')

    @classmethod
    def teardown_class(cls):
        logger.info('========获取首页高风险用户分析用户总数，测试结束==========')

    @allure.severity('normal')
    @allure.story('【高风险用户数总量】')
    def test_risk_high_user(self, sc_login):
        """
        首页用户分析高风险用户总数
        :param sc_login:
        :return:
        """

        headers = {'token': sc_login}
        with allure.step('【用户列表】-【高风险用户总数】接口'):
            users_count_list = users_list_risk(sc_ip, headers,risk=4)

        with allure.step('【高风险用户总数】接口'):
            users_counts = home_user_risk(sc_ip, headers, "risk_high_count")

        with allure.step('首页高风险用户总数和用户列表-高风险用户总数对比一致'):
            assert users_counts == users_count_list, (
                f'首页高风险用户总数({users_counts})与用户列表高风险用户总数({users_count_list})不一致'
            )


