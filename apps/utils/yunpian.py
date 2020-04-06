__author__ = 'Yuxiang'

import json
import requests

from MxShop.settings import YP_APIKEY


class Yunpian(object):
    """
    向云片网请求发送验证码
    """
    def __init__(self):
        self.api_key = YP_APIKEY
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        params = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': '【何雨润】您的验证码是{}。如非本人操作，请忽略本短信'.format(code)
        }

        response = requests.post(self.single_send_url, params)
        re_dict = json.loads(response.text)
        return re_dict


if __name__ == '__main__':
    yunpian = Yunpian()
    print(yunpian.single_send_url)
    yunpian.send_sms('1234', '17316356753')