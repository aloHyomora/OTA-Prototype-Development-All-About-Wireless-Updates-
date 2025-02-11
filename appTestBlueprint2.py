from flask import Flask
from auth.views import auth_blueprint
from main.views import main_blueprint

app = Flask(__name__)

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(main_blueprint, url_prefix='/')

@app.route('/welcome')
def welcome():
    return '환영합니다! 이것은 블루프린트를 사용하지 않는 직접적인 라우트입니다.'