import requests
from config.settings import WEBHOOK_URL
from datetime import datetime, timedelta, timezone


class WeChatNotifier:
    def send_report(self, group_name, content):
        if not content:
            return

        # 获取北京时间
        beijing_time = datetime.now(timezone(timedelta(hours=8))).strftime('%m-%d %H:%M')

        # 组装纯文本消息内容
        # 纯文本模式下，Markdown 的语法（如 **加粗**）会直接显示为符号，不影响阅读
        final_msg = f"【🕵️‍♂️ 链上研报 | {group_name}】\n"
        final_msg += f"生成时间: {beijing_time}\n"
        final_msg += "------------------------------\n"
        final_msg += content

        headers = {"Content-Type": "application/json"}

        # --- 核心修改：改为 text 类型 ---
        data = {
            "msgtype": "text",
            "text": {
                "content": final_msg,
                # 如果你想提醒所有人，可以取消下面这行的注释
                # "mentioned_list": ["@all"]
            }
        }
        # ---------------------------

        try:
            resp = requests.post(WEBHOOK_URL, json=data, headers=headers)
            # 打印结果方便调试
            if resp.status_code == 200 and resp.json().get('errcode') == 0:
                print(f"✅ [{group_name}] 文本报告已推送")
            else:
                print(f"❌ 推送失败: {resp.text}")

        except Exception as e:
            print(f"Network Error sending to WeChat: {e}")