# notification.py Ok
import requests
import json

WEB_HOOK_URL = "https://hooks.slack.com/services/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"

def send_notification(messages):
    formatted_messages = "\n".join(messages).replace("\n", "\\n")

    # Slackに通知
    requests.post(WEB_HOOK_URL, data=json.dumps({
        'text': f'Notification From Python:\n{formatted_messages}',  # 各メッセージを改行して表示
    }))

# このファイルを直接実行した時だけ通知する場合
if __name__ == "__main__":
    send_notification(["This is a test notification."])