import allure
import pytest
import settings
from common.log_handler import setup_logger
import urllib3
import configparser
from test_case.test_pending_risk_event.get_total_from_url import get_total_from_url
from test_case.test_pending_vul_event.vul_all_pending import vul_list_all_pending, vul_home_all_pending

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = setup_logger()

config = configparser.ConfigParser()
config.read(settings.INI_FILE, encoding='utf-8')
sc_ip = config.get('login', 'sc_ip')


@allure.feature('【首页】-【待处置事件】-【低危弱点待处置/已处置饼图】')
class TestCase:
    @classmethod
    def setup_class(cls):
        logger.info('======== 获取首页待处置事件低危弱点待处置/已处置饼图，测试开始 ==========')


    @classmethod
    def teardown_class(cls):
        logger.info('======== 获取首页待处置事件低危弱点待处置/已处置饼图，测试结束 ==========')

    @allure.story('【待处置低危弱点总数】')
    def test_vul_low_pending(self, sc_login):
        """待处置/已处置低危弱点事件饼图总数"""
        try:
            headers = {'token': sc_login}
            # 获取弱点事件列表数据
            with allure.step('【弱点】-【弱点事件列表】接口'):
                vul_data = vul_list_all_pending(
                    sc_url=sc_ip,
                    headers=headers,
                    vul_level='2'  # 低危弱点等级
                )
                pending_total = vul_data.get("pending_total_count")
                total_count = vul_data.get("total_count")

                logger.info(f'获取弱点列表低危待处置数量：{pending_total}，已处置数量：{total_count}')

                assert pending_total is not None, "弱点列表待处置低危弱点事件总数未获取"
                assert total_count is not None, "弱点列表低危弱点事件总数未获取"

            # 获取首页饼图数据
            with allure.step('【待处置低危弱点总数】接口'):
                home_data = vul_home_all_pending(
                    sc_url=sc_ip,
                    headers=headers,
                    vul_level='2',
                    vul_grade='低危弱点'
                )

            # 校验待处置数量
            with allure.step('校验待处置数一致'):
                assert home_data.get("pending_count") == pending_total, (
                    f'待处置数不一致：首页待处置低危弱点为 {home_data.get("pending_count")}，'
                    f'弱点列表待处置低危弱点为 {pending_total}'
                )

            # 校验已处置数量
            with allure.step('校验已处置数一致'):
                assert home_data.get("done_count") == total_count, (
                    f'已处置数不一致：首页已处置低危弱点为 {home_data.get("done_count")}，'
                    f'弱点列表已处置低危弱点为 {total_count}'
                )

        except Exception as e:
            logger.error(f'test_vul_low_pending 异常: {e}', exc_info=True)
            pytest.fail(f'测试失败：{e}')
