# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import json
import pytest
import allure
from common.handle_log import log
from case.loan_case import LoanCase
from middleware.project_yaml import loan_data
from middleware.data_replace import DataReplace as DR


# 获取创建接口测试数据
interfaces_data = loan_data['interfaces']


class TestInterfaces(LoanCase):

    @allure.story('创建接口')
    @allure.title('{test_data[title]}')
    @pytest.mark.parametrize("test_data", interfaces_data)
    def test_interfaces(self, test_data, get_login_data, conn_db):
        """
        创建接口 测试案例
        :param test_data: 创建项目 + 创建接口  测试数据
        :param get_login_data: 登录响应结果数据
        :param conn_db: 数据库连接对象
        :return:
        """

        log.info(f"开始执行测试案例：{test_data['title']}")

        # 测试数据替换
        test_data = json.loads(DR().replace_data(test_data))

        # 发送创建接口请求
        result = self.case_interface(test_data, token=get_login_data['token'])

        # 响应结果断言
        self.assert_equal(test_data['expect']['status_code'], result['status_code'])
        # 预期结果数据替换
        if result['status_code'] == 201:
            self.assert_equal(test_data['interface_data']['name'], result['data']['name'])
            self.assert_equal(test_data['interface_data']['project_id'], result['data']['project_id'])
        else:
            self.assert_equal(test_data['expect']['msg'], result['data'])

        # 数据库断言
        if test_data['sql']:
            db_data = conn_db.query_one(test_data['sql'])
            self.assert_equal(test_data['interface_data']['name'], db_data['name'])
            self.assert_equal(test_data['interface_data']['project_id'], db_data['project_id'])

        log.info(f"{test_data['title']} 测试案例执行通过！\n")






