from flask import Flask, render_template

app = Flask(__name__)

# 메인 페이지 라우트
@app.route('/')
def home():
    return render_template('index.html')