from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user

app = Flask(__name__)

# 데이터베이스 설정 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:Skinova0326!@localhost/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Flask 애플리케이션을 위한 비밀 키 설정
app.config['SECRET_KEY'] = 'mysecretkey'

db = SQLAlchemy(app) # SQLAlchemy 인스턴스 생성

login_manager = LoginManager()  # Flask-Login의 LoginManager 인스턴스 생성
login_manager.init_app(app)     # 애플리케이션에 LoginManager 적용
login_manager.login_view = 'login' # 로그인 페이지의 뷰 함수 이름을 설정합니다.

# 사용자 모델 정의
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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # 주어진 사용자 ID에 해당하는 사용자 객체를 반환

@app.route('/')
def index():
    return 'Home Page'

@app.route('/protected')
@login_required # 로그인한 사용자만 액세스 가능
def protected():
    return f'Logged in as {current_user.username}'  # 현재 로그인한 사용자의 이름을 표시

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()  # 데이터베이스에서 사용자 조회

        if user and user.password == password:  # 사용자가 존재하고 비밀번호가 맞다면 로그인 처리
            login_user(user)   

            return redirect(url_for('protected'))   # 보호된 페이지로 리디렉션
        
    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
@login_required # 로그인한 사용자만 액세스 가능
def logout():
    logout_user()   # 현재 사용자 로그아웃 처리
    return redirect(url_for('index'))

@app.route('/create_test_user')
def create_test_user():
    # 테스트 사용자 생성
    test_user = User(username='testuser', email='test@example.com', password='testpassword')

    db.session.add(test_user)    
    db.session.commit() # DB에 테스트 사용자 추가
    return 'Test user created'  # 사용자 생성 완료 메세지 반환
