# coding: utf-8

import json
import base64
import requests
import sys
import random

def login(username, password):
    username = base64.b64encode(username.encode('utf-8')).decode('utf-8')
    user_agents = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 '
        'Mobile/13B143 Safari/601.1]',
        'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/48.0.2564.23 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/48.0.2564.23 Mobile Safari/537.36']

    headers = {
        'User_Agent': random.choice(user_agents),
        'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F',
        'Origin': 'https://passport.weibo.cn',
        'Host': 'passport.weibo.cn'
    }
    post_data = {
        'username': '',
        'password': '',
        'savestate': '1',
        'ec': '0',
        'pagerefer': 'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F&wm=3349&vt=4',
        'entry': 'mweibo'
    }
    # 这个入口仍然有效
    login_url = 'https://passport.weibo.cn/signin/login'
    session = requests.Session()
    res = session.post(login_url,data=post_data, headers=headers)
    jsonStr = res.content.decode('gbk')
    info = json.loads(jsonStr)
    #print(info)
    if info["retcode"] == "0":
        #print("登录成功")
        # 把cookies添加到headers中，必须写这一步，否则后面调用API失败
        weibo_com_session = requests.Session()
        ret = weibo_com_session.get(info['crossDomainUrlList'][0])
        #print(ret.content)
        cookies = ret.cookies.get_dict('.weibo.com', '/')
        cookies = [key + "=" + value for key, value in cookies.items()]
        cookies = "; ".join(cookies)
        print(cookies)
    else:
        print("登录失败")

    return session

def getCookie(username, password):
    session=login(username, password)

if __name__ == '__main__':
    getCookie(sys.argv[1], sys.argv[2])
