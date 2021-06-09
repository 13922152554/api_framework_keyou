# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

from common.basi_api import BaseApi


class LoanApi(BaseApi):
    """ 项目_接口层 """

    def projects_api(self, name: str, leader: str, tester: str, programmer: str, publish_app: str, token, desc: str = None):
        """
        创建项目接口
        :param name: 项目名称
        :param leader: 项目负责人
        :param tester: 项目测试人员
        :param programmer: 开发人员
        :param publish_app: 发布应用
        :param desc: 简要描述
        :return: 原始响应结果
        """

        url = self.deal_url(self.conf_data['loan_api']['projects'])
        data = {
            "url": url,
            "method": "POST",
            "headers": {"Authorization": token},
            "json": {
                "name": name,
                "leader": leader,
                "tester": tester,
                "programmer": programmer,
                "publish_app": publish_app
            }
        }

        if desc is not None:
            data['json'].update({"desc": desc})

        # 发送请求
        response = self.send_http(data)

        return response

    def interfaces_api(self, name: str, tester: str, project_id: int, token, desc: str = None):
        """
        创建接口  接口
        :param name: 接口名称
        :param tester: 测试人员
        :param project_id: 所属项目ID
        :param desc: 简要描述
        :return: 原始响应结果
        """

        url = self.deal_url(self.conf_data['loan_api']['interfaces'])

        data = {
            "url": url,
            "method": "POST",
            "headers": {"Authorization": token},
            "json": {
                "name": name,
                "tester": tester,
                "project_id": project_id
            }
        }

        if desc:
            data['json'].update({"desc": desc})

        # 发送请求
        response = self.send_http(data)

        return response

    def test_case_api(self, name: str, interface: dict, author: str, request: str, token: str, include: str = None):
        """
        创建用例接口
        :param name: 用例名称
        :param interface: 所属接口和项目信息
        :param author: 用例执行前置顺序
        :param request: 编写人员
        :param include: 请求信息
        :return: 原始响应结果
        """

        url = self.deal_url(self.conf_data['loan_api']['testcases'])
        data = {
            "url": url,
            "method": "POST",
            "headers": {"Authorization": token},
            "json": {
                "name": name,
                "interface": interface,
                "author": author,
                "request": request
            }
        }

        if include:
            data['json'].update({"include": include})

        # 发送请求
        response = self.send_http(data)

        return response












