# 导包
import requests


class CostApi:

    def __init__(self):
        self.headers = {"Content-Type": "application/json;charset=UTF-8"}

    # 添加其他费用接口
    def add_cost(self, add_url, costname, cookies):
        json = {"costItem": "91",
                "costName": costname,
                "isScope": "0",
                "price": "1.00",
                "state": "1",
                "unit": "元"}
        return requests.post(url=add_url,
                             json=json,
                             headers=self.headers,
                             cookies=cookies)

    # 查询其他费用接口
    def query_cost(self, query_url, costName, cookies):
        json = {"costName": costName,
                "start": "0",
                "length": "18"}
        return requests.post(url=query_url,
                             json=json,
                             headers=self.headers,
                             cookies=cookies)

    # 修改其他费用接口
    def modify_cost(self, modify_url, octId, price, cookies):
        json = {"octId": octId,
                "price": price}
        return requests.post(url=modify_url,
                             json=json,
                             headers=self.headers,
                             cookies=cookies)

    # 删除其他费用接口
    def del_cost(self, del_url, octId, cookies):
        return requests.post(url=del_url + octId,
                             headers=self.headers,
                             cookies=cookies)
