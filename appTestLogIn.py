# 필요한 모듈들을 임포트합니다.
from collections import UserDict
from flask import Flask, request, redirect, url_for, session # 웹 애플리케이션과 세션 관리
from flask_sqlalchemy import SQLAlchemy # ORM을 위한 플라스크 확장
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user

# 플라스크 애플리케이션 인스턴스를 생성합니다.
app = Flask(__name__)

# 데이터베이스 설정을 애플리케이션 설정에 추가합니다. 여기서는 MySQL을 사용하고 있습니다.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:Skinova0326!@localhost/flaskdb'
# SQLAlchemy의 수정 추적 기능을 비활성화합니다. (성능상의 이유로 권장됩니다.)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 세션 및 쿠키에 대한 보안 향상을 위해 필요한 비밀 키를 설정합니다. Flask 애플리케이션을 위한 비밀 키 설정
app.config['SECRET_KEY'] = 'mysecretkey'

# SQLAlchemy 인스턴스 생성하고 애플리케이션에 바인딩합니다.
db = SQLAlchemy(app) 

login_manager = LoginManager()  # Flask-Login의 LoginManager 인스턴스 생성
login_manager.init_app(app)     # 애플리케이션에 LoginManager 적용
login_manager.login_view = 'login' # 로그인 페이지의 뷰 함수 이름을 설정합니다.

# 데이터베이스 모델을 정의합니다. UserMixin은 Flask-Login에서 제공되는 기본 사용자 모델입니다.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)    # 사용자의 ID, 고유 식별자
    username = db.Column(db.String(80), unique=True, nullable=False) # 사용자 이름, 고유해야 함.
    email = db.Column(db.String(120), unique=True, nullable=False) # 사용자 이메일, 고유해야 함.
    password = db.Column(db.String(128))    # 사용자 비밀번호

    def __repr__(self):
        return f'<User {self.username}>'
    
# 애플리케이션 컨텍스트 안에서 데이터베이스 테이블 생성
with app.app_context():
    db.create_all()

# 사용자 ID로 사용자를 로드하는 콜백 함수를 정의합니다.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # 주어진 사용자 ID에 해당하는 사용자 객체를 반환

# 인덱스 뷰를 정의합니다. '/' 경로로 접근할 경우 실행됩니다.
@app.route('/')
def index():
    user_id = session.get('user_id')    # 세션에서 user_id를 가져옵니다.
    if user_id:
        user = User.query.get(user_id)
        return f'Logged in as {user.username}'

    return 'You are not logged in'

# 보호된 페이지를 위한 뷰를 정의합니다. 이 페이지는 로그인이 필요합니다.
@app.route('/protected')
@login_required # 로그인이 필요하다는 데코레이터입니다. 로그인한 사용자만 접근 가능합니다.
def protected():
    return f'Logged in as {current_user.username}'  # 현재 로그인한 사용자의 이름을 표시

# 로그인 뷰를 정의합니다. GET과 POST 메서드를 모두 처리합니다.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 폼 데이터로부터 사용자 이름과 비밀번호를 가져옵니다.
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()  # 데이터베이스에서 사용자 조회

        if user and user.password == password:  # 사용자가 존재하고 비밀번호가 맞다면 로그인 처리
            login_user(user)   
            session['user_id'] = user.id    # 세션에 user_id를 저장합니다.
            return redirect(url_for('protected'))   # 보호된 페이지로 리디렉션
        
    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''
# 로그아웃 뷰를 정의합니다. 
@app.route('/logout')
@login_required # 로그인이 필요하다는 데코레이터입니다.
def logout():
    logout_user()   # 현재 사용자 로그아웃 처리
    session.pop('user_id', None) # 세션에서 user_id를 제거합니다. 
    return redirect(url_for('index'))   # 인덱스 페이지로 리다이렉트합니다.

# 테스트 사용자를 생성하는 뷰를 정의합니다.
@app.route('/create_test_user')
def create_test_user():
    # 테스트 사용자 생성
    test_user = User(username='testuser', email='test@example.com', password='testpassword')

    db.session.add(test_user)    
    db.session.commit() # DB에 테스트 사용자 추가
    return 'Test user created'  # 사용자 생성 완료 메세지 반환
