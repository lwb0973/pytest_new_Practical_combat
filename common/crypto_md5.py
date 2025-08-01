
import hashlib


def md5enc(in_str):
    """
    字符串MD5加密
    """
    md5 = hashlib.md5()
    md5.update(in_str.encode("utf8"))
    return md5.hexdigest()

# def recognize_captcha_from_base64(base64_data):
#     """
#     识别base64，转换成具体验证码
#     """
#
#     # 从逗号处截取后面的base64字符串
#     pure_base64 = base64_data.split(",")[1] if "," in base64_data else base64_data
#     try:
#         image_data = base64.b64decode(pure_base64)
#
#         with open(os.devnull, 'w') as f:
#             sys.stdout = f
#             ocr = DdddOcr()
#             sys.stdout = sys.__stdout__
#
#         result = ocr.classification(image_data)
#         return result
#
#     except Exception as e:
#         print(f"Error processing image: {str(e)}")
#         return None
#
# def rsa_encrypt(msg: str, publickey, max_length=100):
#     """校验RSA加密 使用公钥进行加密"""
#     cipher = PKCS1_cipher.new(RSA.importKey(publickey))
#     res_byte = bytes()
#     for i in range(0, len(msg), max_length):
#         res_byte += cipher.encrypt(msg[i:i + max_length].encode('utf-8'))
#     # cipher_text = base64.b64encode(cipher.encrypt(password.encode())).decode()
#     return base64.b64encode(res_byte).decode('utf-8')
#
# def get_login_captcha_info(sc_ip):
#     resposne = requests.get("https://{}/api/v1.2/captcha".format(sc_ip), verify=False)
#     data = resposne.json()['data']
#     return data['captcha'], data['id']
#
# def get_token(sc_ip):
#     """
#             获取 token
#             :param sc_ip:
#             :return:
#             """
#     username = "admin"  # 用户名
#     password = "root123."  # 密码
#     public_key = """-----BEGIN PUBLIC KEY-----
#             MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDcu1sLod7mIz0EaYW7iM/glFNL
#             kTFI5n87pFW/0Xv2UFUiPoFKiBagZ0NsBtPTKzFFimmqEdbj0W0O7wwoQ1bupTo8
#             1qYm1EJ+Qc3REzmPyEJn9wof7vHvSlNdcIff6wJOOZ+Vqq08qK4p9HG73/8oKgVx
#             Nw4cEJUnmqUqtAP31wIDAQAB
#             -----END PUBLIC KEY-----"""  # 公钥
#
#     res = requests.get("https://{}/api/v1.2/randString".format(sc_ip), verify=False)
#     rand_str = res.json().get('data').get('rand')
#     captcha_base64, captcha_id = get_login_captcha_info(sc_ip)
#     captcha_code = recognize_captcha_from_base64(captcha_base64)
#
#     info = ''
#     if rand_str:
#         temp_str = {
#             "username": username,
#             "password": md5enc(password),
#             "uuid": rand_str,
#             "captcha": captcha_code,
#             "captchaId": captcha_id
#         }
#         info = rsa_encrypt(json.dumps(temp_str), public_key)
#     info = {"info": info}
#     res = requests.post(url='https://{}/api/v1.2/login'.format(sc_ip), json=info, verify=False).json()
#     print(res['data']['token'])
#     return res['data']['token']
#
#
# get_token('192.192.100.100')