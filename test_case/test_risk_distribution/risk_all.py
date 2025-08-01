
from jsonpath import jsonpath
import requests
import pytest
from common.log_handler import setup_logger
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = setup_logger()

# 获取api列表对应风险等级的api数
def risk_api_list(sc_url,headers,payload):
    url = f'https://{sc_url}/apione/v2/assets/list'
    response = requests.post(url, json=payload, headers=headers, verify=False)
    assert response.status_code == 200, f'接口请求失败，状态码：{response.status_code}'
    all_row_count = jsonpath(response.json(), '$.data.row_count')
    if not all_row_count:
        logger.error("row_count 字段提取失败")
        pytest.fail("setup_class: row_count 字段为空或未提取到")
    return all_row_count[0]




# 获取首页高中低风险api数
def home_risk_api(sc_url,headers,all_risk_count,risk_name):
    url = f'https://{sc_url}/apione/v2/api-assets/home/summary?period=7d'
    response = requests.request(method='GET', url=url, headers=headers, verify=False)
    assert response.status_code == 200, f'首页{risk_name}api总数请求响应失败'
    risk_all_count = jsonpath(response.json(), f'$.data.metric.{all_risk_count}')[0]
    return risk_all_count

