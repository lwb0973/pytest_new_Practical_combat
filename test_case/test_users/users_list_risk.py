import requests
from jsonpath import jsonpath
from common.log_handler import setup_logger
from json import JSONDecodeError
import pytest

logger = setup_logger()


def users_list_risk(sc_ip, headers, risk=None, user_label_ids=None):
    """
    获取用户高中低风险等级总数
    :param sc_ip: 总控IP地址
    :param headers: 请求头包含token
    :param risk: 风险等级参数，可不传
    """

    try:
        url = f'https://{sc_ip}/apione/v2/users/list'
        # risk 不传时 risk_levels 必须为空列表
        risk_levels = [] if risk is None else [risk]
        payload = {
            "risk_levels": risk_levels,
            "page_num": 1,
            "page_size": 10
        }
        # ⭐ user_label_ids 传入时才添加到 payload
        if user_label_ids is not None:
            payload["user_label_ids"] = user_label_ids
        response = requests.post(url, json=payload, headers=headers, verify=False)
        assert response.status_code == 200, f'接口请求失败，状态码：{response.status_code}'
        users_count_risk = jsonpath(response.json(), '$.data.row_count')[0]
        return users_count_risk
    except JSONDecodeError as e:
        logger.error(f'提取JSON解析用户总数错误: {e}')
        pytest.fail(f'提取JSON解析用户总数解析失败: {e}')

    except Exception as e:
        logger.error(f'请求数据发生异常: {e}')
        pytest.fail(f'请求异常: {e}')
