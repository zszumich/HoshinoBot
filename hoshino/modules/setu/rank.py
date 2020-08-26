import os
import random

from nonebot.exceptions import CQHttpError
from nonebot import on_command
from hoshino import R, Service, priv
from hoshino.typing import *

import re
import os
import time
from multiprocessing import Process, Queue
import threading
from urllib import request, error, parse
import requests
from tqdm import tqdm
import http.client
import datetime 
import json

from gzip import GzipFile
from io import StringIO, BytesIO
import zlib


sv = Service('check_rank', manage_priv=priv.SUPERUSER, enable_on_default=True, visible=False)

class rank_spider:
    def __init__(self):
        self.headers = {"Custom-Source":"GitHub@zszumich","Content-Type": "application/json","Referer": "https://kengxxiao.github.io/Kyouka/"}
        self.url = 'https://service-kjcbcnmw-1254119946.gz.apigw.tencentcs.com/'
        self.payload = {'history':'0'}
    def get_data(self, check_type, refer):
        payload = self.payload
        url = self.url
        if(check_type == 'name'):
            payload['clanName'] = refer
            url = url+'name/0'
        if(check_type == 'rank'):
            url = url+'/rank/{0}'.format(refer)
        if(check_type == 'leader'):
            url = url+'/leader/0'
            payload['leaderName'] = refer
            
        data = requests.post(url, data = json.dumps(payload), headers = self.headers)
        data = json.loads(data.text)
        return(data)

def check_rank_score(spider, rank):
    data = spider.get_data('rank', rank)
    score = data['data'][0]['damage']
    return(score)

def check_rank(rank):
    rank_list = [1,3,10,20,50,200,600,1200,2800,5000,10000,15000,25000,40000,60000]
    rank_list = [x for x in rank_list if x <= rank]
    close_rank = rank_list[-1]
    return(close_rank)

def check_status(score):
    score_ratio = [[1, 1, 1.1, 1.1, 1.2],[1.2, 1.2, 1.5, 1.7, 2]]
    boss_hp = [[6000000, 8000000, 10000000, 12000000, 20000000],[6000000, 8000000, 10000000, 12000000, 20000000]]
    num_epoch = 2
    num_boss = len(boss_hp[0])
    damage = 0
    score_c = 0
    count_c = 0
    count_b = 0
    final_damage = 0
    res_damage = 0
    temp = '{0}周目{1}王,进度{2}%'
    while(score_c < score):
        count_b = 0
        while(score_c < score):
            final_damage = damage
            if(count_c < num_epoch-1):
                damage = damage + boss_hp[count_c][count_b]
                score_c = score_c + boss_hp[count_c][count_b]*score_ratio[count_c][count_b]
            else:
                damage = damage + boss_hp[num_epoch-1][count_b]
                score_c = score_c + boss_hp[num_epoch-1][count_b]*score_ratio[num_epoch-1][count_b]
            if(score_c > score):
                break
            else:
                final_damage = damage
                count_b = count_b + 1
            if(count_b == num_boss):
                break
        if(score_c > score):
            break
        count_c = count_c + 1
    remain_score = score_c - score
    if(count_c < num_epoch-1):
        remain_damage = remain_score/score_ratio[count_c][count_b]
        process = int((boss_hp[count_c][count_b]-remain_damage)/boss_hp[count_c][count_b]*100)
    else:
        remain_damage = remain_score/score_ratio[num_epoch-1][count_b]
        process = int((boss_hp[num_epoch-1][count_b]-remain_damage)/boss_hp[num_epoch-1][count_b]*100)
    result = temp.format(count_c+1, count_b+1, process)
    return(result)


def check_hanghui(name):
    result = '数据来自:https://kengxxiao.github.io/Kyouka/\n'
    my_spider = rank_spider()
    data = my_spider.get_data('name',name)
    template ='公会名称: {0}\n会长:{1}\n会长ID:{2}\n会战分数:{3}\n排名:{4}\n进度:{5}\n距档线{6}相差分数:{7}\n'
    if(data['full'] == 0):
        temp = '无法查询到此工会'
        result = result+temp
    else:
        for data_t in data['data']:
            temp = template
            score = data_t['damage']
            rank = data_t['rank']
            dang_xian = check_rank(rank)
            rank_score = check_rank_score(my_spider, dang_xian)
            score_diff = rank_score - score
            process = check_status(score)
            temp = temp.format(data_t['clan_name'],data_t['leader_name'],data_t['leader_viewer_id'],score,rank,process,
                              dang_xian,score_diff)
            result = result+temp+'\n'
        
    return(result)


@on_command('ranking', aliases=('会战排名','公会排名'), only_to_me=True)
async def calcul(session):
    ctx = session.ctx
    user_id = ctx['user_id']
    message = ctx["message"].extract_plain_text()
    mess_list = message.split()
    for m in mess_list[1:]:
        name = m
        result = check_hanghui(name)
        await session.send(result)