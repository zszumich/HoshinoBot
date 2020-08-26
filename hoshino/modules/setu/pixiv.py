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

from .model import setu_score


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)

def check_dir(path):
    folder = os.path.exists(path)
    return(folder)


def get_pixiv_picture(path):
    record_name = path+'/record.txt'
    f = open(record_name,'r')
    filename = []
    for line in f:
        line = line.replace('\n','')
        filename.append(line)
    file = choice(filename)
    txt_name = path+'/'+file+'.txt'
    title = open(txt_name,'r',encoding='UTF-8').readline()
    reg = r'-pid(\d+)'
    pid = re.findall(reg,file)[0]
    return(file, title, pid)

class spider:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
               "Connection": "keep-alive",
               "Referer": ""}
    def get_html(self,url):
        page1 = request.Request(url, headers = self.headers)
        page = request.urlopen(page1)
        html = page.read().decode('utf-8')
        return(html) 

class pixiv_spider:
    def __init__(self, new=False):
        self.url = "https://www.pixiv.net/ranking.php?mode=daily&content=illust&p=%d&date=%d%02d%02d"
        self.date = datetime.datetime.now()
        if(new):
            self.img_reg = re.compile(
                r'class="new".+?data-filter="thumbnail-filter lazy-image"data-src="(.+?\.jpg)"data-type="illust"')
        else:
            self.img_reg = re.compile(
                r'data-filter="thumbnail-filter lazy-image"data-src="(.+?\.jpg)"data-type="illust"')
        self.content_reg = r'<title>#(.*)- pixiv</title>'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
               "Connection": "keep-alive",
               "Referer": ""}
    def get_pixiv_id(self, url):
        reg = r'.+/(\d+)_p0'
        return re.findall(reg, url)[0]
    def get_referer(self, url):
        reference = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id="
        return reference + self.get_pixiv_id(url)
    def get_pictures(self, spider, page, path):
        url = self.url%(page,self.date.year, self.date.month, self.date.day-2)
        html = spider.get_html(url)
        image_urls = re.findall(self.img_reg, html)
        num_image = len(image_urls)
        print("get {0} images on page {1}".format(num_image, page))
        file = open(path+'/record.txt','a')
        for i in range(0,num_image):
            image_url = image_urls[i]
            image_url = image_url.replace('c/240x480/img-master','img-original')
            image_url = image_url.replace('_master1200','')
            #image_url = image_url.replace('.jpg', '.png')
            pixiv_id = self.get_pixiv_id(image_url)
            content_url = self.get_referer(image_url)
            self.headers['Referer'] = content_url
            content_html = spider.get_html(content_url)
            file_name = 'pixiv-rank-{0}-{1}-{2}-pid{3}'.format(self.date.year, self.date.month, self.date.day-2, pixiv_id)
            file.write(file_name+'\n')
            image_title = re.findall(self.content_reg, content_html)
            with open(path+'/'+file_name+'.txt','w',encoding='UTF-8') as f:
                f.write(image_title[0])
            f.close()
            try:
                timeout = 1000
                req = request.Request(image_url,None, self.headers)
                res = request.urlopen(req, timeout=timeout)
                image_name = file_name+'.jpg'
                rstream = res.read()
                with open(path+'/'+file_name+'.jpg','wb') as f:
                    f.write(rstream)
            except error.HTTPError:
                image_url = image_url.replace('.jpg', '.png')
                timeout = 1000
                req = request.Request(image_url,None, self.headers)
                res = request.urlopen(req, timeout=timeout)
                image_name = file_name+'.png'
                rstream = res.read()
                with open(path+'/'+file_name+'.png','wb') as f:
                    f.write(rstream)
            print(image_name)
        file.close()
        return(num_image)



class pixiv_spider_mp:  #多进程爬虫
    def __init__(self,spider, path, new=False, r18 = False):
        if(r18):
            self.url = "https://www.pixiv.net/ranking.php?mode=daily_r18&content=illust&p=%d&date=%d%02d%02d"
        else:
            self.url = "https://www.pixiv.net/ranking.php?mode=daily&content=illust&p=%d&date=%d%02d%02d"
        self.date = datetime.datetime.now() - datetime.timedelta(days=2)
        if(new):
            self.img_reg = re.compile(
                r'class="new".+?data-filter="thumbnail-filter lazy-image"data-src="(.+?\.jpg)"data-type="illust"')
        else:
            self.img_reg = re.compile(
                r'data-filter="thumbnail-filter lazy-image"data-src="(.+?\.jpg)"data-type="illust"')
        self.content_reg = r'<title>#(.*)- pixiv</title>'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
               "Connection": "keep-alive",
               "Referer": ""}
        self.path = path
        self.spider = spider
    def get_pixiv_id(self, url):
        reg = r'.+/(\d+)_p0'
        return re.findall(reg, url)[0]
    def get_referer(self, url):
        reference = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id="
        return reference + self.get_pixiv_id(url)
    def save_picture(self, image_url):
        path = self.path
        spider = self.spider
        image_url = image_url.replace('c/240x480/img-master','img-original')
        image_url = image_url.replace('_master1200','')
        #image_url = image_url.replace('.jpg', '.png')
        pixiv_id = self.get_pixiv_id(image_url)
        content_url = self.get_referer(image_url)
        self.headers['Referer'] = content_url
        content_html = spider.get_html(content_url)
        file_name = 'pixiv-rank-{0}-{1}-{2}-pid{3}'.format(self.date.year, self.date.month, self.date.day, pixiv_id)
        image_title = re.findall(self.content_reg, content_html)
        with open(path+'/'+file_name+'.txt','w',encoding='UTF-8') as f:
            if(len(image_title)>0):
                f.write(image_title[0])
            else:
                f.write('no title')
        f.close()
        try:
            timeout = 1000
            req = request.Request(image_url,None, self.headers)
            res = request.urlopen(req, timeout=timeout)
            image_name = file_name+'.jpg'
            rstream = res.read()
            with open(path+'/'+file_name+'.jpg','wb') as f:
                f.write(rstream)
        except error.HTTPError:
            image_url = image_url.replace('.jpg', '.png')
            timeout = 1000
            req = request.Request(image_url,None, self.headers)
            res = request.urlopen(req, timeout=timeout)
            image_name = file_name+'.png'
            rstream = res.read()
            with open(path+'/'+file_name+'.png','wb') as f:
                f.write(rstream)
        print(image_name)
        
    def save_image_name(self, image_urls):
        path = self.path
        num_image = len(image_urls)
        file = open(path+'/record.txt','a')
        for i in range(0,num_image):
            image_url = image_urls[i]
            pixiv_id = self.get_pixiv_id(image_url)
            file_name = 'pixiv-rank-{0}-{1}-{2}-pid{3}'.format(self.date.year, self.date.month, self.date.day, pixiv_id)
            file.write(file_name+'\n')
        file.close()
        
        
    def get_pictures(self, page):
        spider = self.spider
        path = self.path
        url = self.url%(page,self.date.year, self.date.month, self.date.day)
        html = spider.get_html(url)
        image_urls = re.findall(self.img_reg, html)
        num_image = len(image_urls)
        print("get {0} images on page {1}".format(num_image, page))
        self.save_image_name(image_urls)
        pool = Pool()
        pool.map(self.save_picture, image_urls) #多线程爬虫
        pool.close()
        pool.join()
        #for i in range(0,num_image):
            #image_url = image_urls[i]
            #self.save_picture(image_url)  #单线程模式
        
        return(num_image)




class pixiv_spider_male:  #多进程爬虫
    def __init__(self,spider, path, new=False, r18 = False):
        if(r18):
            self.url = "https://www.pixiv.net/ranking.php?mode=male_r18&p=%d&date=%d%02d%02d"
        else:
            self.url = "https://www.pixiv.net/ranking.php?mode=male&p=%d&date=%d%02d%02d"
        self.date = datetime.datetime.now() - datetime.timedelta(days=2)
        if(new):
            self.img_reg = re.compile(
                r'class="new".+?data-filter="thumbnail-filter lazy-image"data-src="(.+?\.jpg)"data-type="illust"')
        else:
            self.img_reg = re.compile(
                r'data-filter="thumbnail-filter lazy-image"data-src="(.+?\.jpg)"data-type="illust"')
        self.content_reg = r'<title>#(.*)- pixiv</title>'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
               "Connection": "keep-alive",
               "Referer": ""}
        self.path = path
        self.spider = spider
    def get_pixiv_id(self, url):
        reg = r'.+/(\d+)_p0'
        return re.findall(reg, url)[0]
    def get_referer(self, url):
        reference = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id="
        return reference + self.get_pixiv_id(url)
    def save_picture(self, image_url):
        path = self.path
        spider = self.spider
        image_url = image_url.replace('c/240x480/img-master','img-original')
        image_url = image_url.replace('_master1200','')
        #image_url = image_url.replace('.jpg', '.png')
        pixiv_id = self.get_pixiv_id(image_url)
        content_url = self.get_referer(image_url)
        self.headers['Referer'] = content_url
        content_html = spider.get_html(content_url)
        file_name = 'pixiv-rank-{0}-{1}-{2}-pid{3}'.format(self.date.year, self.date.month, self.date.day, pixiv_id)
        image_title = re.findall(self.content_reg, content_html)
        with open(path+'/'+file_name+'.txt','w',encoding='UTF-8') as f:
            if(len(image_title)>0):
                f.write(image_title[0])
            else:
                f.write('no title')
        f.close()
        try:
            timeout = 1000
            req = request.Request(image_url,None, self.headers)
            res = request.urlopen(req, timeout=timeout)
            image_name = file_name+'.jpg'
            rstream = res.read()
            with open(path+'/'+file_name+'.jpg','wb') as f:
                f.write(rstream)
        except error.HTTPError:
            image_url = image_url.replace('.jpg', '.png')
            timeout = 1000
            req = request.Request(image_url,None, self.headers)
            res = request.urlopen(req, timeout=timeout)
            image_name = file_name+'.png'
            rstream = res.read()
            with open(path+'/'+file_name+'.png','wb') as f:
                f.write(rstream)
        print(image_name)
        
    def save_image_name(self, image_urls):
        path = self.path
        num_image = len(image_urls)
        file = open(path+'/record.txt','a')
        for i in range(0,num_image):
            image_url = image_urls[i]
            pixiv_id = self.get_pixiv_id(image_url)
            file_name = 'pixiv-male-{0}-{1}-{2}-pid{3}'.format(self.date.year, self.date.month, self.date.day, pixiv_id)
            file.write(file_name+'\n')
        file.close()
        
        
    def get_pictures(self, page):
        spider = self.spider
        path = self.path
        url = self.url%(page,self.date.year, self.date.month, self.date.day)
        html = spider.get_html(url)
        image_urls = re.findall(self.img_reg, html)
        num_image = len(image_urls)
        print("get {0} images on page {1}".format(num_image, page))
        self.save_image_name(image_urls)
        pool = Pool()
        pool.map(self.save_picture, image_urls) #多线程爬虫
        pool.close()
        pool.join()
        #for i in range(0,num_image):
            #image_url = image_urls[i]
            #self.save_picture(image_url)  #单线程模式
        
        return(num_image)





sv = Service('pixiv', manage_priv=priv.SUPERUSER, enable_on_default=True, visible=False)
@sv.on_fullmatch(('爬取今日图片'), only_to_me=True)
async def get_pixiv(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        
        await bot.send(ev, '你不是主人，爬')
    else:
        await bot.send(ev, '好的主人，将爬取pixiv排行榜前三页图片')
        num_img = 0
        my_spider = spider()
        #my_pixiv_spider = pixiv_spider(new=True)
        date = datetime.datetime.now() - datetime.timedelta(days=2)
        path = '/lustre/qq_bot/res/img/pixiv/%02d%02d'%(date.month,date.day)
        is_dir = check_dir(path)
        if(is_dir):
            await bot.send(ev, '图片已经完成爬取')
        else:
            mkdir(path)
            my_pixiv_spider = pixiv_spider_mp(spider = my_spider, path = path, new = False, r18 = False)
            for i in range(1,4):
                num_img = num_img + my_pixiv_spider.get_pictures(i)
            await bot.send(ev, '爬取完成，共收集{0}张图片'.format(num_img))


@sv.on_fullmatch(('今日图片'), only_to_me=True)
async def get_picture(bot, ev):
    date = datetime.datetime.now()
    delta = datetime.timedelta(days=2)
    date = date - delta
    path = '/lustre/qq_bot/res/img/pixiv/%02d%02d'%(date.month,date.day)
    is_dir = check_dir(path)
    if(is_dir):
        file_n, title, pid = get_pixiv_picture(path)
        file_p = path+'/'+file_n+'.png'
        if(check_dir(file_p)):
            file_n = 'pixiv/%02d%02d'%(date.month,date.day)+'/'+file_n+'.png'
        else:
            file_n = 'pixiv/%02d%02d'%(date.month,date.day)+'/'+file_n+'.jpg'
        pic = R.img(file_n).cqcode
        score = setu_score('../res/img/'+file_n, 'model/setu-resnet-0825.pt',3)
        r_message = 'title: {0}, pixiv id:{1}，涩图指数:{2}'.format(title,pid, score)
        await bot.send(ev, r_message+f'{pic}')
    else:
        await bot.send(ev, '尚未获得今日图片，请使用“爬取今日图片”命令获取')

@sv.on_fullmatch(('补充涩图'), only_to_me=True)
async def get_pixiv(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        
        await bot.send(ev, '你不是主人，爬')
    else:
        await bot.send(ev, '好的主人，将爬取pixiv排行榜前三页图片')
        num_img = 0
        my_spider = spider()
        #my_pixiv_spider = pixiv_spider(new=True)
        date = datetime.datetime.now() - datetime.timedelta(days=2)
        path = '/lustre/qq_bot/res/img/setu'
        is_dir = check_dir(path)
        if(is_dir):
            my_pixiv_spider = pixiv_spider_male(spider = my_spider, path = path, new = False, r18 = False)
            for i in range(1,4):
                num_img = num_img + my_pixiv_spider.get_pictures(i)
            await bot.send(ev, '爬取完成，共收集{0}张图片'.format(num_img))
    
        else:
            mkdir(path)
            my_pixiv_spider = pixiv_spider_male(spider = my_spider, path = path, new = False, r18 = False)
            for i in range(1,4):
                num_img = num_img + my_pixiv_spider.get_pictures(i)
            await bot.send(ev, '爬取完成，共收集{0}张图片'.format(num_img))