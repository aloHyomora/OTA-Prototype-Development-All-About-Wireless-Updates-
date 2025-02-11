from flask import Flask, Blueprint

# BluePrint 객체 생성 params: blueprint Name, module Name
auth_blueprint = Blueprint('auth', __name__)

# 블루프린트를 사용하여 라우트 정의
@auth_blueprint.route('/login')
def login():
    return '로그인 페이지입니다.'

@auth_blueprint.route('/logout')
def logout():
    return '로그아웃 페이지입니다.'

app = Flask(__name__)

# 블루 프린트 등록
app.register_blueprint(auth_blueprint, url_prefix='/auth')