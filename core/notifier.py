import requests
from datetime import datetime, timedelta, timezone


class WeChatNotifier:

    def send_report(self, group_name, content, webhook_url):
        if not content or not webhook_url:
            print(f"⚠️ 跳过推送: 内容为空或 Webhook 未配置 ({group_name})")
            return

        beijing_time = datetime.now(timezone(timedelta(hours=8))).strftime('%m-%d %H:%M')

        final_msg = f"【🕵️‍♂️ 链上研报 | {group_name}】\n"
        final_msg += f"生成时间: {beijing_time}\n"
        final_msg += "------------------------------\n"
        final_msg += content

        headers = {"Content-Type": "application/json"}
        data = {
            "msgtype": "text",
            "text": {"content": final_msg}
        }

        try:
            resp = requests.post(webhook_url, json=data, headers=headers)
            if resp.status_code == 200 and resp.json().get('errcode') == 0:
                print(f"✅ [{group_name}] 推送成功")
            else:
                print(f"❌ 推送失败: {resp.text}")
        except Exception as e:
            print(f"❌ 网络错误: {e}")