import os
import logging
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# TOKEN
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise RuntimeError("TOKEN not set!")

# Application v20 (KHÔNG DÙNG Updater nữa)
application = Application.builder().token(TOKEN).build()

# /start handler
async def start(update: Update, context):
    keyboard = [[InlineKeyboardButton("🎮 Chơi Tiến Lên Miền Nam", web_app={"url": "https://tienlen-miniapp.netlify.app"})]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎉 **CHÀO BẠN!**\n\nBấm nút để chơi Tiến Lên Miền Nam ngay!",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Handler khác
async def unknown(update: Update, context):
    await update.message.reply_text("Gõ /start để chơi nhé!")

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, unknown))

@app.route("/")
def index():
    return "<h1>🚀 TIẾN LÊN BOT V2 LIVE!</h1><p><a href='/setwebhook'>Set Webhook</a></p>"

@app.route("/setwebhook")
def set_webhook():
    url = f"https://{request.host}/webhook"
    try:
        application.bot.set_webhook(url=url)
        return f"<h1>✅ WEBHOOK SET: {url}</h1>"
    except Exception as e:
        return f"<h1>❌ ERROR: {e}</h1>"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        if update:
            asyncio.run(application.process_update(update))
        return "OK", 200
    except Exception as e:
        logger.error(f"Error: {e}")
        return "ERROR", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
