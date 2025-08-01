import os
import sys
import base64
from ddddocr import DdddOcr
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
import requests

# 获取验证码图片原始数据
def get_login_captcha_info(sc_ip):
    resposne = requests.get("https://{}/api/v1.2/captcha".format(sc_ip), verify=False)
    data = resposne.json()['data']
    return data['captcha'], data['id']

# 转换成验证码图片
def recognize_captcha_from_base64(base64_data):
    """
    识别base64，转换成具体验证码
    """
    # 从逗号处截取后面的base64字符串
    pure_base64 = base64_data.split(",")[1] if "," in base64_data else base64_data
    try:
        image_data = base64.b64decode(pure_base64)
        with open(os.devnull, 'w') as f:
            sys.stdout = f
            ocr = DdddOcr()
            sys.stdout = sys.__stdout__
        result = ocr.classification(image_data)
        return result
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None

# 统一加密
def rsa_encrypt(msg: str, max_length=100):
    """校验RSA加密 使用公钥进行加密"""
    public_key = """-----BEGIN PUBLIC KEY-----
                   MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDcu1sLod7mIz0EaYW7iM/glFNL
                   kTFI5n87pFW/0Xv2UFUiPoFKiBagZ0NsBtPTKzFFimmqEdbj0W0O7wwoQ1bupTo8
                   1qYm1EJ+Qc3REzmPyEJn9wof7vHvSlNdcIff6wJOOZ+Vqq08qK4p9HG73/8oKgVx
                   Nw4cEJUnmqUqtAP31wIDAQAB
                   -----END PUBLIC KEY-----"""

    cipher = PKCS1_cipher.new(RSA.importKey(public_key))
    res_byte = bytes()
    for i in range(0, len(msg), max_length):
        res_byte += cipher.encrypt(msg[i:i + max_length].encode('utf-8'))
    return base64.b64encode(res_byte).decode('utf-8')
