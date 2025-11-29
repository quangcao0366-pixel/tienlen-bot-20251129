import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>🚀 TIẾN LÊN BOT LIVE! Deploy OK</h1>'

@app.route('/health')
def health():
    return jsonify({'status': 'OK', 'port': os.environ.get('PORT', '5000')})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
