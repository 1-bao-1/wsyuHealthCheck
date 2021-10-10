"""
模拟健康打卡的思路
1. 通过 http://yqfk.wsyu.edu.cn:8089/appLogin/login 获取 uuid 作为打卡的参数
2. 传入对应参数即可
"""

import requests

DEFAULT_HEADERS = {
    'User-Agent': 'wasp'
}


def get_uuid(username: str, password: str) -> str:
    """获取 uuid，作为打卡的参数传入打卡函数
    :param: username 你的学号
    :param: password 你的名字

    :return: 请求到的数据
    """
    api = 'http://yqfk.wsyu.edu.cn:8089/appLogin/login'

    # 这个地方只能传 json 参数，不能传 data
    return requests.post(api, headers=DEFAULT_HEADERS, json=dict(
        username=username, password=password)).json()


def get_userinfo(uuid: str) -> dict:
    """获取一些基本信息，其中包含是否打卡的信息
    :param: uuid 通过 get_uuid 获取的字符串

    :return: 一些基本信息
    """
    api = 'http://yqfk.wsyu.edu.cn:8089/appWX/getUserInfo'
    return requests.post(api, headers=DEFAULT_HEADERS, json={'UUID': uuid}).json()


def add_health_state(uuid: str, addr: str = '', ansr: str = '') -> dict:
    api = 'http://yqfk.wsyu.edu.cn:8089/hltQstnr/addHltQstnr'

    if not addr:
        addr = '湖北省武汉市'  # 填报的地理位置

    if not ansr:
        ansr = '2,2,2,'  # 一切正常

    post_data = {
        'ansr': ansr,
        'address': addr,
        'uuid': uuid
    }

    return requests.post(api, headers=DEFAULT_HEADERS, json=post_data).json()


def health_check(username: str, password: str, addr: str = ''):
    """打卡并返回结果

    :return: (是否成功, 接口数据)"""
    rjson = get_uuid(username, password)

    # code == 00 有两种可能：
    # 1. 用户名或密码错误
    # 2. 用户已经打过卡了
    # 第二种情况会有个 data 字段。我们希望返回错误的情况是用户名或密码错误，因此下面需要加个判断
    if rjson['code'] != '00' and 'data' not in rjson:
        return False, rjson

    uuid = rjson['data']['uuid']
    return True, add_health_state(uuid, addr=addr)
