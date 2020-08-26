
import random
from datetime import timedelta

import nonebot
from nonebot import Message, MessageSegment, message_preprocessor, on_command
from nonebot.message import _check_calling_me_nickname

import hoshino
from hoshino import R, Service, util
from math import *

sv = Service('bot-caculation', help_='计算器')

@on_command('calcul', aliases=('cal','calculate'), only_to_me=True)
async def calcul(session):
    ctx = session.ctx
    user_id = ctx['user_id']
    message = ctx["message"].extract_plain_text()
    mess_list = message.split()
    try:
        result = eval(mess_list[1])
        await session.send(str(result), at_sender=True)
    except SyntaxError as reason:
        if(user_id == 844965747):
            await session.send('主人，算式出错了', at_sender=True)
        else:
            await session.send('算式出错了，憨批', at_sender=True)
    
    
