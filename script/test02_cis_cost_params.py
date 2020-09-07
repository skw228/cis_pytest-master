# 导包
import logging
import unittest

import allure

import app
from api.cost_api import CostApi
from api.login_api import LoginApi
from utils import assert_common, read_data
from parameterized import parameterized
import pytest


# 创建测试类

@pytest.mark.run(order=2)
class TestCisCostParams:

    def setup(self):
        # 实例化登录
        self.login_api = LoginApi()
        # 实例化费用
        self.cost_api = CostApi()

    def teardown(self):
        pass

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.step("登录")
    def test01_login_success(self):
        allure.attach("账号：30000，密码：eslink888", "登录")
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

    # 定义其他费用数据文件路径
    cost_filepath = app.GET_PATH + "/data/cost_data.json"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.step("添加其他费用")
    @pytest.mark.parametrize("add_url, costname, success", read_data(cost_filepath, 'add_cost'))
    def test02_add_cost(self, add_url, costname, success):
        # 发送添加其他费用的接口请求
        response = self.cost_api.add_cost(add_url, costname, app.COOKIE)
        # 打印添加员工的结果
        logging.info("添加其他费用的结果为：{}".format(response.text))
        # logging.info("添加费用的响应码：{}".format(response.status_code))
        assert success in response.text

    @allure.severity(allure.severity_level.NORMAL)
    @allure.step("查询其他费用")
    @pytest.mark.parametrize("query_url, costName, http_code", read_data(cost_filepath, 'query_cost'))
    def test03_query_cost(self, query_url, costName, http_code):
        # 发送查询其他费用的接口请求
        response = self.cost_api.query_cost(query_url, costName, app.COOKIE)
        # 打印查询的结果
        logging.info("查询的结果为：{}".format(response.json()))
        # 提取查询的其他费用ID，并保存到全局变量
        app.OCT_ID = response.json().get('data')[-1].get('octId')
        # 打印保存的ID
        logging.info("保存到全局变量其他费用的ID为：{}".format(app.OCT_ID))
        assert http_code == response.status_code

    @allure.severity(allure.severity_level.MINOR)
    @allure.step("修改其他费用")
    @pytest.mark.parametrize("modify_url, price, success", read_data(cost_filepath, 'modify_cost'))
    def test04_modify_cost(self, modify_url, price, success):
        # 发送修改其他费用的接口请求
        response = self.cost_api.modify_cost(modify_url, app.OCT_ID, price, app.COOKIE)
        # 打印修改的结果
        logging.info("修改的结果为：{}".format(response.text))
        assert success in response.text

    @allure.severity(allure.severity_level.TRIVIAL)
    @allure.step("删除其他费用")
    @pytest.mark.parametrize("del_url, success", read_data(cost_filepath, 'delete_cost'))
    def test05_del_cost(self, del_url, success):
        # 发送删除其他费用的接口请求
        response = self.cost_api.del_cost(del_url, app.OCT_ID, app.COOKIE)
        # 打印删除的结果
        logging.info("删除的结果为：{}".format(response.text))
        assert success in response.text
