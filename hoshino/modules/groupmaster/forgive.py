# TODO: rewrite this


import random
from datetime import timedelta
from datetime import datetime
import nonebot
from nonebot import Message, MessageSegment, message_preprocessor, on_command
from nonebot.message import _check_calling_me_nickname

import hoshino
from hoshino import R, Service, util
from hoshino.typing import *
sv = Service('forgive', use_priv=-99999, help_='原谅被拉黑的')

FORGIVE_WORD = (
    '对不起','我错了','原谅我吧'
)

@on_command('forgive_word', aliases=FORGIVE_WORD, only_to_me=True)
async def forgive_word(session):
    ctx = session.ctx
    user_id = ctx['user_id']
    msg_from = str(user_id)
    my_stats = hoshino.priv.forgive_block_user(user_id,timedelta(minutes=1))
    pic = R.img(f"chieri{random.randint(1, 4)}.jpg").cqcode
    if(my_stats == True):
        await session.send(f"一分钟后就原谅你啦！\n{pic}", at_sender=True)
        #bot.send(ev,"原谅你啦\n", at_sender=True)
    else:
        await session.send(f"mua~\n{pic}", at_sender=True)
        #bot.send(ev,"你没做错事呀\n", at_sender=True)

DUI_WORD = (
    '不理就不理吧'
)
@on_command('dui_word', aliases=DUI_WORD, only_to_me=True)
async def dui_ren(session):
    ctx = session.ctx
    user_id = ctx['user_id']
    msg_from = str(user_id)
    is_black = hoshino.priv.check_block_user(user_id)
    pic = R.img('luelue.jpg').cqcode
    if(True):
        await session.send(f"略略略\n{pic}", at_sender=True)

#@on_command('ji_chou', aliases=('记仇'))
@sv.on_prefix('记仇')
async def yuanliang(bot, ev: CQEvent):
    if ev.user_id not in bot.config.SUPERUSERS:
        await bot.send(ev,"你不是主人，爬，略略略", at_sender=True)
    else:
        #message = ctx["message"].extract_plain_text()
        #mess_list = message.split()
        for m in ev.message:
            if m.type == 'at' and m.data['qq'] != 'all':
                ban_id = int(m.data['qq'])
        #ban_id = mess_list[1]
        ban_id = int(ban_id)
        await bot.send(ev,"好的主人，已记仇", at_sender=True)
        hoshino.priv.set_block_user(ban_id, timedelta(hours=8))


#@on_command('yuanliang', aliases=('原谅'))
@sv.on_prefix('原谅')
#async def yuanliang(session):
    #ctx = session.ctx
   # user_id = ctx['user_id']
async def yuanliang(bot, ev: CQEvent):
    if ev.user_id not in bot.config.SUPERUSERS:
        await bot.send(ev,"你不是主人，爬，略略略", at_sender=True)
    else:
        #message = ctx["message"].extract_plain_text()
        #mess_list = message.split()
        #ban_id = mess_list[1]
        for m in ev.message:
            if m.type == 'at' and m.data['qq'] != 'all':
                ban_id = int(m.data['qq'])
        ban_id = int(ban_id)
        await bot.send(ev,"好的主人，原谅TA啦", at_sender=True)
        hoshino.priv.set_block_user(ban_id, timedelta(seconds=2))
        
@sv.on_fullmatch(('查看黑名单'))
async def check_black(bot, ev):
    black = hoshino.priv.return_block_user()
    group_id = ev.group_id
    counter = 0
    if(len(black)==0):
        await bot.send(ev, '小本本上并未记仇~')
    else:
        for id in black.keys():
            if(datetime.now()>black[id]):
                continue
            mess = r'带恶人:[CQ:at,qq={0}],刑期至{1}（UTC+8）'.format(id, black[id]+timedelta(hours=6))
            await bot.send(ev, mess)
            counter += 1
        if(counter == 0):
            await bot.send(ev, '小本本上并未记仇~')
