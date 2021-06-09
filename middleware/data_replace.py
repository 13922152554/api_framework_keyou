# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import re
import json
import random
from jsonpath import jsonpath
from faker import Faker, Factory
from middleware.project_yaml import conf_data
from middleware.project_mysql import ProjectMysql
from middleware.project_yaml import res_yaml


class DataReplace:

    def __init__(self):
        self.db = ProjectMysql()
        self.fake = Factory().create('zh_CN')

    @property
    def len_six_user_name(self):
        """
        生成六位长度未注册的用户名：test.auth_user表中不存在的username字符串
        :return: 生成的字符串
        """

        while True:
            username = self.fake.pystr(min_chars=6, max_chars=6)
            sql = f"select * from test.auth_user where username='{username}';"
            db_data = self.db.get_count(sql)
            if not db_data:
                break

        return username

    @property
    def len_twenty_user_name(self):
        """
        生成20位长度未注册的用户名：test.auth_user表中不存在的username字符串
        :return: 生成的字符串
        """

        username = self.fake.pystr(min_chars=20, max_chars=20)

        return username

    @property
    def old_user_name(self):
        """
        已注册的用户名：auth_user表中最大id记录的username
        :return: 已注册的用户名
        """

        sql = 'select username from test.auth_user ORDER BY id desc LIMIT 0, 1;'
        db_data = self.db.query_one(sql)

        return db_data['username']

    @property
    def email(self):
        """
        生成符合标准格式且未注册的邮箱(test.auth_user表中不存在的email）
        :return: 生成的email
        """
        while True:
            email = self.fake.email()
            sql = f"select * from test.auth_user where email='{email}';"
            db_data = self.db.get_count(sql)
            if not db_data:
                break

        return email

    @property
    def old_email(self):
        """
        已经注册的邮箱：auth_user表中最大id记录的username
        :return: 已注册的邮箱
        """

        sql = "SELECT id,email FROM test.auth_user WHERE email !='' ORDER BY id DESC LIMIT 0,1;"
        db_data = self.db.query_one(sql)

        return db_data['email']

    @property
    def username(self):
        """ 从配置文件中读取登录用户名 """

        return conf_data['account']['username']

    @property
    def password(self):
        """ 从配置文件中读取登录用户密码 """

        return conf_data['account']['password']

    @property
    def len_one_str(self):
        """ 一位长度的字符串 """

        while True:
            len_one_str = self.fake.pystr(min_chars=5, max_chars=5)
            sql = f"SELECT * FROM test.`tb_projects` WHERE NAME='{len_one_str}';"
            db_data = self.db.get_count(sql)
            if not db_data:
                break

        return len_one_str

    @property
    def len_fifty_str(self):
        """ 五十位长度的字符串 """

        while True:
            len_fifty_str = self.fake.pystr(min_chars=50, max_chars=50)
            sql = f"SELECT * FROM test.`tb_testcases` WHERE NAME='{len_fifty_str}';"
            db_data = self.db.get_count(sql)
            if not db_data:
                break

        return len_fifty_str

    @property
    def len_max_fifty_str(self):
        """ 大于50位长度（51长度）的字符串 """

        return self.fake.pystr(min_chars=51, max_chars=51)

    @property
    def len_two_hundred_str(self):
        """ 两百位长度的字符串 """

        return self.fake.pystr(min_chars=200, max_chars=200)

    @property
    def len_max_two_hundred_str(self):
        """ 大于200长度（201长度)的字符串"""

        return self.fake.pystr(min_chars=201, max_chars=201)

    @property
    def len_hundred_str(self):
        """ 100位长度的字符串 """

        return self.fake.pystr(min_chars=100, max_chars=100)

    @property
    def len_max_hundred_str(self):
        """ 大于100位长度（101长度）的字符串 """

        return self.fake.pystr(min_chars=101, max_chars=101)

    @property
    def old_project_name(self):
        """ 已存在的项目名称 """

        sql = "SELECT NAME FROM test.`tb_projects` ORDER BY id DESC LIMIT 0,1;"
        db_data = self.db.query_one(sql)

        return db_data['NAME']

    @property
    def old_testcase_name(self):
        """ 已存在的用例名 """

        sql = 'SELECT NAME FROM test.`tb_testcases` ORDER BY id DESC LIMIT 0,1;'
        db_data = self.db.query_one(sql)

        return db_data['NAME']

    @property
    def min_interface_id(self):
        """ 查询最新项目ID下的最大interface_id 再减1 """

        sql = 'SELECT id FROM test.`tb_interfaces` WHERE project_id=(SELECT MAX(project_id) FROM test.`tb_interfaces`)'
        db_data = self.db.query_one(sql)

        return str(db_data['id'] - 1)

    def replace_data(self, target_string: str, source_string: dict = None):
        """
        测试数据替换： 要替换的数据均是源数据与目标数据中均能查找匹配上的值（任意一方匹配为空时均不进行替换）
        1、从DataReplace类中提取target_string字符串中要进行替换的值，替换target_string字符串中的数据
        2、从source_string字典中提取target_string字符串中要进行替换的值，替换target_string字符串中的数据
        :param source_string: （源）字典
        :param target_string: （目标）字符串：要进行替换的字符串
        :return:
        """

        # 若传递的数据非str类型则将转换为json字符串类型
        if not isinstance(target_string, str):
            target_string = json.dumps(target_string)

        pattern = r'#(.+?)#'

        str_data: str = target_string

        search_list = list()

        # 一次性匹配查到源字符串中所有符合条件的字符并存储到search_list列表中
        while re.search(pattern, str_data):

            # 查找第一个匹配项作为键值（类属性名）
            search_list.append(re.search(pattern, str_data).group(1))

            # 将每一次匹配到的字符串替换为空字符（若不进行替换则每次只能匹配同一个字符）
            str_data = str_data.replace(f'#{search_list[-1]}#', '', 1)

        # 挨个替换能在DataReplace类中匹配到的字符，无法匹配到的则不进行替换
        for item in search_list:

            # 从Context类的对象中获取key属性的值，若不存在则返回空
            if source_string:
                value = jsonpath(source_string, f'$..{item}')[0]
            else:
                value = getattr(self, item, '')

            if value:
                # 将获取到的value替换相应匹配到的子字符串（注意：每次只替换一次，否则所有以#开头以#结束的子字符串将全部被替换）
                # string_data = re.sub(pattern, value, string_data, 1)  # 存在问题：当for循环迭代变量在此类属性中找不到时也被替换成下一个存在的迭代变量对应的属性值
                if not isinstance(value, str):
                    value = str(value)
                target_string = target_string.replace(f'#{item}#', value, 1)

        return target_string

    def __make_phone(self):
        """ 生成手机号 """

        fake = Faker(locale='zh_CN')
        phone_number = fake.phone_number()

        return phone_number

    def close_db(self):
        self.db.close()


if __name__ == '__main__':
    from middleware.project_yaml import member_data
    # print(member_data['register'][0]['data'])
    str_data = "ADSFKLJDL #loan_id#"
    con = DataReplace()
    data = con.replace_data(str_data)
    print(data)






