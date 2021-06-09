# -*- coding:utf-8 -*-
# Email:84351228@qq.com
# Author:KeKe

import pytest
from middleware.project_yaml import conf_data
from api.member_api import MemberApi
from common.handle_mysql import HandleMysql
from common.wrapper import write_res


@pytest.fixture(scope="class")
def conn_db():
    db = HandleMysql(**conf_data['mysql'])
    yield db
    db.close()


@pytest.fixture
def get_login_data():
    user_account = conf_data['account']
    login_data = MemberApi().login_api(**user_account).json()
    login_data['token'] = f'JWT {login_data["token"]}'
    yield login_data




