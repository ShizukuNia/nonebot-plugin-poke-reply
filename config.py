from typing import List
from pathlib import Path
from nonebot import get_driver
from pydantic import BaseSettings


class Config(BaseSettings):
    
    poke_black_list: List = []
    """黑名单不可使用Q群"""    
    poke_max: int = 5
    """最多戳的次数"""    
    poke_send_poke: bool = True
    """戳一戳是否发送反戳"""    
    poke_send_pic: bool = False
    """戳一戳是否发送图片"""    
    poke_send_text: bool = False
    """戳一戳是否发送文本"""   
    poke_send_audio: bool = True
    """戳一戳是否发送语音"""
    poke_path: Path = Path("data/poke")
    """资源路径"""
    poke_priority: int = 1
    """戳一戳优先级"""
    poke_block: bool = True
    """戳一戳是否阻断"""
    class Config:
        extra = "ignore"


config = Config.parse_obj(get_driver().config)

if not config.poke_path.exists() or not config.poke_path.is_dir():
    config.poke_path.mkdir(0o755, parents=True, exist_ok=True)