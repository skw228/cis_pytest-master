# 导包
import requests


class ChaoBiaoApi:

    def __init__(self):
        self.headers = {"Content-Type": "application/json;charset=UTF-8"}

    # 添加抄表计划接口
    def add_plan(self, add_url, planname, planno, cookies):
        json = {"addrId": "202009012011269610102203886880",
                "addrs": [],
                "codeId": "110228",
                "frequencyUnit": '1',
                "limitBillingQty": "0",
                "mrFrequency": "1",
                "mrPlanName": planname,
                "mrPlanNo": planno,
                "mrPlanType": "11",
                "mrStaffId": "44210",
                "nextExecDate": "2020-09-03",
                "tenantId": "ITQ8m46H1FpoaC2brNC52vLr06lv24LA"}
        return requests.post(url=add_url,
                             json=json,
                             headers=self.headers,
                             cookies=cookies)

    # 查询抄表计划接口
    def query_plan(self, query_url, planno, cookies):
        json = {"mrPlanNo": planno,
                "start": "0",
                "length": "18"}
        return requests.post(url=query_url,
                             json=json,
                             headers=self.headers,
                             cookies=cookies)

    # 删除抄表计划接口
    def del_plan(self, del_url, planid, cookies):
        return requests.post(url=del_url + planid,
                             headers=self.headers,
                             cookies=cookies)
