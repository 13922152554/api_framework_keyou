# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import allure
from jsonpath import jsonpath
from common.basi_api import BaseApi
from common.wrapper import write_res


class MemberApi(BaseApi):
    """ 用户_接口层 """

    def register_api(self, username: str, email: str, password: str, password_confirm: str):
        """
        注册接口
        :param username: 用户名
        :param email: 邮箱
        :param password: 密码
        :param password_confirm: 确认密码
        :return: 原始响应结果
        """

        url = self.deal_url(self.conf_data['member_api']['register'])

        data = {
            "url": url,
            "method": "POST",
            "json": {
                "username": username,
                "email": email,
                "password": password,
                "password_confirm": password_confirm
            }
        }

        # 发起请求
        response = self.send_http(data)

        return response

    def check_username_register_api(self, username: str):
        """
        判断用户名是否已注册接口
        :param username: 用户名
        :return: 原始响应结果
        """

        # 替换url中的username
        url = self.deal_url(self.conf_data['member_api']['check_username_register'].replace('#username#', username))

        data = {
            "url": url,
            "method": "GET"
        }

        # 发送请求
        response = self.send_http(data)

        return response

    def check_email_register_api(self, email: str):
        """
        判断邮箱是否已注册接口
        :param email: 邮箱
        :return: 原始响应结果
        """

        # 替换url中的email
        url = self.deal_url(self.conf_data['member_api']['check_email_register'].replace('#email#', email))

        data = {
            "url": url,
            "method": "GET"
        }

        # 发送请求
        response = self.send_http(data)

        return response

    def login_api(self, username: str, password: str):
        """
        登录接口
        :param username:  用户名
        :param password:  密码
        :return:  原始响应结果
        """

        url = self.deal_url(self.conf_data['member_api']['login'])
        data = {
            "url": url,
            "method": "POST",
            "json": {
                "username": username,
                "password": password
            }
        }

        # 发送登录请求
        response = self.send_http(data)

        return response










