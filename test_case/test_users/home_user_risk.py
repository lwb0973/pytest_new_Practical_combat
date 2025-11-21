import requests
from jsonpath import jsonpath
from json import JSONDecodeError
from common.log_handler import setup_logger
logger = setup_logger()
import pytest

def home_user_risk(sc_ip,headers,total_count):
    """
    获取首页用户相关数据总数字段
    :param sc_ip: 总控IP地址
    :param headers: 请求头包含token
    :param total_count: 获取用户相关总数参数
    :return:
    """
    try:
        url = f'https://{sc_ip}/apione/v2/users/metrics'
        response = requests.get(url, headers=headers, verify=False)
        assert response.status_code == 200, '首页用户总数请求响应失败'
        users_count = jsonpath(response.json(), f'$.data.metric.{total_count}')
        assert users_count, '未获取用户总数字段数据'
        return users_count[0]

    except JSONDecodeError as e:
        logger.error(f'提取JSON解析用户总数错误: {e}')
        pytest.fail(f'提取JSON解析用户总数解析失败: {e}')

    except Exception as e:
        logger.error(f'请求数据发生异常: {e}')
        pytest.fail(f'请求异常: {e}')


