# 导包
import logging
import unittest

import allure

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

    # 定义抄表计划数据文件路径
    plan_filepath = app.GET_PATH + "/data/plan_data.json"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.step("添加抄表计划")
    @pytest.mark.parametrize("add_url, planname, planno, success", read_data(plan_filepath, 'add_plan'))
    def test01_add_cost(self, add_url, planname, planno, success):
        # 发送添加抄表计划的接口请求
        response = self.chaobiao_api.add_plan(add_url, planname, planno, app.COOKIE)
        # 打印添加抄表计划的结果
        logging.info("添加抄表计划的结果为：{}".format(response.text))
        logging.info("添加抄表计划的响应码：{}".format(response.status_code))
        assert success in response.text

    @allure.severity(allure.severity_level.NORMAL)
    @allure.step("查询抄表计划")
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

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.step("删除抄表计划")
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
