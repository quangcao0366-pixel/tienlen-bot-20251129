import os
import logging
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# TOKEN
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise RuntimeError("❌ TOKEN environment variable not set!")

BOT_URL = f"https://api.telegram.org/bot{TOKEN}"

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>🚀 Tiến Lên Bot V2</title></head>
    <body style="font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
        <h1>🚀 TIẾN LÊN BOT V2 - LIVE!</h1>
        <p><strong>Service:</strong> tienlen-bot-20251129</p>
        <p><strong>Status:</strong> ✅ Ready!</p>
        <p><a href="/health" style="color: white; padding: 10px 20px; background: #48bb78; text-decoration: none; border-radius: 5px;">🔍 Health</a>
        <a href="/setwebhook" style="color: white; padding: 10px 20px; background: #ed8936; text-decoration: none; border-radius: 5px; margin-left: 10px;">🔗 Webhook</a></p>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return jsonify({
        'status': 'OK',
        'service': 'tienlen-bot-20251129',
        'bot': 'ready',
        'method': 'HTTP API'
    })

@app.route('/setwebhook', methods=['GET'])
def set_webhook():
    webhook_url = f"https://{request.host}/webhook"
    
    try:
        # Set webhook
        response = requests.post(f"{BOT_URL}/setWebhook", data={
            'url': webhook_url
        })
        data = response.json()
        
        if data['ok']:
            # Get webhook info
            info_response = requests.get(f"{BOT_URL}/getWebhookInfo")
            info = info_response.json()
            
            return f'''
            <!DOCTYPE html>
            <html><head><title>Webhook Success</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #48bb78, #38a169); color: white;">
                <h1>✅ WEBHOOK CÀI ĐẶT THÀNH CÔNG!</h1>
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <p><strong>🔗 Webhook URL:</strong></p>
                    <code style="background: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px; display: block; word-break: break-all;">
                        {webhook_url}
                    </code>
                    <p><strong>📊 Pending updates:</strong> {info['result']['pending_update_count']}</p>
                </div>
                <p><strong>🎉 Bot đã sẵn sàng! Thử gõ <code>/start</code> trong Telegram ngay!</strong></p>
                <a href="/" style="color: white; text-decoration: none; padding: 12px 24px; background: rgba(255,255,255,0.2); border-radius: 25px;">🏠 Trang chủ</a>
            </body></html>
            '''
        else:
            return f'<h1>❌ Set webhook failed: {data}</h1>'
            
    except Exception as e:
        return f'<h1>❌ Lỗi: {str(e)}</h1><a href="/">Trang chủ</a>'

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Nhận update từ Telegram
        update = request.get_json(force=True)
        
        if not update:
            return 'OK', 200
        
        # Xử lý message
        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            text = message.get('text', '')
            
            if text == '/start':
                # Gửi message với nút chơi game
                send_message(chat_id, 
                    "🎉 **CHÀO BẠN ĐẾN VỚI TIẾN LÊN BOT!**\n\n"
                    "👆 **Bấm nút bên dưới** để **chơi Tiến Lên Miền Nam** ngay!\n\n"
                    "✨ **Tính năng:**\n"
                    "• 🎯 Game mượt mà\n"
                    "• 👥 Chơi với bạn bè\n"
                    "• 🚫 Không quảng cáo",
                    reply_markup={
                        "inline_keyboard": [[
                            {
                                "text": "🎮 Chơi Tiến Lên Miền Nam",
                                "web_app": {"url": "https://tienlen-miniapp.netlify.app"}
                            }
                        ]]
                    }
                )
            
            elif text == '/help':
                send_message(chat_id,
                    "🆘 **HƯỚNG DẪN:**\n\n"
                    "📋 **Lệnh:**\n"
                    "• `/start` - Bắt đầu chơi\n"
                    "• `/help` - Hướng dẫn này"
                )
            
            else:
                send_message(chat_id,
                    "🎮 **Gõ `/start` để bắt đầu chơi!**"
                )
        
        return 'OK', 200
        
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return 'ERROR', 500

def send_message(chat_id, text, reply_markup=None):
    """Gửi tin nhắn qua Telegram API"""
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    
    try:
        response = requests.post(f"{BOT_URL}/sendMessage", data=data)
        return response.json()
    except Exception as e:
        logging.error(f"Send message error: {e}")
        return None

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
