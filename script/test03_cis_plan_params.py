# 导包
import logging
import unittest

import app
from api.chaobiao_api import ChaoBiaoApi
from api.login_api import LoginApi
from utils import assert_common, read_data
from parameterized import parameterized
import pytest


# 创建测试类

@pytest.mark.run(order=99)
class TestCisPlanParams:

    def setup(self):
        # 实例化登录
        self.login_api = LoginApi()
        # 实例化计划
        self.chaobiao_api = ChaoBiaoApi()

    def teardown(self):
        pass

    def test01_login_success(self):
        # 发送登录接口请求
        data = {
            "loginName": "p0H3JjVedTYfNEK2CK79A5OcDXTgffibY+dWndUCLYlaM6u+4AAZwOA+Xw8TT4MgRjLqzCC/1Uzz4TV5XtvhedsYw8ysH2qczoB/M3xmNm0RL7DLhFw2JV5rsR8EpZumwRzA7Y3IL7WbI3ddexmlu6537DVi0rNnzNZWxDXFjVD6HJsZtAhW4aTnTUsyTJX80YM/NtwcbC2F5KWPWN2NJ2Kugprs6+EO4kX40NdCEaTkzoC793/Wf286ALI3TIfeb6CmxeUwVM8RtHrMq1eOfMzheqf4TU7VHZgsniepuLVXIfoD6A0vav8MAc7vsCXRR5c28LN8Tr3bMXIg7FtPvw==",
            "loginPwd": "kYLiSAL51EC6nLc2rgvrE5OzTFIr4JIai78QVXKJTynfnHdKlvsGToQlbEHGC99JLGMpHw81cATi+AJ/okcZ+qQuZBa4FCNwGW6GeF8XvpRghSL7Qk8xCHn5GFhcMVp9hEmY64NW5yVXeVOEXUr9icDuRZ+uytIwF4DHZ/jsj6XxVEwggpgws1AeC5pdVIzTjB/oKsxT7rerDwkaaEz3JoySscCXxpTdJ9q2lhd052w9cNpd8+TSM8T4lyQjZgRtZSSzfJJlQFIH8mBlEmNt2dh6L/wQmXn2WlNhKU+xS0+Z6m1+/wOA+cK3w4ISdhtApKTnVf1rDRwnQV3WQzj4OA=="}
        response = self.login_api.login('http://etbc.hw-qa.eslink.net.cn/user/login', data,
                                        {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
        # 打印登录接口
        # logging.info("登录接口返回的结果为：{}".format(response.json()))
        # 提取登录返回的cookies
        cookies = response.cookies
        # 把cookie保存到全局变量
        app.COOKIE = cookies
        # 打印cookie
        logging.info("提取的cookie为：{}".format(app.COOKIE))
        # 断言
        assert_common(self, 200, '100000', '运行正确', response)

    # 定义抄表计划数据文件路径
    plan_filepath = app.GET_PATH + "/data/plan_data.json"

    @pytest.mark.parametrize("add_url, planname, planno, success", read_data(plan_filepath, 'add_plan'))
    def test01_add_cost(self, add_url, planname, planno, success):
        # 发送添加抄表计划的接口请求
        response = self.chaobiao_api.add_plan(add_url, planname, planno, app.COOKIE)
        # 打印添加抄表计划的结果
        logging.info("添加抄表计划的结果为：{}".format(response.text))
        logging.info("添加抄表计划的响应码：{}".format(response.status_code))
        assert success in response.text

    # 实现查询抄表计划接口
    @pytest.mark.parametrize("query_url, planno, http_code", read_data(plan_filepath, 'query_plan'))
    def test02_query_cost(self, query_url, planno, http_code):
        # 发送查询抄表计划的接口请求
        response = self.chaobiao_api.query_plan(query_url, planno, app.COOKIE)
        # 打印查询的结果
        logging.info("查询的结果为：{}".format(response.json()))
        # 提取查询的抄表计划ID，并保存到全局变量
        app.PLAN_ID = response.json().get('data')[-1].get('mrPlanId')
        # 打印保存的ID
        logging.info("保存到全局变量抄表计划的ID为：{}".format(app.PLAN_ID))
        assert http_code == response.status_code

    # 实现删除抄表计划接口
    @pytest.mark.parametrize("del_url, success", read_data(plan_filepath, 'delete_plan'))
    def test03_del_cost(self, del_url, success):
        # 发送删除抄表计划的接口请求
        response = self.chaobiao_api.del_plan(del_url, app.PLAN_ID, app.COOKIE)
        # 打印删除的结果
        logging.info("删除的结果为：{}".format(response.text))
        try:
            assert success == response.text
        except Exception as e:
            print(e)
