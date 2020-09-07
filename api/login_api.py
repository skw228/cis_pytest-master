# 导包
import requests
from requests import Response


# 封装接口类
class LoginApi:
    def __init__(self):
        pass

    def login(self, url, data, headers):
        """
        :rtype:Response
        """
        # 发送登录请求，并返回。
        return requests.post(url=url, data=data, headers=headers)
