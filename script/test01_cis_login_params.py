# 导包
# !/usr/bin/env Python
# coding=utf-8
import unittest, logging

import app
from api.login_api import LoginApi
from utils import assert_common, read_login_data
from parameterized import parameterized
import pytest


@pytest.mark.run(order=1)
class TestCisLoginParams:
    # 初始化
    def setup(self):
        self.login_api = LoginApi()

    # 登录
    # 定义登录数据文件的路径
    filepath = app.GET_PATH + '/data/login_data.json'

    @pytest.mark.parametrize("case_name, login_url, request_body, http_code, returnCode, returnMessage",
                             read_login_data(filepath))
    def test_login(self, case_name, login_url, request_body, http_code, returnCode, returnMessage):
        response = self.login_api.login(login_url, request_body,
                                        {"Content-Type": "application/x-www-form-urlencoded"})
        logging.info("登录的结果为：{}".format(response.json()))
        assert_common(self, http_code, returnCode, returnMessage, response)
