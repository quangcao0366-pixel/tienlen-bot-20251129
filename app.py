import os
import logging
import asyncio
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# TOKEN từ Environment Variables
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    app.logger.error("❌ TOKEN environment variable not set!")
    raise RuntimeError("TOKEN not set!")

# Tạo Telegram Application
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /start"""
    keyboard = [
        [InlineKeyboardButton("🎮 Chơi Tiến Lên Miền Nam", web_app={"url": "https://tienlen-miniapp.netlify.app"})]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        "🎉 **CHÀO BẠN ĐẾN VỚI TIẾN LÊN BOT!**\n\n"
        "👆 **Bấm nút bên dưới** để **chơi Tiến Lên Miền Nam** ngay!\n\n"
        "✨ **Tính năng:**\n"
        "• 🎯 Game mượt mà, không lag\n"
        "• 👥 Chơi với bạn bè\n"
        "• 🎨 Giao diện đẹp mắt\n"
        "• 🚫 Không quảng cáo\n\n"
        "🚀 **Bắt đầu chơi ngay!**"
    )
    
    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /help"""
    help_text = (
        "🆘 **HƯỚNG DẪN SỬ DỤNG**\n\n"
        "📋 **Lệnh có sẵn:**\n"
        "• `/start` - Bắt đầu chơi\n"
        "• `/help` - Hiển thị hướng dẫn\n\n"
        "🎮 **Cách chơi:**\n"
        "1. Gõ `/start`\n"
        "2. Bấm **'Chơi Tiến Lên Miền Nam'**\n"
        "3. Thưởng thức game! 🎉"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý tin nhắn khác"""
    await update.message.reply_text(
        "🎮 **Gõ `/start` để bắt đầu chơi!**\n\n"
        "👇 Bấm nút bên dưới:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎮 Bắt đầu chơi", callback_data="start_game")]
        ])
    )

# Đăng ký handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>🚀 Tiến Lên Bot V2</title></head>
    <body style="font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
        <h1>🚀 TIẾN LÊN BOT V2 - LIVE!</h1>
        <p><strong>Service:</strong> tienlen-bot-20251129</p>
        <p><strong>Status:</strong> ✅ Telegram Bot Ready!</p>
        <p>
            <a href="/health" style="color: white; padding: 10px 20px; background: #48bb78; text-decoration: none; border-radius: 5px;">🔍 Health Check</a>
            <a href="/setwebhook" style="color: white; padding: 10px 20px; background: #ed8936; text-decoration: none; border-radius: 5px; margin-left: 10px;">🔗 Set Webhook</a>
        </p>
        <hr>
        <p><strong>🎉 Bot đã sẵn sàng! Thử gõ <code>/start</code> trong Telegram</strong></p>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return jsonify({
        'status': 'OK',
        'service': 'tienlen-bot-20251129',
        'bot': 'ready',
        'token': 'configured' if TOKEN else 'missing',
        'webhook': 'ready'
    })

@app.route('/setwebhook', methods=['GET'])
def set_webhook():
    """Cài đặt webhook"""
    webhook_url = f"https://{request.host}/webhook"
    
    async def _set():
        await application.bot.set_webhook(url=webhook_url)
        info = await application.bot.get_webhook_info()
        return info
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        webhook_info = loop.run_until_complete(_set())
        loop.close()
        
        return f'''
        <!DOCTYPE html>
        <html><head><title>Webhook Success</title></head>
        <body style="font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #48bb78, #38a169); color: white;">
            <h1>✅ WEBHOOK CÀI ĐẶT THÀNH CÔNG!</h1>
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;">
                <p><strong>🔗 Webhook URL:</strong></p>
                <code style="background: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px; display: block; word-break: break-all; margin: 10px 0;">
                    {webhook_url}
                </code>
                <p><strong>📊 Pending updates:</strong> {webhook_info.pending_update_count}</p>
            </div>
            <p><strong>🎉 Bot đã sẵn sàng! Thử gõ <code>/start</code> trong Telegram ngay!</strong></p>
            <a href="/" style="color: white; text-decoration: none; padding: 12px 24px; background: rgba(255,255,255,0.2); border-radius: 25px;">🏠 Trang chủ</a>
        </body></html>
        '''
    except Exception as e:
        return f'''
        <h1 style="color: red;">❌ Lỗi Webhook: {str(e)}</h1>
        <p>Đảm bảo đã thêm TOKEN trong Environment Variables</p>
        <a href="/">🏠 Trang chủ</a>
        '''

@app.route('/webhook', methods=['POST'])
def webhook():
    """Nhận updates từ Telegram"""
    try:
        json_data = request.get_json(force=True)
        if not json_data:
            return 'No data', 200
        
        update = Update.de_json(json_data, application.bot)
        if update:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(application.process_update(update))
            finally:
                loop.close()
        
        return 'OK', 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return 'ERROR', 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
