
from jsonpath import jsonpath
import requests
from test_case.test_pending_risk_event.get_total_from_url import get_total_from_url

#
def risk_list_all_pending(sc_url, headers, risk_level):
    """
    风险列表获取对应风险等级函数
    :param sc_url: 总控地址
    :param headers: 请求头包含token
    :param risk_level: 风险等级参数
    :return:
    """
    base_url = f'https://{sc_url}/apione/v2/risk/records?page_num=1&page_size=1000&inventory=2&risk_level={risk_level}'
    pending_url = f'{base_url}&disposal_status=2'
    total_url = f'{base_url}&disposal_status=3'
    pending_total_count = get_total_from_url(pending_url, headers, "待处置")
    total_count = get_total_from_url(total_url, headers, "已处置")
    return {'pending_total_count':pending_total_count, 'total_count':total_count}


#
def risk_home_all_pending(sc_url, headers, risk_level,risk_grade):
    """
    首页获取风险待处置对应风险等级函数
    :param sc_url: 总控地址
    :param headers: 请求头包含token
    :param risk_level: 风险等级参数
    :param risk_grade: 风险等级中文名称
    :return:
    """
    url = f'https://{sc_url}/apione/v2/risk/records/summary/by-level?period=7d&time_layout=2006-01-02'
    response = requests.get(url, headers=headers, verify=False)
    assert response.status_code == 200, f'首页待处置{risk_grade}总数请求失败'
    # 提取 risk_level 为 3 的对象
    high_risk_data = jsonpath(response.json(), f'$.data.risk_level[?(@.risk_level=={risk_level})]')
    # 如果未找到数据，则使用默认值
    if  high_risk_data:
        data = high_risk_data[0]
    else:
        data = {"pending_count": 0, "total_count": 0}
    pending_count = data['pending_count']
    total_count = data['total_count']
    done_count = total_count - pending_count
    return {"pending_count":pending_count, "done_count":done_count}