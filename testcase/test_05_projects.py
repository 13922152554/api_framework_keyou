# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import json
import pytest
import allure
from common.handle_log import log
from api.loan_api import LoanApi
from middleware.project_yaml import loan_data
from middleware.data_replace import DataReplace as DR


# 获取创建项目接口测试数据
projects_data = loan_data['projects']


class TestAddProject(LoanApi):
    """  新增项目 测试案例层"""

    @allure.story('创建项目')
    @allure.title('{test_data[title]}')
    @pytest.mark.parametrize("test_data", projects_data)
    def test_add_project(self, test_data, conn_db, get_login_data):
        """
        创建项目接口测试案例
        :param test_data: 测试数据
        :param get_login_data: 用户登录响应结果
        :return:
        """

        log.info(f"开始执行测试案例：{test_data['title']}")

        # 测试数据替换
        test_data['data'] = json.loads(DR().replace_data(test_data['data']))

        # 发送创建项目请求
        result = self.projects_api(**test_data['data'], token=get_login_data['token'])

        # 响应结果断言（状态码 + 响应数据）
        self.assert_equal(test_data['expect']['status_code'], result.status_code)

        result_json: dict = result.json()
        # 测试数据替换
        if result.status_code == 201:
            result_json.pop("id")
            result_json.pop("create_time")
            self.assert_equal(test_data['data'], result_json)
        else:
            self.assert_equal(test_data['expect']['msg'], result_json)

        # 数据库断言
        if test_data['sql']:
            db_data = conn_db.query_one(test_data['sql'])
            self.assert_equal(test_data['data'], db_data)

        log.info(f"{test_data['title']} 测试案例执行通过！\n")







