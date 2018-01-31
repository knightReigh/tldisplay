#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
创立一个timeline
template: https://bootsnipp.com/snippets/featured/timeline-21-with-images-and-responsive
"""
import os
import sys
from template import *
from utilities import reformat_time
from utilities import read_weibo_file
from utilities import copytree

class timecard:

    def __init__(self):
        self.time = [] # each: '2018-1-2'
        self.meta = [] # each: {'up_num','retweet_num','comment_num'}
        self.content = [] # each: 'ransfdlsmdkglja'
        self.img_path = [] # each: '/path/to/img.jpg'
        self.img_src = [] # each: 'url-to-jpg'

    def load_text(self, inputfile):
        print("为timecard加载文字信息")
        if not os.path.isfile(inputfile):
            print("文字文件不存在 %s\n加载失败" % inputfile)
            return

        weibo = read_weibo_file(inputfile)
        self.time = weibo['publish_time']
        self.content = weibo['content']
        self.meta = weibo['meta']
        self.img_src = [""] * len(self.content)
        self.img_path = [""] * len(self.content)

        for i in range(0, len(self.time)): # change Y-m-d H:M to YmdHM
            self.time[i] = reformat_time(self.time[i])



def template_wrapper(dest_path, timecards, template_name, ignore_retweet=True):
    """ wrapper function to apply timeline tempalte to timecards
    """
    template_path = os.getcwd() + os.path.sep + "timeline_templates" + os.path.sep + template_name

    header_file = template_path + os.path.sep + "head.html"
    tail_file = template_path + os.path.sep + "tail.html"

    if not os.path.isfile(header_file) or not os.path.isfile(tail_file):
        print("HTML template incomplete.")
        sys.exit()

    with open(header_file, 'rt', encoding='utf-8') as hf:
        header_string = ''.join(hf.readlines())

    with open(tail_file, 'rt', encoding='utf-8') as tf:
        tail_string = ''.join(tf.readlines())

    # build body
    body_string = ""
    if template_name == "PinkStar" or "PinkStarReverse":
        body_string = template_PinkStar(timecards,"https://weibo.com/u/5491331848", ignore_retweet)

    html_content = header_string + body_string + tail_string

    with open(dest_path + os.path.sep + "index.html", 'wt', encoding='utf-8') as f:
        f.write(html_content)

    copytree(template_path + os.path.sep + "source", dest_path + os.path.sep + "source")

def build_timeline(user_id, template_name="PinkStar"):
    """ source_path = os.getcwd() + '/weibo/weibo_id/'
    """

    # weibo_path
    weibo_path = os.getcwd() + os.path.sep + "weibo" + os.path.sep + str(user_id)
    if not os.path.isdir(weibo_path):
        print("No weibo path")
        sys.exit()

    # build timecards
    timecards = timecard()
    timecards.load_text(weibo_path + os.path.sep + str(user_id) + '.txt')

    # filter
    ignore_retweet = True

    # choose template
    dest_path = os.getcwd() + os.path.sep + "dist" + os.path.sep + str(user_id)
    if not os.path.isdir(dest_path):
        os.makedirs(dest_path)
    template_wrapper(dest_path, timecards, template_name, ignore_retweet)
