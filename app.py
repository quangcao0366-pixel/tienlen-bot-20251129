import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>🚀 TIẾN LÊN BOT LIVE!</h1>
    <h2>Service: tienlen-bot-20251129</h2>
    <p><a href="/health">Health Check</a></p>
    '''

@app.route('/health')
def health():
    return jsonify({
        'status': 'OK',
        'service': 'tienlen-bot-20251129',
        'port': os.environ.get('PORT', '5000'),
        'timestamp': '2025-11-29'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
