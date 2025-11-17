import requests
from jsonpath import jsonpath
from common.log_handler import setup_logger
import pytest
logger = setup_logger()



def get_total_from_url(url, headers, label):
    """
    请求接口并返回 $.data.total 字段
    :param url: 总控地址
    :param headers: 请求头包含token
    :param label: 弱点记录处置状态带处置/已处置，中文标识
    :return:
    """
    try:
        response = requests.get(url, headers=headers, verify=False)
        assert response.status_code == 200, f"{label} 接口请求失败，状态码：{response.status_code}"

        total = jsonpath(response.json(), '$.data.total')
        if not total:
            logger.error(f"{label} 字段提取失败：未找到 $.data.total")
            pytest.fail(f"{label} 字段提取失败")
        return total[0]
    except Exception as e:
        logger.error(f"{label} 请求或数据提取失败: {e}", exc_info=True)
        pytest.fail(f"{label} 请求异常: {e}")