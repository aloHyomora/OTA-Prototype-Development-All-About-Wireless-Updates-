from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/img/<path:filename>')
def custom_static(filename):
    return send_from_directory('static/img', filename)

# 메인 페이지 라우트
@app.route('/')
def home():
    return render_template('index.html')