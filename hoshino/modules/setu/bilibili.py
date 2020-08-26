import os
import random

from nonebot.exceptions import CQHttpError

from hoshino import R, Service, priv
from hoshino.util import FreqLimiter, DailyNumberLimiter

import re
import time
from multiprocessing import Process, Queue, Pool
import threading
from urllib import request, error
from tqdm import tqdm
import http.client
import datetime 
from random import choice

from gzip import GzipFile
from io import StringIO, BytesIO
import zlib

def gzip(data):
    buf = BytesIO(data)
    f = GzipFile(fileobj=buf)
    return f.read()

class spider:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
               "Connection": "keep-alive",
               "Referer": ""}
        self.reg_title = re.compile(r'name="title" content="(.+?)\_哔哩哔哩')
        self.reg_owner = re.compile(r'"owner":{"mid":(.+?),"name":"(.+?)"')
        self.url = 'https://www.bilibili.com/video/'
        self.reg_avid = r'<meta data-vue-meta="true" itemprop="url" content="https://www.bilibili.com/video/av(\d+)/">'
        self.data_url = 'http://api.bilibili.com/archive_stat/stat?aid='
        self.image_reg = re.compile(r'<meta data-vue-meta="true" itemprop="image" content="(.+?)">')
        self.image_url = None
        
    def get_html(self,url):
        page1 = request.Request(url, headers = self.headers)
        page = request.urlopen(page1)
        encoding = page.info().get('Content-Encoding')
        html = page.read()
        if encoding == 'gzip':
            html = gzip(html)
        html = html.decode('utf-8')
        return(html) 
    def get_image(self):
        req = request.Request(self.image_url,None, self.headers)
        timeout = 1000
        res = request.urlopen(req, timeout=timeout)
        rstream = res.read()
        with open('/lustre/qq_bot/res/img/bili/video_info.jpg','wb') as f:
            f.write(rstream)
    def get_info(self, bvid):
        url = self.url+bvid
        html = self.get_html(url)
        self.headers['Referer'] = url
        title = re.findall(self.reg_title, html)[0]
        avid = re.findall(self.reg_avid, html)[0]
        wid, owner = re.findall(self.reg_owner,html)[0]
        self.image_url = re.findall(self.image_reg, html)[0]
        data_url = self.data_url+avid
        data = self.get_html(data_url)
        data = eval(data)
        return(title, avid, self.image_url, owner, url, data)


sv = Service('bilibili', manage_priv=priv.SUPERUSER, enable_on_default=True, visible=False)
@sv.on_prefix(('BV'))
async def bilibili(bot, ev):
    
    message = ev.message.extract_plain_text()
    my_spider = spider()
    bvid='BV'+message
    try:
        title, avid, image_url, owner, url, data = my_spider.get_info(bvid)
        my_spider.get_image()
        data = data['data']
        pic = R.img('bili/video_info.jpg').cqcode
        out_message1 = "标题：{0}\nAV号：{1}\nBV号：{2}\nup主:{3}\n".format(title,avid,bvid,owner)
        out_message2 = "播放量：{0}\n点赞数：{1}\n投币数：{2}\n收藏：{3}\n".format(data["view"],data["like"],data["coin"],data["favorite"])
        out_message3 = "链接：{0}".format(url)
        await bot.send(ev, out_message1+f'{pic}'+out_message2+out_message3)
    except error.HTTPError:
        await bot.send(ev, '解析失败')



