import os
import random

from nonebot.exceptions import CQHttpError

from hoshino import R, Service, priv
from hoshino.util import FreqLimiter, DailyNumberLimiter

from .model import setu_score

_max = 15
EXCEED_NOTICE = f'您今天已经冲过{_max}次了，请明早5点后再来！'
_nlmt = DailyNumberLimiter(_max)
_flmt = FreqLimiter(5)

sv = Service('setu', manage_priv=priv.SUPERUSER, enable_on_default=False, visible=False)
setu_folder = R.img('setu/').path

def setu_gener():
    while True:
        filelist = os.listdir(setu_folder)
        filelist = [x for x in filelist if('.jpg' in x or '.png' in x)]
        score = 0
        while(score<0.6):
            filename = random.choice(filelist)
            if os.path.isfile(os.path.join(setu_folder, filename)):
                image_name = '/lustre/qq_bot/res/img/setu/'+filename
                score = setu_score(image_name, 'model/setu-resnet-0825.pt',3)[0,0]
                if(score>0.6):
                    return(R.img('setu/', filename),score)

#etu_gener = setu_gener()

def get_setu():
    #return setu_gener.__next__()
    return setu_gener()


@sv.on_rex(r'不够[涩瑟色]|[涩瑟色]图|来一?[点份张].*[涩瑟色]|再来[点份张]|看过了|铜')
async def setu(bot, ev):
    """随机叫一份涩图，对每个用户有冷却时间"""
    uid = ev['user_id']
    if not _nlmt.check(uid):
        await bot.send(ev, EXCEED_NOTICE, at_sender=True)
        return
    if not _flmt.check(uid):
        await bot.send(ev, '您冲得太快了，请稍候再冲', at_sender=True)
        return
    _flmt.start_cd(uid)
    _nlmt.increase(uid)

    # conditions all ok, send a setu.
    pic,score = get_setu()
    r_message = '涩图指数:{0}'.format(score)
    try:
        await bot.send(ev, r_message+f'{pic.cqcode}')
        #await bot.send_msg_async(ev, r_message+f'{pic.cqcode}')
        #await bot.send(ev, '目前缺少涩图库')
    except CQHttpError:
        sv.logger.error(f"发送图片{pic.path}失败")
        try:
            await bot.send(ev, '涩图太涩，发不出去勒...')
        except:
            pass

@sv.on_fullmatch(('38976DB3BD961A97F1954BA00612925C.jpg','10D7F00255B6757551350352F3735670.jpg','10D7F00255B6757551350352F3735670.png'))
async def setu1(bot, ev):
    """随机叫一份涩图，对每个用户有冷却时间"""
    uid = ev['user_id']
    if not _nlmt.check(uid):
        await bot.send(ev, EXCEED_NOTICE, at_sender=True)
        return
    if not _flmt.check(uid):
        await bot.send(ev, '您冲得太快了，请稍候再冲', at_sender=True)
        return
    _flmt.start_cd(uid)
    _nlmt.increase(uid)

    # conditions all ok, send a setu.
    pic,score = get_setu()
    r_message = '涩图指数:{0}'.format(score)
    try:
        await bot.send(ev, r_message+f'{pic.cqcode}')
        #await bot.send(ev, '目前缺少涩图库')
    except CQHttpError:
        sv.logger.error(f"发送图片{pic.path}失败")
        try:
            await bot.send(ev, '涩图太涩，发不出去勒...')
        except:
            pass

@sv.on_fullmatch(('{76051E9A-225D-5A80-C17F-9C0F225B4F4F}.mirai'))
async def fsetu(bot, ev):
    """随机叫一份涩图，对每个用户有冷却时间"""
    uid = ev['user_id']
    if not _nlmt.check(uid):
        await bot.send(ev, EXCEED_NOTICE, at_sender=True)
        return
    if not _flmt.check(uid):
        await bot.send(ev, '您冲得太快了，请稍候再冲', at_sender=True)
        return
    _flmt.start_cd(uid)
    _nlmt.increase(uid)

    # conditions all ok, send a setu.
    for count in range(1,4):
        pic,score = get_setu()
        r_message = '涩图指数:{0}'.format(score)
        try:
            await bot.send(ev, r_message+f'{pic.cqcode}')
            #await bot.send(ev, '目前缺少涩图库')
        except CQHttpError:
            sv.logger.error(f"发送图片{pic.path}失败")
            try:
                await bot.send(ev, '涩图太涩，发不出去勒...')
            except:
                pass
    
