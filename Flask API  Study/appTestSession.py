from flask import Flask, session, abort

app = Flask(__name__)
app.secret_key = 'your_secret_key' # 실제 환경에서는 안전하게 관리해야 할 정보

@app.route('/set_session')
def set_session():
    session['username'] = 'John'
    return '세션에 사용자 이름이 설정되었습니다.'

@app.route('/get_session')
def get_session():
    username = session.get('username')
    if username:
        return f'사용자 이름: {username}'
    return '사용자 이름이 세션에 설정되지 않았습니다.'

@app.route('/protected')
def protected():
    if 'username' not in session:
        abort(403)