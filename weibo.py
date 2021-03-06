#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#coding: utf8

"""
所有路径为相对路径
当前目录:
    + weibo.py
    + analysis.py
    + etc
工作目录:
    当前目录/weibo/user_id/
    当前目录/weibo/user_id/images
"""

import os
import re
import requests
import traceback
import time
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
import utilities
import platform


class Weibo:

    # 默认爬虫参数
    connection_timeout = 90 # seconds
    pause_interval = 15 # 读取微博每_页停顿一次，避免短时间内读取过多
    pause_time = 5 # 停顿时长 seconds

    # Weibo类初始化
    def __init__(self, user_id, filter=1):
        self.user = {"user_id":user_id,"username":"","sex":"","region":"","birthday":"","intro":""}  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
        self.filter = filter  # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博，1代表只爬取用户的原创微博
        self.meta = {"following":0,"followers":0} # 关注数、粉丝数
        self.weibo_num = 0  # 用户全部微博数
        self.weibo_num2 = 0  # 爬取到的微博数
        self.pic_count = 0   # 所含原创图片数
        self.weibo = []  # 微博内容     {"weibo_content":"", "publish_time":"", "up_num":int,"retweet_num":int, "comment_num":int, "imgref":"","imgsetref":""}
                         # 内容，发布时间，赞，转发，评论
        self.imgurl = [] # 解析后微博图片
        self.imgset = [] # 解析后微博组图
        self.cookie = {"Cookie":""}

    def set_cookie(self, new_cookie):
        if isinstance(new_cookie,dict):
            if "Cookie" in new_cookie:
                self.cookie = new_cookie
            else:
                print("%s has no key \"Cookie\"" % new_cookie)
        else:
            print("input not a valid dictionary")

    def get_user(self):
        # 获取用户信息
        url = "https://weibo.cn/%d/info" % (int(self.user["user_id"]))
        start_time = time.time()
        while True:
            try:
                r = requests.get(url,cookies = self.cookie)
                if r.status_code != 200:
                    print("get_user: Request failure: code %d" % r.status_code)
                    return r.status_code
                else:
                    html = r.content
                break
            except Exception as e:
                if time.time() > start_time + self.connection_timeout:
                    raise Exception('Unable to get connection to %s after %s seconds of ConnectionErrors' \
                            % (url, self.connection_timeout))
                else:
                    time.sleep(1)

        soup = BeautifulSoup(html,"lxml")
        self.user["username"] = soup.find("title").text[:-3]
        textual = ''.join(item.text for item in soup.findAll("div",{"class":"c"}))
        self.user["sex"] = re.search(r'性别:(.*)?地区',textual).group(1)
        self.user["region"] = re.search(r'地区:(.*)?生日',textual).group(1)
        self.user["birthday"] = re.search(r'生日:(.*)?简介',textual).group(1)
        self.user['intro'] = re.search(r'简介:(.*)?互联网',textual).group(1)
        print("用户名：" + str(self.user["username"]))

        # 获取用户微博数、关注数、粉丝数
        url = "https://weibo.cn/u/%d?filter=%d&page=1" % (self.user['user_id'], self.filter)
        start_time = time.time()
        while True:
            try:
                html = requests.get(url,cookies = self.cookie).content
                break
            except Exception as e:
                if time.time() > start_time + self.connection_timeout: raise Exception('Unable to get connection to %s after %s seconds of ConnectionErrors' \
                            % (url, self.connection_timeout))
                else:
                    time.sleep(1)

        soup = BeautifulSoup(html,"lxml")
        try:
            self.weibo_num = int(soup.find("div",{"class":"tip2"}).find("span",{"class":"tc"}).text[3:-1])
            self.meta["following"] = int(soup.find("div",{"class":"tip2"}).findAll("a")[0].text[3:-1])
            self.meta["followers"] = int(soup.find("div",{"class":"tip2"}).findAll("a")[1].text[3:-1])

            print("微博数：" + str(self.weibo_num))
            print("关注数：" + str(self.meta["following"]))
            print("粉丝数：" + str(self.meta["followers"]))
        except Exception as e:
            print(e)
            traceback.print_exc()

        return 200

    def get_weibo(self, UPDATE=False, UPDATE_OLDTIME=datetime.now().strftime('%Y-%m-%d %H:%M')):
        # 读取每条微博信息
        #   分times次读取，中途停顿，避免短时间访问次数过多
        #   文字信息储存于: {"content","pub_time","up_num","retweet_num","comment_num"} @ */weibo/weibo.txt
        #   图片信息储存：*/weibo/pics/index/0.ext + content.txt

        page_num = 1
        pic_count = 0
        update_count = 0
        update_cache = [] # store updated_weibo

        url = "https://weibo.cn/u/%d?filter=%d&page=1" % (self.user['user_id'], self.filter)
        start_time = time.time()
        while True:
            try:
                r = requests.get(url,cookies = self.cookie)
                if r.status_code != 200:
                    print("get_weibo: Request failure: code %d" % r.status_code)
                    return r.status_code
                else:
                    html = r.content
                break
            except Exception:
                if time.time() > start_time + self.connection_timeout:
                    raise Exception('Unable to get connection to %s after %s seconds of ConnectionErrors' \
                            % (url, self.connection_timeout))
                else:
                    time.sleep(1)

        soup = BeautifulSoup(html,"lxml")

        if soup.find("input",{"name":"mp"}) == None:
            page_num = 1
        else:
            page_num = int(soup.find("input",{"name":"mp"})["value"])

        # 设定读取批次
        pause_interval = self.pause_interval
        pause_num = 1

        # 如果更新微博，首先去掉置顶微博
        if UPDATE:
            self.weibo = self.weibo[1:]

        for page in range(1,page_num + 1):

            # 周期停顿
            if (page % pause_interval == 0):
                print("正在进行第%d次停顿,防止访问次数过多" % pause_num)
                time.sleep(self.pause_time)
                pause_num += 1

            # 获取页面
            url = "https://weibo.cn/u/%d?filter=%d&page=%d" % (self.user['user_id'],self.filter,page)
            start_time = time.time()
            while True:
                try:
                    html = requests.get(url,cookies = self.cookie).content
                    break
                except Exception:
                    if time.time() > start_time + self.connection_timeout:
                        raise Exception('Unable to get connection to %s after %s seconds of ConnectionErrors' \
                                % (url, self.connection_timeout))
                    else:
                        time.sleep(1)

            soup = BeautifulSoup(html,"lxml")
            info = soup.findAll(lambda tag: tag.name == 'div' and tag.get('class') == ['c'])
            if (len(info)>3):
                if soup.title.text == '我的首页':
                    info = info[2:]
                info = info[:len(info)-2] # 最后两项为设置信息
                for each in info:
                    # 获取每页微博信息
                    str_class = each.find("span")["class"][0]
                    weibo_content = ""
                    publish_time = ""
                    up_num = 0
                    retweet_num = 0
                    comment_num = 0
                    imgref = ""
                    imgsetref = ""

                    # 微博内容
                    if str_class == 'cmt':
                        # 转发了 + 原信息 + 转发理由
                        retweet_from = each.findAll("div")[0].findAll("span")[0].text
                        retweet_content = each.findAll("div")[0].findAll("span")[1].text
                        retweet_cite = each.findAll("div")[-1].text
                        retweet_cite = retweet_cite[:retweet_cite.find(u'赞')]
                        weibo_content = retweet_from + '\n' + retweet_content + '\n' + retweet_cite
                    else:       # str_class == 'ctt'
                        weibo_content = each.find("span",{"class":"ctt"}).text

                    weibo_content = utilities.remove_nbws(weibo_content)
                    if platform.system() != 'Windows':
                        print("微博内容：" + weibo_content)

                    # 发布时间
                    publish_time = each.findAll("span",{"class":"ct"})[-1].text.split("来自")[0].strip()
                    if "刚刚" in publish_time:
                        publish_time = datetime.now().strftime('%Y-%m-%d %H:%M')
                    elif "分钟" in publish_time:
                        minute = publish_time[:publish_time.find("分钟")]
                        publish_time = (datetime.now() - timedelta(minutes=int(minute))).strftime('%Y-%m-%d %H:%M')
                    elif "今天" in publish_time:
                        today = datetime.now().strftime('%Y-%m-%d')
                        publish_time = today + " " + publish_time[3:]
                    elif "月" in publish_time:
                        publish_time = datetime.now().strftime("%Y") + '-' + publish_time[0:2] \
                                        + '-' + publish_time[3:5] + ' ' + publish_time[7:12]
                    else:
                        publish_time = publish_time[:16]
                    print("微博发布时间：" + publish_time)

                    # guid: 转、评、赞
                    str_meta = each.findAll("div")[-1].text
                    str_meta = str_meta[str_meta.find('赞'):]
                    pattern = r"\d+\.?\d*"
                    guid = re.findall(pattern, str_meta, re.M)

                    up_num = int(guid[0])
                    retweet_num = int(guid[1])
                    comment_num = int(guid[2])

                    print("点赞数：" + str(up_num) + \
                            ' 转发数：' + str(retweet_num) + \
                            ' 评论数：' + str(comment_num))
                    print()

                    # 原创图片（如果存在）
                    if str_class == "ctt" or str_class == "kt":
                        tmp_imgurl = each.find_all('a',href=re.compile(r'^http://weibo.cn/mblog/oripic',re.I))
                        if tmp_imgurl:
                            imgref = re.sub(r"amp;", '', tmp_imgurl[0]['href'])

                        tmp_imgseturl = each.find_all('a',href=re.compile(r'^http://weibo.cn/mblog/picAll',re.I))
                        if tmp_imgseturl:
                            imgsetref = tmp_imgseturl[0]['href']

                    # 储存
                    weibo_instance = {"weibo_content":weibo_content,"publish_time":publish_time,"up_num":up_num,"retweet_num":retweet_num,"comment_num":comment_num, "imgref":imgref,"imgsetref":imgsetref}

                    if UPDATE:
                        if update_count == 0 or datetime.strptime(publish_time, '%Y-%m-%d %H:%M') > datetime.strptime(UPDATE_OLDTIME, '%Y-%m-%d %H:%M'):
                            # 置顶微博总被替换
                            update_cache.append(weibo_instance)
                            self.weibo_num2 += 1
                            update_count += 1
                        else:
                            self.weibo = update_cache + self.weibo
                            print("共更新%d条微博" % (update_count-1))
                            return 200
                    else:
                        self.weibo.append(weibo_instance)
                        self.weibo_num2 += 1


        self.pic_count = pic_count
        if not self.filter:
            print("共" + str(self.weibo_num) + "条微博")
        else:
            print("共" + str(self.weibo_num) + "条微博,其中"
                    + str(self.weibo_num2) + "为原创微博")

        return 200

    # 输出微博内容
    def write_txt(self):
        try:
            if self.filter:
                result_header = "\n\n原创微博内容：\n"
            else:
                result_header = "\n\n微博内容：\n"

            result = ("用户信息\n用户昵称：" + self.user['username'] + \
                      "\n用户id：" + str(self.user['user_id']) + \
                      "\n微博数：" + str(self.weibo_num) + \
                      "\n关注数：" + str(self.meta['following']) + \
                      "\n粉丝数：" + str(self.meta['followers']) + \
                      result_header)

            compact = ""
            compact_count = 1
            for i in range(1, len(self.weibo) + 1):
                text = (str(i) + ":" + self.weibo[i - 1]['weibo_content'] + "\n" + \
                        "发布时间：" + self.weibo[i - 1]['publish_time'] + "\n" + \
                        "点赞数：" + str(self.weibo[i - 1]['up_num']) + \
                        "	 转发数：" + str(self.weibo[i - 1]['retweet_num']) + \
                        "	 评论数：" + str(self.weibo[i - 1]['comment_num']) + "\n\n")
                result = result + text

                # compact版本用于数据分析，故不计算转发内容
                if re.search(r'^转发.*',self.weibo[i - 1]['weibo_content'], re.M) == None:
                    compact = compact + str(compact_count) + ': ' + \
                            ''.join(self.weibo[i - 1]['weibo_content']) + '\n\n'
                    compact_count += 1

            file_dir = os.getcwd() + os.path.sep + "weibo" + os.path.sep + "%d" % self.user['user_id']
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
            file_path = file_dir + os.path.sep + "%d" % self.user['user_id'] + ".txt"
            file_path_c = file_dir + os.path.sep + "%d" % self.user['user_id'] + "-compact.txt"

            f = open(file_path, "wt", encoding='utf-8')
            f2 = open(file_path_c,'wt', encoding='utf-8')
            f.write(result)
            f2.write(compact)
            f.close()
            f2.close()
            print("微博写入文件完毕，保存路径:" + file_path)
        except Exception as e:
            print(e)
            traceback.print_exc()

    # 输出imgreflist
    def write_imgref_list(self):
        file_dir = os.getcwd() + os.path.sep + "weibo" + os.path.sep + str(self.user['user_id'])
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        file_path = file_dir + os.path.sep + "imgref_list.txt"

        with open(file_path,'w') as f:
            i = 1
            for each in self.weibo:
                f.write(str(i) + ', ' + each['imgref'] + '\n')
                f.write(str(i) + ', ' + each['imgsetref'] + '\n')
                i += 1

    # 从txt读取微博
    def get_weibo_from_file(self,inputfile):
        """
        路径格式：从当前文件夹开始计算
        默认：/weibo/user_id/user_id.txt
        """
        print("从%s微博文档创立Weibo() object" % inputfile.split(os.path.sep)[-1])

        if not os.path.isfile(inputfile):
            print("文件不存在 %s\n读取失败" % inputfile)
            return

        file_result = utilities.read_weibo_file(inputfile)
        user = file_result['user']
        content = file_result['content']
        time = file_result['publish_time']
        meta = file_result['meta']

        self.user['user_id'] = user['user_id']
        self.user['username'] = user['username']
        self.weibo_num = user['weibo_num']
        self.meta["following"] = user['following']
        self.meta["followers"] = user['followers']

        self.weibo_num2 = len(content)

        for i in range(self.weibo_num2):
            _weibo = {"weibo_content":content[i], "publish_time": time[i], "up_num":meta[i]['up_num'], \
                    "retweet_num":meta[i]['retweet_num'],"comment_num":meta[i]['comment_num'], \
                    "imgref": "", "imgsetref":""}
            self.weibo.append(_weibo)

    # check file backup
    def check_backup(self):
        working_path = os.getcwd() + os.path.sep + "weibo" + os.path.sep + str(self.user['user_id'])
        utilities.check_backup(working_path)

    def start(self):
        try:
            self.get_user()
            self.get_weibo()
            self.check_backup()
            self.write_txt()
            self.write_imgref_list()
        except Exception as e:
            print(e)
            traceback.print_exc()

    def update(self):
        try:
            weibo_file = (os.getcwd() + os.path.sep + "weibo" + os.path.sep + str(self.user['user_id'])
                            + os.path.sep + str(self.user['user_id']) + '.txt')
            self.get_weibo_from_file(weibo_file)
            old_length = len(self.weibo)

            status_code = self.get_user() # 更新用户信息

            UPDATE_OLDTIME = self.weibo[1]['publish_time']
            status_code = self.get_weibo(UPDATE=True, UPDATE_OLDTIME=UPDATE_OLDTIME)
            if status_code == 200:
                new_length = len(self.weibo)
                self.check_backup()
                self.write_txt() # update txt file
                self.write_imgref_list() # update imgref_list
                print("旧微博数: %d, 新微博数: %d\n" % (old_length, new_length))
            else:
                print("微博request失败，不读取新数据 code %d" % status_code)

        except Exception as e:
            print(e)
            traceback.print_exc()
