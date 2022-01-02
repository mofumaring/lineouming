import json
from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
import os

file = open('information.json', 'r')
info = json.load(file)

app=Flask(__name__)
#環境変数の取得
CHANNEL_ACCESS_TOKEN = information['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET = information['CHANNEL_SECRET']
line_bot_api=LineBotApi(CHANNEL_ACCESS_TOKEN)
handler=WebhookHandler(CHANNEL_SECRET)

@app.route("/callback",methods=["POST"])
def callback():
    signature=request.headers["X-Line-Signature"]

    body=request.get_data(as_text=True)
    app.logger.info("Request body"+body)

    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

def main():
    USER_ID = info['USER_ID']
    messages = TextSendMessage(text="～アップデート～  \n リプに対してオウム返しできるようになりました！同じ言葉を返してくれるか是非試してみてください。")
    line_bot_api.push_message(USER_ID, messages=messages)    

if __name__=="__main__":
    main()
    port=int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0",port=port)
