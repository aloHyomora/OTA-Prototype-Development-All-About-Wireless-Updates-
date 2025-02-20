from flask import Flask, render_template, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)

# 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://flaskuser:Skinova0326!@localhost/my_memo_app'
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)

# 데이터 모델 정의
class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return f'<Memo {self.title}>'

# 로그인 기능 초기화
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # 로그인 페이지의 뷰 함수 이름

# 사용자 모델을 정의하고 데이터베이스 스키마에 반영
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(512))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Flask-Login이 현재 로그인한 사용자를 로드할 수 있도록 사용자 로딩 함수 정의
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 회원 가입 기능
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'Account created successfully'}), 201
    return render_template('singup.html')

# 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return jsonify({'message':'Logged in successfully'}), 200
        return abort(401, description="Invalid credentials")
    return render_template('login.html')

# 로그아웃
@app.route('/logout', methods=['GET'])
def logout():
    if current_user.is_authenticated:  # 로그인된 사용자만 로그아웃 처리
        logout_user()
        return jsonify({'message': 'Logged out successfully'}), 200
    return jsonify({'error': 'No user is logged in'}), 400

# 기존 라우트
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return '이것은 마이 메모 앱의 소개 페이지입니다.'

# 데이터베이스 생성
with app.app_context():
    db.create_all()

# 메모 생성
@app.route('/memos/create', methods=['POST'])
def create_memo():
    title = request.json['title']
    content = request.json['content']
    new_memo = Memo(title=title, content=content)
    db.session.add(new_memo)
    db.session.commit()
    return jsonify({'message': 'Memo created!'}), 201

# 메모 조회
@app.route('/memos', methods=['GET'])
def list_memos():
    memos = Memo.query.all()
    return jsonify([{'id': memo.id, 'title' : memo.title, 'content':memo.content} for memo in memos]), 200

# 메모 업데이트
@app.route('/memos/update/<int:id>', methods=['PUT'])
def update_memo(id):
    memo = Memo.query.filter_by(id=id).first()

    if memo:
        memo.title = request.json['title']
        memo.content = request.json['content']
        db.session.commit()
        return jsonify({'message':'Memo updated'}), 200
    else:
        abort(404, description="Memo not found")

# 메모 삭제
@app.route('/memos/delete/<int:id>', methods=['DELETE'])
def delete_memo(id):
    memo = Memo.query.filter_by(id=id).first()
    if memo:
        db.session.delete(memo)
        db.session.commit()
        return jsonify({'message':'Memo deleted'}), 200
    else:
        abort(404, description="Memo not found")