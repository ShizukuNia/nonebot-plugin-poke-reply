from pathlib import Path
import aiofiles
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Message, MessageSegment, PokeNotifyEvent, GroupMessageEvent
from nonebot.typing import T_State
from typing import List
from .config import config
import random
import time

class Utils:
    def __init__(self) -> None:
        """初始化"""

        self.poke_black_list: List = config.poke_black_list
        """黑名单不可使用Q群"""    

        self.poke_max: int = config.poke_max
        """最多戳的次数"""    

        self.poke_send_poke: bool = config.poke_send_poke
        """戳一戳是否发送反戳"""    

        self.poke_send_pic: bool = config.poke_send_pic
        """戳一戳是否发送图片"""    

        self.poke_send_text: bool = config.poke_send_text
        """戳一戳是否发送文本"""   

        self.poke_send_audio: bool = config.poke_send_audio
        """戳一戳是否发送语音"""

        self.poke_file_path: Path = config.poke_path
        """戳一戳资源路径"""

        self.poke_priority: int = config.poke_priority
        """戳一戳优先级"""

        self.poke_block: bool = config.poke_block
        """戳一戳是否阻断"""

        self.poke_file_path.joinpath("audio").mkdir(parents=True, exist_ok=True)
        self.poke_file_path.joinpath("picture").mkdir(parents=True, exist_ok=True)

    

    async def send_audio(self, matcher: Matcher):
        """发送语音"""
        if self.poke_send_audio:
            poke_audio_list = self.poke_file_path.joinpath("audio").iterdir()
            audio_file_list: List[Path] = []
            for audio_file in poke_audio_list:
                if audio_file.is_file() and audio_file.suffix.lower() in [".wav", ".mp3", ".aac"]:
                    audio_file_list.append(audio_file)
            send_audio = random.choice(audio_file_list)
            await matcher.send(MessageSegment.record(file=f"file:///{send_audio.resolve()}"))
        else:
            await matcher.send("不让发语音，果咩捏")    


    async def send_pic(self):
        """发送图片和text"""
        if self.poke_send_pic:
            logger.success("发送图片")
            poke_pic_list = self.poke_file_path.joinpath("picture").iterdir()
            pic_file_list: List[Path] = []
            for pic_file in poke_pic_list:
                if pic_file.is_file() and pic_file.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp", ".gif"]:
                    pic_file_list.append(pic_file)
            send_pic = random.choice(pic_file_list)
        else:
            send_pic = None
        return send_pic


    async def send_text(self):
        logger.success("发送文字")
        if self.poke_file_path.joinpath("poke.txt").is_file():
            async with aiofiles.open(
                self.poke_file_path.joinpath("poke.txt"),
                mode="r",
                encoding="utf-8",
            ) as f:
                text_file_list: List[str] = (await f.read()).split("\n")
                send_text = random.choice(text_file_list)
        else:
            async with aiofiles.open(
                self.poke_file_path.joinpath("poke.txt"),
                mode="w",
                encoding="utf-8",
            ) as f:
                text_file_list: List[str] = [
                "这几天心情不太好 无法直播 下次再见",
                "盒到你了",
                "谁再黑屁我，把你们🦵🦀了",
                "再戳，给你一拳",
                "啊对不起刚刚工作了 我只是想说谢谢每次给我做很多切片",
                "感觉我不在这里大家更容易说话，溜了！真的很感谢！",
                "你小心点儿",
                "你没有下次",
                "为什么每次说这个？有什么意思？",
                "这不是你的评论吗",
                "8",
                "有没有人说明什么情况？我做错了什么吗？？​",
                "马上到你家门口",
                ]
                await f.write("/n".join(text_file_list))
                send_text = random.choice(text_file_list)
        return send_text
    

    async def send_poke(self, event: GroupMessageEvent, matcher: Matcher, state: T_State):
        """对某人使用戳一戳"""
        if state["times"] > 5:
            state["times"] = 5
            await matcher.send("最多帮你戳五次")
        while state["times"] > 0:
            state["times"] -= 1
            time.sleep(0.3)
            await matcher.send(Message([MessageSegment("poke", {"qq": state["poke_list"]})]))
    
    async def poke_rule(self, event: PokeNotifyEvent):
        """黑名单判断"""
        if isinstance(event, PokeNotifyEvent):
            group = event.group_id
            return (group not in set(self.poke_black_list))
        logger.warning("rule不通过")
        return False
    

# 创建一个工具实例
utils = Utils()