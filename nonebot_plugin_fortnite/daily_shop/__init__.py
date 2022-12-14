from nonebot.plugin import on_command

from utils.utils import scheduler, get_bot
from utils.manager import group_manager
from utils.message_builder import image
from services.log import logger

__zx_plugin_name__ = "商城"
__plugin_usage__ = """
usage：
    堡垒之夜每日商城
    指令：
        商城
""".strip()
__plugin_type__ = ("堡批专属",)
__plugin_cmd__ = ["商城"]
__plugin_des__ = "堡垒之夜每日商城"
__plugin_task__ = {"fn":"堡垒之夜商城推送"}

@scheduler.scheduled_job(
    "cron",
    hour=8,
    minute=2,
)
async def shopupshop():
    try:
        bot = get_bot()
        gl = await bot.get_group_list()
        gl = [g["group_id"] for g in gl]
        result = get_dailyshop()
        for g in gl:
            if await group_manager.check_group_task_status(g, 'fn'):
                await bot.send_group_msg(group_id=g, message=result) 
    except Exception as e:
        logger.error("堡垒之夜商城错误 {e}")

shopshop = on_command("商城", priority=5, block=True)    
@shopshop.handle()
async def _():
    result = get_dailyshop()
    await shopshop.finish(message=result)

def get_dailyshop():
    result = image("https://cdn.dingpanbao.cn/blzy/shop.png")
    if result is None or result == "":
        result = "堡垒皮肤api请求超时"
    return result