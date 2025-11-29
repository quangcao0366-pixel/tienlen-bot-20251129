from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>🚀 TIẾN LÊN BOT LIVE! Tên: tienlen-bot-20251129</h1>'

@app.route('/health')
def health():
    return {'status': 'OK', 'service': 'tienlen-bot-20251129'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
