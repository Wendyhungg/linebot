from flask import Flask, request, abort
from linebot import ( LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import os
from dotenv import load_dotenv #使用.env文件需要加載的
from function import *

load_dotenv() # 加入 .env 文件中的環境變數
app = Flask(__name__)

# 使用os獲取環境變數的值
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 檢查環境變數有無設置成功
if LINE_CHANNEL_SECRET is None or LINE_CHANNEL_ACCESS_TOKEN is None:
    print("環境變數設置未成功")
else:
    print("成功")

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    if '麻辣鍋' in user_message:
        message = FlexTemplate1()
        line_bot_api.reply_message(event.reply_token, message)
    elif '石頭火鍋' in user_message:
        message = FlexTemplate2()
        line_bot_api.reply_message(event.reply_token, message)

    
    
if __name__=="__main__":
    port = int(os.environ.get('PORT', 2000))
    app.run(host='0.0.0.0', port=port,debug=True)