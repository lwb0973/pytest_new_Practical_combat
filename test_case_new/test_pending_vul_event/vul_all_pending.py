
from jsonpath import jsonpath
import requests
from test_case.test_pending_vul_event.get_total_from_url import get_total_from_url

# 弱点列表获取对应弱点等级函数
def vul_list_all_pending(sc_url, headers, vul_level):
    base_url = f'https://{sc_url}/apione/v2/vul/records?page_num=1000000&page_size=50&api_name_exact=0&vul_level={vul_level}'
    pending_url = f'{base_url}&disposal_status=2&layout=2006-01-02%2015%3A04%3A05'
    total_url = f'{base_url}&disposal_status=3&layout=2006-01-02%2015%3A04%3A05'
    pending_total_count = get_total_from_url(pending_url, headers, "待处置")
    total_count = get_total_from_url(total_url, headers, "已处置")
    return {'pending_total_count':pending_total_count, 'total_count':total_count}


# 首页获取弱点待处置对应弱点等级函数
def vul_home_all_pending(sc_url, headers, vul_level,vul_grade):
    url = f'https://{sc_url}/apione/v2/vul/records/summary/by-level?period=7d&time_layout=2006-01-02'
    response = requests.get(url, headers=headers, verify=False)
    assert response.status_code == 200, f'首页待处置{vul_grade}总数请求失败'
    # 提取 risk_level 为 3 的对象
    high_vul_data = jsonpath(response.json(), f'$.data.vul_level[?(@.vul_level=={vul_level})]')
    # 如果未找到数据，则使用默认值
    if  high_vul_data:
        data = high_vul_data[0]
    else:
        data = {"pending_count": 0, "total_count": 0}
    pending_count = data['pending_count']
    total_count = data['total_count']
    done_count = total_count - pending_count
    return {"pending_count":pending_count, "done_count":done_count}