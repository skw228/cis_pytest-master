# 1.导包
import time
import unittest
from BeautifulReport import BeautifulReport
import app

# 2.组织要运行得测试套件
suite = unittest.TestLoader().discover(start_dir=app.GET_PATH + "/script/", pattern="*params.py")
# 3.定义测试报告的文件名
file_name = "test-{}.html".format(time.strftime("%Y%m%d%H%M%S"))
# file_name = "test.html"
# 4.实例化BeautifulReport的实例运行测试生成报告
# filename:测试报告的文件名
# description:测试报告描述可以理解标题
# log_path:测试报告生成路径
BeautifulReport(suite).report(filename=file_name, description="测试报告", log_path="./report")
