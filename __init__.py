
import random
from nonebot.plugin import PluginMetadata
from nonebot.plugin.on import on_notice, on_command
from nonebot.adapters.onebot.v11 import (Message, MessageSegment, PokeNotifyEvent, GroupMessageEvent)
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.typing import T_State
from .utils import utils

__version__ = "0.1.0"
__plugin_meta__ = PluginMetadata(
    name="戳一戳事件",
    description="自定义群聊戳一戳事件",
    usage="戳戳",
    type="application",
    homepage="https://github.com/Agnes4m/nonebot_plugin_poke_reply",
    supported_adapters={"~onebot.v11"},
    extra={
        "version": __version__,
        "author": "shizuku_nia <1466209917@qq.com>",
    },
)


poke_rule = utils.poke_rule
# 戳一戳响应器 优先级1, 不会向下阻断, 条件: 戳一戳bot触发
poke_reply = on_notice(rule=poke_rule, block=utils.poke_block)

# 戳别人关键词响应器
poke_someone = on_command("戳", aliases={"戳一下", "去戳"}, priority=6, block=utils.poke_block)


@poke_reply.handle()
async def poke_handle(
        event: PokeNotifyEvent,
        matcher: Matcher
    ):
    """戳一戳回复, 私聊会报错, 暂时摸不着头脑"""
    probability = random.random()
    if event.is_tome():
        # 80%概率回复lu宝的语音
        if probability < 0.80:
            # 发送语音需要配置ffmpeg, 这里try一下, 不行就反戳
            try:
                await utils.send_audio(matcher)
            except Exception:
                await matcher.send("语音发不出来，只能戳戳你了")
                await matcher.send(Message([MessageSegment("poke", {"qq": f"{event.user_id}"})]))
        # 20%概率反戳回去
        else:
            await matcher.send(Message([MessageSegment("poke", {"qq": f"{event.user_id}"})]))
    else:
        # 有人在戳一戳的时候lu宝有时也会跟着戳
        if probability < 0.50:
            await matcher.send(Message([MessageSegment("poke", {"qq": f"{event.target_id}"})]))


@poke_someone.handle()
async def poke_someone(
        event: GroupMessageEvent,
        matcher: Matcher,
        state: T_State,
        args: Message=CommandArg()
        ):
    """让lu宝去戳别人"""
    for arg in args:
        if arg.type == "at":
            state["poke_list"] = arg.data["qq"]
        elif arg.type == "text":
            if "@" in arg.data["text"]:
                await matcher.finish(f"@不能只是文本哦")
            else:
                times = str(arg).replace(" ", "").replace("次", "").replace("下", "")
    if times.isdigit():
        state["times"] = int(times)
    else:
        state["times"] = 1
    await utils.send_poke(event, matcher, state)
