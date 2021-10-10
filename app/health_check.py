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

    :return: uuid
    """
    api = 'http://yqfk.wsyu.edu.cn:8089/appLogin/login'
    # 这个地方只能传 json 参数，不能传 data
    result = requests.post(api, headers=DEFAULT_HEADERS, json=dict(
        username=username, password=password)).json()

    return result['data']['uuid']


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
    try:
        uuid = get_uuid(username, password)
    except:
        return {
            'message': '用户名或密码错误。提示：用户名为你的姓名，密码为你的学号。'
        }
    # userinfo = get_userinfo(uuid)
    # hltSt == 2 && divSt == 0 表示没有打卡
    # hltSt == 1 && divSt == 1 表示打卡

    return add_health_state(uuid, addr=addr)

    """
    checked = (userinfo['data']['hltSt'] ==
               '1' and userinfo['data']['divSt'] == '1')

    print(f'{password} 是否已经打卡: {checked}')
    # 打卡
    if not checked:
        print(password, add_health_state(uuid))
    """
