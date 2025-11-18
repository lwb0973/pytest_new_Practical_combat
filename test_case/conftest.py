import pytest
import requests
import json
import settings
import configparser
from common.base64_handler import get_login_captcha_info,recognize_captcha_from_base64,rsa_encrypt
from common.crypto_md5 import md5enc


# 读取ini配置文件
config = configparser.ConfigParser()
config.read(settings.INI_FILE, encoding='utf-8')
sc_ip = config.get('login', 'sc_ip')
username = config.get('login','username')
password = config.get('login','password')
# 登录接口获取token
@pytest.fixture(scope="session")
def sc_login():
    """
    获取 token
    :param sc_ip:
    :return:
    """
    res = requests.get("https://{}/api/v1.2/randString".format(sc_ip), verify=False)
    rand_str = res.json().get('data').get('rand')
    captcha_base64, captcha_id = get_login_captcha_info(sc_ip)
    captcha_code = recognize_captcha_from_base64(captcha_base64)
    info = ''
    if rand_str:
        temp_str = {
            "username": username,
            "password": md5enc(password),
            "uuid": rand_str,
            "captcha": captcha_code,
            "captchaId": captcha_id
        }
        info = rsa_encrypt(json.dumps(temp_str))
    info = {"info": info}
    res = requests.post(url='https://{}/api/v1.2/login'.format(sc_ip), json=info, verify=False).json()
    return res['data']['token']



