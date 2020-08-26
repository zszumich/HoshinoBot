import re
import os
import time
from multiprocessing import Process, Queue, Pool
import threading
from urllib import request, error
from tqdm import tqdm
import http.client
import datetime
import urllib

import requests

from hoshino.typing import *
import os
import random

from nonebot.exceptions import CQHttpError

from hoshino import R, Service, priv
from hoshino.util import FreqLimiter, DailyNumberLimiter

from .model import setu_score

sv = Service('pixiv_finder', manage_priv=priv.SUPERUSER, enable_on_default=False, visible=True)
setu_folder = R.img('setu/').path

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)

def get_url_code(name):
    url_code = urllib.parse.quote(name)
    return(url_code)

class pixiv_finder:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
               "Connection": "keep-alive",
                "cookie": 'first_visit_datetime_pc=2020-07-19+04%3A58%3A20; p_ab_id=9; p_ab_id_2=4; p_ab_d_id=607830816; yuid_b=FhR0MUM; _ga=GA1.2.672916843.1595102319; PHPSESSID=56740049_yYR0J141eAZydms7qiAlSLRYaN8yMC9Q; c_type=25; privacy_policy_agreement=2; a_type=0; b_type=1; login_ever=yes; _fbp=fb.1.1595102335143.643957705; categorized_tags=BU9SQkS-zU~OEXgaiEbRa~b8b4-hqot7~y8GNntYHsi; __cfduid=d986566d66ebc4ed44cd50d984f2cb4b31598342788; __utmc=235335808; limited_ads=%7B%22responsive%22%3A%22%22%7D; _gid=GA1.2.1387906540.1598344120; tag_view_ranking=RTJMXD26Ak~UHoCzjluR7~Z6bm0MDWcb~LX3_ayvQX4~CKmTUJN-vB~zlJWvJkZ3-~QJ0EuFHij-~N2nQExjPv0~Z6xukSbUC-~Lt-oEicbBr~vti3o9ERHH~nbsmIXaCVu~GVhqHdSy8A~FDU-lMiwEp~p9OU_hVZ6E~0xsDLqCEW6~9yRbHTPFto~UM_HqLzRzs~BU9SQkS-zU~y8GNntYHsi~7JJvM2-Bzx~cV8vQf3-sD~7Uj2al1_Ht~ijVwpxjcnx~jH0uD88V6F; __utma=235335808.672916843.1595102319.1598374122.1598424533.15; __utmz=235335808.1598424533.15.6.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; __utmt_p=1; tags_sended=1; __utmt_ssl=1; __utmt_www=1; _gcl_au=1.1.38001198.1598424646; __utmv=235335808.|2=login%20ever=yes=1^3=plan=premium=1^5=gender=male=1^6=user_id=56740049=1^9=p_ab_id=9=1^10=p_ab_id_2=4=1^11=lang=zh=1; ki_t=1595272002623%3B1598424529552%3B1598424657989%3B4%3B7; ki_r=; __utmb=235335808.13.9.1598424560515',
               "Referer": ""}
        self.refer = 'https://www.pixiv.net/ajax/search/artworks/{0}?word={0}&order=popular_male_d&mode=safe&p=1&s_mode=s_tag&type=all'
    def get_id(self,name):
        url_code = get_url_code(name)
        refer = self.refer.format(url_code)
        header = self.headers
        header['Referer'] = refer
        session = requests.get(refer, headers=header)
        JSON = session.json()
        pic_list ={}
        for data in JSON["body"]["illustManga"]["data"]:
            if 'id' in data.keys():
                pic_list[data['id']] = data['illustTitle']
                #url_list[data['id']] = url[0]
        return(pic_list)
    def get_image(self, name, pic_id):
        URL = "https://www.pixiv.net/ajax/illust/{0}/pages?lang=zh".format(pic_id)
        url_code = get_url_code(name)
        refer = self.refer.format(url_code)
        header = self.headers
        header['Referer'] = refer
        session = requests.get(URL, headers=header)
        JSON1 = session.json()
        url = JSON1["body"][0]["urls"]["original"]
        timeout = 1000
        req = request.Request(url,None, header)
        res = request.urlopen(req, timeout=timeout)
        rstream = res.read()
        if('jpg' in url):
            filename = setu_folder+'/pixiv/temp/test.jpg'
        elif('png' in url):
            filename = setu_folder+'/pixiv/temp/test.png'
        with open(filename,'wb') as f:
            f.write(rstream)
        return(filename)

@sv.on_prefix('来张')
async def finder(bot, ev: CQEvent):
    m = ev.message[0]
    m = m.data['text']
    m = m.replace("色图",'')
    m = m.replace('涩图','')
    m = m.replace('瑟图','')
    filepath = setu_folder+'/pixiv/temp/'
    mkdir(filepath)
    spider = pixiv_finder()
    pic_list = spider.get_id(m)
    pid_list = list(pic_list.keys())
    if(len(pid_list)==0):
        await bot.send(ev,'无法找到{0}的涩图，爪巴'.format(m), at_sender=True)
    else:
        pid = random.choice(pid_list)
        title = pic_list[pid]
        image_name = spider.get_image(m,pid)
        score = setu_score(image_name, 'model/setu-resnet-0825.pt',3)
        pic = R.img(image_name).cqcode
        string = "标题:{0}\npid:{1}\n涩图指数{2}".format(title,pid,score[0][0])
        await bot.send(ev,string+f'{pic}', at_sender=True)

@sv.on_prefix('来份')
async def finder(bot, ev: CQEvent):
    m = ev.message[0]
    m = m.data['text']
    m = m.replace("色图",'')
    m = m.replace('涩图','')
    m = m.replace('瑟图','')
    filepath = setu_folder+'/pixiv/temp/'
    mkdir(filepath)
    spider = pixiv_finder()
    pic_list = spider.get_id(m)
    pid_list = list(pic_list.keys())
    if(len(pid_list)==0):
        await bot.send(ev,'无法找到{0}的涩图，爪巴'.format(m), at_sender=True)
    else:
        pid = random.choice(pid_list)
        title = pic_list[pid]
        image_name = spider.get_image(m,pid)
        score = setu_score(image_name, 'model/setu-resnet-0825.pt',3)
        pic = R.img(image_name).cqcode
        string = "标题:{0}\npid:{1}\n涩图指数{2}".format(title,pid,score[0][0])
        await bot.send(ev,string+f'{pic}', at_sender=True)

@sv.on_prefix('来点')
async def finder(bot, ev: CQEvent):
    m = ev.message[0]
    m = m.data['text']
    m = m.replace("色图",'')
    m = m.replace('涩图','')
    m = m.replace('瑟图','')
    filepath = setu_folder+'/pixiv/temp/'
    mkdir(filepath)
    spider = pixiv_finder()
    pic_list = spider.get_id(m)
    pid_list = list(pic_list.keys())
    if(len(pid_list)==0):
        await bot.send(ev,'无法找到{0}的涩图，爪巴'.format(m), at_sender=True)
    else:
        pid = random.choice(pid_list)
        title = pic_list[pid]
        image_name = spider.get_image(m,pid)
        score = setu_score(image_name, 'model/setu-resnet-0825.pt',3)
        pic = R.img(image_name).cqcode
        string = "标题:{0}\npid:{1}\n涩图指数{2}".format(title,pid,score[0][0])
        await bot.send(ev,string+f'{pic}', at_sender=True)