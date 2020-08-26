import random

from nonebot import on_command

from hoshino import R, Service, priv, util


# basic function for debug, not included in Service('chat')
@on_command('zai?', aliases=('在?', '在？', '在吗', '在么？', '在嘛', '在嘛？'), only_to_me=True)
async def say_hello(session):
    await session.send('はい！私はいつも貴方の側にいますよ！')


sv = Service('chat', visible=False)

@sv.on_fullmatch(('沙雕机器人', '沙雕機器人'))
async def say_sorry(bot, ev):
    await bot.send(ev, 'ごめんなさい！嘤嘤嘤(〒︿〒)')

@sv.on_fullmatch(('2548AB313E5D3AB4E8DD079C9A3DBEEC.jpg'))
async def zhao_zhuren(bot, ev):
    await bot.send(ev, '主人，有人叫你')

@sv.on_fullmatch(('EC56A8FF432E2FB21A30AFF413167314.jpg'))
async def zhao_zhuren(bot, ev):
    await bot.send(ev, '我来我来！')

@sv.on_fullmatch(('5A4C1EEEAB50A945DCF4CF0A0AB29F6C.jpg'))
async def maidiao(bot, ev):
    pic= R.img('biaoqing/maidiao.gif').cqcode
    await bot.send(ev, f'{pic}')

@sv.on_fullmatch(('E50DF1FC9430306644E04E0CF9D06FF1.jpg'))
async def wowan(bot, ev):
    pic= R.img('biaoqing/wowan.jpg').cqcode
    await bot.send(ev, f'{pic}')

@sv.on_rex(r'憨批', only_to_me=True)
async def say_sorry(bot, ev):
    await bot.send(ev, '憨批就是书虫')

@sv.on_rex(r'书虫', only_to_me=True)
async def say_sorry(bot, ev):
    await bot.send(ev, '书虫就是憨批')

@sv.on_rex(r'羊驼', only_to_me=True)
async def say_sorry(bot, ev):
    await bot.send(ev, '羊驼是琉璃的老公')

@sv.on_rex(r'喜欢你|爱你', only_to_me=True)
async def xihuan(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        rdm = random.random()
        #pic = R.img('bozui.jpg').cqcode
        if(rdm<0.5):
            await bot.send(ev, '你不是主人，不喜欢你，爬\n', at_sender=True)
        else:
            await bot.send(ev, 'mua~')
    else:
        await bot.send(ev, '大好きだよ、ご主人様~', at_sender=True)


@sv.on_fullmatch(('啵啵'))
async def say_bobo(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        rdm = random.random()
        #pic = R.img('bozui.jpg').cqcode
        if(rdm<0.5):
            await bot.send(ev, '下属不可以和上司啵嘴\n', at_sender=True)
        else:
            await bot.send(ev, 'mua~', at_sender=True)
    else:
        await bot.send(ev, 'mua~')

@sv.on_fullmatch(('老婆', 'waifu', 'laopo'), only_to_me=True)
async def chat_waifu(bot, ev):
    pic= R.img('laopo.jpg').cqcode
    if not priv.check_priv(ev, priv.SUPERUSER):
        
        await bot.send(ev, f'才不是你老婆，哼！\n{pic}')
    else:
        await bot.send(ev, f'mua~\n{pic}')


@sv.on_fullmatch(('睡了', '晚安'))
async def goodnight(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        await bot.send(ev, '晚安', at_sender=True)
    else:
        await bot.send(ev, '主人晚安~', at_sender=True)

@sv.on_fullmatch('叫主人', only_to_me=True)
async def call_master(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        rdm = random.random()
        if(rdm<0.5):
            await bot.send(ev, '你不是主人，爬，略略略', at_sender=True)
        else:
            await bot.send(ev, 'mua~', at_sender=True)
    else:
        await bot.send(ev, '主人mua~', at_sender=True)

@sv.on_fullmatch(('亲亲', 'kiss'))
async def chat_kiss(bot, ev):
    await bot.send(ev, 'mua~', at_sender=True)

@sv.on_fullmatch('老公', only_to_me=True)
async def chat_laogong(bot, ev):
    await bot.send(ev, '你给我滚！', at_sender=True)


@sv.on_fullmatch('mua', only_to_me=True)
async def chat_mua(bot, ev):
    await bot.send(ev, '笨蛋~', at_sender=True)


@sv.on_fullmatch('来点星奏')
async def seina(bot, ev):
    await bot.send(ev, R.img('星奏.png').cqcode)


@sv.on_fullmatch(('我有个朋友说他好了', '我朋友说他好了', ))
async def ddhaole(bot, ev):
    await bot.send(ev, '那个朋友是不是你弟弟？')
    await util.silence(ev, 30)

@sv.on_rex(r'我有个朋友')
async def yougepengyou(bot, ev):
    await bot.send(ev, '你说的那个朋友是不是你自己')
    #await util.silence(ev, 30)


@sv.on_fullmatch('我好了')
async def nihaole(bot, ev):
    await bot.send(ev, '不许好，憋回去！')
    await util.silence(ev, 30)


# ============================================ #


@sv.on_keyword(('确实', '有一说一', 'u1s1', 'yysy'))
async def chat_queshi(bot, ctx):
    if random.random() < 0.05:
        await bot.send(ctx, R.img('确实.jpg').cqcode)


@sv.on_keyword(('会战'))
async def chat_clanba(bot, ctx):
    if random.random() < 0.02:
        await bot.send(ctx, R.img('我的天啊你看看都几度了.jpg').cqcode)


@sv.on_keyword(('内鬼'))
async def chat_neigui(bot, ctx):
    if random.random() < 0.10:
        await bot.send(ctx, R.img('内鬼.png').cqcode)

nyb_player = f'''{R.img('newyearburst.jpg').cqcode}
正在播放：New Year Burst
──●━━━━ 1:05/1:30
⇆ ㅤ◁ ㅤㅤ❚❚ ㅤㅤ▷ ㅤ↻
'''.strip()

@sv.on_keyword(('春黑', '新黑'))
async def new_year_burst(bot, ev):
    if random.random() < 0.02:
        await bot.send(ev, nyb_player)
