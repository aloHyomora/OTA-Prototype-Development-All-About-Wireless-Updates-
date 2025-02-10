from flask import Flask, url_for, redirect

app = Flask(__name__)

# 홈페이지
@app.route('/')
def index():
    return f'홈페이지: {url_for("index")}'

# 사용자 프로필 페이지
@app.route('/user/<username>')
def user_profile(username):
    return f'{username}의 프로필 페이지: {url_for("user_profile", username=username)}'

# 정적 파일 테스트를 위한 경로
@app.route('/static-example')
def static_example():
    return f'정적 파일 URL: {url_for("static", filename="style.css")}'

# 절대 URL 테스트
@app.route('/absolute')
def absolute():
    return f'외부 절대 URL: {url_for("index", _external=True)}'

@app.route('/https')
def https():
    return f'HTTPS 절대 URL: {url_for("index", _scheme="https", _external=True)}'