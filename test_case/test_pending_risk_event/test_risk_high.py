import allure
import pytest
import settings
from common.log_handler import setup_logger
import urllib3
import configparser
from test_case.test_pending_risk_event.risk_all_pending import risk_list_all_pending,risk_home_all_pending
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = setup_logger()

config = configparser.ConfigParser()
config.read(settings.INI_FILE, encoding='utf-8')
sc_ip = config.get('login', 'sc_ip')


@allure.feature('【首页】-【待处置事件】-【高危风险待处置/已处置饼图】')
class TestCase:
    @classmethod
    def setup_class(cls):
        logger.info('======== 获取首页待处置事件高危风险待处置/已处置饼图，测试开始 ==========')

    @classmethod
    def teardown_class(cls):
        logger.info('======== 获取首页待处置事件高危风险待处置/已处置饼图，测试结束 ==========')

    @allure.story('【待处置高危风险总数】')
    def test_risk_high_pending(self, sc_login):
        """待处置/已处置高危风险事件饼图总数"""
        try:
            with allure.step('【风险】-【风险事件列表】接口'):
                headers = {'token': sc_login}
                risk_data = risk_list_all_pending(
                    sc_url=sc_ip,
                    headers=headers,
                    risk_level='4'  # 高危风险等级
                )
                pending_total = risk_data.get("pending_total_count")
                total_count = risk_data.get("total_count")
                logger.info(f"获取风险列表高危待处置数量：{pending_total}，已处置数量：{total_count}")

                assert pending_total is not None, "风险列表待处置高危风险事件总数未获取"
                assert total_count is not None, "风险列表高危风险事件总数未获取"

            with allure.step('【待处置高危风险总数】接口'):
                home_data = risk_home_all_pending(
                    sc_url=sc_ip,
                    headers=headers,
                    risk_level='4',
                    risk_grade="高危风险"
                )
                home_pending = home_data.get("pending_count")
                home_done = home_data.get("done_count")

            with allure.step('校验待处置数一致'):
                assert home_pending == pending_total, (
                    f'待处置数不一致：首页待处置高危风险为 {home_pending}，风险列表待处置高危风险为 {pending_total}'
                )

            with allure.step('校验已处置数一致'):
                assert home_done == total_count, (
                    f'已处置数不一致：首页已处置高危风险为 {home_done}，风险列表已处置高危风险为 {total_count}'
                )

        except Exception as e:
            logger.error(f'test_risk_high_pending 异常: {e}', exc_info=True)
            pytest.fail(f'测试失败：{e}')
