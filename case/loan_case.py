# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import allure
import json
from jsonpath import jsonpath
from api.loan_api import LoanApi
from api.member_api import MemberApi
from middleware.data_replace import DataReplace as DR
from common.wrapper import log_info


class LoanCase(LoanApi):
    """ 项目_业务层
        业务层：负责关联接口、替换关联接口动态参数、传递token"""

    @log_info
    @allure.step('step:调用业务api-创建接口')
    def case_interface(self, data: dict, token):
        """
        创建接口业务场景
        :param data: 创建项目 + 创建 接口测试数据
        :return: json格式响应数据
        """

        # 创建项目
        if data.get("project_data"):
            project_res = self.projects_api(**data['project_data'], token=token).json()
            data['interface_data']['project_id'] = jsonpath(project_res, '$..id')[0]

        # 创建接口
        response = self.interfaces_api(**data['interface_data'], token=token)

        # 获取响应状态码并更新至json响应结果中
        res = dict()
        res['status_code'] = response.status_code
        res['data'] = response.json()

        return res

    @log_info
    @allure.step('step:调用业务api-创建案例')
    def case_testcases(self, data: dict, token):
        """
        创建用例接口业务场景
        :param data: 创建项目 + 创建接口 + 创建用例 接口测试数据
        :return: json格式响应结果
        """

        # 创建项目、创建接口
        interface_res = self.case_interface(data, token=token)

        # 创建案例测试数据替换（替换interface字段）
        data['testcase_data']['interface'] = json.loads(DR().replace_data(
            data['testcase_data']['interface'], source_string=interface_res['data']))

        # 创建案例
        response = self.test_case_api(**data['testcase_data'], token=token)

        # 获取响应状态码更新至json响应结果中
        res = dict()
        res['status_code'] = response.status_code
        res['data'] = response.json()

        return res


























