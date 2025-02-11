from flask import Blueprint

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login')
def login():
    return '로그인 페이지입니다.'

@auth_blueprint.route('/logout')
def logout():
    return '로그아웃 페이지입니다.'