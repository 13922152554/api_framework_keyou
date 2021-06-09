# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import json
import pytest
import allure
from common.handle_log import log
from api.member_api import MemberApi
from middleware.project_yaml import member_data
from middleware.data_replace import DataReplace as DR


# 获取注册接口测试数据
register_data = member_data['register']


class TestRegister(MemberApi):
    """ 用户_测试案例层 """

    @allure.story('注册')
    @allure.title('{test_data[title]}')
    @pytest.mark.parametrize('test_data', register_data)
    def test_register(self, test_data, conn_db):
        """
        注册接口测试
        :param test_data: 注册接口测试数据（包含：title、data、expect、sql)
        :return:
        """

        log.info(f"开始执行测试案例：{test_data['title']}")

        # 测试数据替换
        test_data['data'] = json.loads(DR().replace_data(test_data['data']))

        # 发送请求
        result = self.register_api(**test_data['data'])

        # 响应结果断言（状态码 + 响应数据）
        self.assert_equal(test_data['expect']['status_code'], result.status_code)

        result_json = result.json()
        if result.status_code == 201:
            self.assert_equal(test_data['data']['username'], result_json['username'])
        else:
            self.assert_equal(test_data['expect']['msg'], result_json)

        # 数据库断言
        if test_data['sql']:
            # 数据库查询
            db_data = conn_db.query_one(test_data['sql'])
            self.assert_equal(test_data['data']['username'], db_data['username'])
            self.assert_equal(test_data['data']['email'], db_data['email'])

        log.info(f"{test_data['title']} 测试案例执行通过！\n")

