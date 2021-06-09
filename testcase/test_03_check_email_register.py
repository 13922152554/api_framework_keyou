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


# 获取判断用户名是否注册接口测试数据
check_email_register_data = member_data['check_email_register']


class TestCheckEmailRegister(MemberApi):
    """ 判断邮箱是否已注册接口  测试案例层 """

    @allure.story('判断邮箱是否已注册')
    @allure.title('{test_data[title]}')
    @pytest.mark.parametrize("test_data", check_email_register_data)
    def test_check_email_register(self, test_data, conn_db):
        """
        判断邮箱是否已注册接口测试案例
        :param test_data: 测试数据
        :param conn_db: 数据库连接对象
        :return:
        """

        log.info(f"开始执行测试案例：{test_data['title']}")

        # 测试数据替换
        test_data['data'] = json.loads(DR().replace_data(test_data['data']))

        # 发送判断邮箱是否已注册请求
        result = self.check_email_register_api(**test_data['data'])

        # 响应结果断言
        self.assert_equal(test_data['expect']['status_code'], result.status_code)
        if result.status_code == 200:
            result_json = result.json()
            self.assert_equal(test_data['expect']['count'], result_json['count'])

        # 数据库断言
        if test_data['sql']:
            # sql语句数据替换
            test_data['sql'] = test_data['sql'].replace('#email#', test_data['data']['email'])
            db_data = conn_db.get_count(test_data['sql'])
            self.assert_equal(test_data['expect']['count'], db_data)

        log.info(f"{test_data['title']} 测试案例执行通过！\n")
