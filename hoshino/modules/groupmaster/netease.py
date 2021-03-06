import random

from nonebot import on_command

from hoshino import R, Service, priv, util

sv = Service('netease', manage_priv=priv.SUPERUSER, enable_on_default=True, visible=False)

net_east = ['“生而为人,我很抱歉”','“日推到这首歌的人一定很温柔吧”','“我认识的很多,但我的朋友很少','“陌生人,如果你刷到这条评论就睡吧',
           '“老师讲什么都听不懂了,好想放弃”','“我喜欢你，从满心欢喜到满目疮疾”','“这么晚还在听歌的人,你一定也很寂寞吧”',
           '“温柔吗,拿命换的”','“自己有多伤心,歌单知道,枕头知道,你不知道”','“舔了三年,她终究还是离开了我','“你说爱情要两情相悦,否则,所有的喜欢都是心酸”',
           '“我是两个孩子的父亲…','“《人间失格》里有这样一句话：仅一夜之间，我的心判若两人。他自人山人海中来，原来只为给我一场空欢喜。你来时携风带雨，我无处可避；你走时乱了四季，我久病难医”',
           '“是什么原因让你来听这首歌啊”','“这歌真正听懂的时候一定很悲伤吧”','“我通过了你的好友请求，现在我们可以开始聊天',
           '“你走以后……”','“我今天失恋了，陌生人能给我点个赞吗？”','“教堂的白鸽不会亲吻乌鸦”','“我说下雨了，不是指天气”','“今年12岁，重度抑郁症20年了”',
           '“妈妈在我出生前就走了”','“现实里没有任何一个人理我”','“今天看了看，30楼好像也不高。。。”','“人间不值得”','“人间真好，下次不来了”',
           '“我今年17岁，出意外的话明年18岁，不出意外的话我将永远17岁…”','你也只活了一次，凭什么说我选择的人生是错的。','你爱过一个人吗？从满心欢喜到满目疮痍······',
           '考研可能也失败了，妈妈明天因为心脏有问题要去看，继父不管，我亲爹关机不敢接我电话，那些亲人除了我阿姨在为我们东奔西跑，我才23岁了我承受了那么多，听着这首歌会哭的',
           '重度抑郁啦，不能给家里添麻烦，不买药啦，自己百度怎么缓解情绪。不告诉朋友啦，因为无从开口，平时我都是逗他们开心的。不告诉男朋友啦，"','爸爸在年前查出肺腺癌晚期，一切来的太突然，本来就不富裕的家庭更是雪上加霜，经常看到妈妈夜里擦眼泪，可我到底还是高一学生，分担不了家庭负担，只能好好学习，不知道爸爸还能陪我多久，我真的好爱我的家庭，好爱爸爸和妈妈。',
           '现在已经五年级下册了，老师讲的内容什么也听不进去，成绩也越来越差了，原本想好好努力的，结果没过几天就不想学了，我该怎么办呐',
           '我抑郁症了，我温柔吗，半条命换的快来安慰我我快高考了，赶紧鼓励我','我倒数第一，语文零分，数学零分，英语全是选择题，我成功的错过了所有正确答案。2020我中考，完全没希望······',
           '今年经历太多了，被绿了，被骗2500元，疫情，亲人去世，父母离婚，考试取消，抑郁症复发，控制不住自己的情绪，我也好想爱这个世界啊，我才十几岁我可以的！',
           '五年没有联系的前任，结婚了生了孩子，是我们一直想要的女儿，名字竟然也是我取的,但姓不一样了。','我的爷爷得了冠状病毒，我的生活到了谷底。但是我要坚强，勇敢向前看，迎接我的未来，我的生活。阿门！祝我爷爷康复[可爱][流泪][流泪]',
           '我愛的是位男生，我卻也是一位男生，我的人生，還能成人生嗎?','大四了，工作没着落，没有爱的人，未来不知道去哪，不知道有多少人和我一样，好像渐渐失去直觉，失去了爱人的勇气。好想大声哭一场。我是真的需要个方向啊，更需要人陪。',
           '我逃了很久 拒绝过很多人 直到遇见你 我开始动摇 相信所谓的苦尽甘来 后来才发现你也不爱我','我讨厌圈钱的女孩子，可是如果是你，我更讨厌没钱的自己','他不在对岸 我也不够勇敢',
           '磨脚的鞋子我不会穿第二次，剪坏我头发的理发店，我不会去第二次，可是就是那个不适合我的人我爱了不止一次',
           '你说什么最难熬，是漫漫长夜，还是两月三年，是两人相爱的不能见面，还是你爱的人不爱你','“《人间失格》里有这样一句话：“若能避开猛烈的欢喜，自然也不会有悲痛的来袭。””',
           '“你回信息速度越来越慢，和我说话越来越少，我就知道你要走了”','“我有那么多奇妙的能力 却留不住你”','“这么晚还在听歌的人,你一定也很寂寞吧“',
           '“那些看似没有听懂的回应，大概就是再委婉不过的拒绝”','“《人间失格》里有这么一句话：‘你在此地不要走动，我去给你买袋橘子。’”']



@sv.on_rex(r'网易云|网抑云')
async def netease(bot, ev):
    temp = random.choice(net_east)
    await bot.send(ev, temp)