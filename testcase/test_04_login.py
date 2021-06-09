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
login_data = member_data['login']


class TestLogin(MemberApi):
    """ 登录接口 案例层 """

    @allure.story('判断邮箱是否已注册')
    @allure.title('{test_data[title]}')
    @pytest.mark.parametrize("test_data", login_data)
    def test_login(self, test_data):
        """
        登录接口测试案例
        :param test_data: 测试数据
        :return:
        """

        log.info(f"开始执行测试案例：{test_data['title']}")

        # 测试数据替换
        test_data = json.loads(DR().replace_data(test_data))

        # 发送登录请求
        result = self.login_api(**test_data['data'])

        # 响应结果断言
        self.assert_equal(test_data['expect']['status_code'], result.status_code)

        result_json = result.json()
        if result.status_code == 200:
            self.assert_equal(test_data['data']['username'], result_json['username'])
        else:
            self.assert_equal(test_data['expect']['msg'], result_json)

        log.info(f"{test_data['title']} 测试案例执行通过！\n")






