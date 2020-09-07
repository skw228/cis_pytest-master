# 导包
import json

import app
import logging
from logging import handlers


# 编写初始化日志的代码
# 1 首先定义一个初始化日志的函数
def init_logging():
    # 2 在函数中，设置日志器
    logger = logging.getLogger()
    # 3 设置日志等级
    logger.setLevel(logging.INFO)
    # 4 设置控制台处理器
    sh = logging.StreamHandler()
    # 5 设置文件处理器（文件处理的作用是设置保存日志的文件地址的：需要使用项目根目录定位到日志文件）
    log_path = app.GET_PATH + "/log/ihrm.log"
    fh = logging.handlers.TimedRotatingFileHandler(log_path,
                                                   when='M',  # 分钟
                                                   interval=1,  # 间隔
                                                   backupCount=3,  # 保留
                                                   encoding='utf-8')
    # 6 设置格式化器
    fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
    formatter = logging.Formatter(fmt)
    # 7 将格式化器添加到文件处理器和控制台处理当中
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    # 8 将文件处理器和控制台处理器添加到日志器当中
    logger.addHandler(sh)
    logger.addHandler(fh)


# 封装登录通用断言函数
def assert_common(self, http_code, returnCode, returnMessage, response):
    assert http_code == response.status_code
    assert returnCode == response.json().get('responseCode')
    assert returnMessage in response.json().get('message')


# 读取登录数据的函数
def read_login_data(filepath):
    # 打开数据文件
    with open(filepath, mode='r', encoding='utf-8') as f:
        # 使用json加载数据文件为json格式
        jsonData = json.load(f)
        # 遍历json格式数据文件，把数据处理成列表元组([(),(),()])形式添加到空列表中
        result_list = list()
        for login_data in jsonData:  # type:dict
            # 把values转化为元组形式，并添加到空列表中
            result_list.append(tuple(login_data.values()))
    # print("查看读取的登录数据为：", result_list)
    # 换行
    # print()
    return result_list


# 读取模块的数据函数
def read_data(filepath, interface_name):
    with open(filepath, mode='r', encoding='utf-8') as f:
        # 把数据文件加载成json格式
        jsonData = json.load(f)
        # 读取加载的json数据当中对应接口的数据
        cost_data = jsonData.get(interface_name)  # type:dict
        # 把数据处理成列表元组对象，然后添加到空列表中
        result_list = list()
        result_list.append(cost_data.values())
        # 返回数据
    # print("读取的{}员工数据为：{}".format(interface_name, result_list))
    return result_list


# if __name__ == '__main__':
#     # 定义数据文件路径
#     filepath = app.GET_PATH + "/data/login_data.json"
#     # 读取数据，并接收返回结果
#     result = read_login_data(filepath)
#     # 打印返回的结果
#     print("返回的结果为：", result)

if __name__ == '__main__':
    # 定义员工数据路径
    filepath = app.GET_PATH + "/data/cost_data.json"
    # 读取员工数据
    print(read_data(filepath, 'add_cost'))
    read_data(filepath, 'query_cost')
    read_data(filepath, 'modify_cost')
    read_data(filepath, 'delete_cost')
