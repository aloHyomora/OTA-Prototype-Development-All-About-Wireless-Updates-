""" This is the appTestMySQL module for Flask and SQLAlchemy """
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:Skinova0326!@localhost/db_name'  # DB 설정
db = SQLAlchemy(app)

class User(db.Model):
    """ SQLAlchemy model for the User table """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    

# 애플리케이션 컨텍스트 안에서 DB 테이블을 생성합니다. 
with app.app_context():
    # db.create_all() 메서드는 모델에 정의된 모든 테이블을 데이터베이스에 생성합니다.
    db.create_all()

# 라우트 정의
@app.route('/')
def index():
    #데이터 생성
     new_user = User(username='john', email='john@example.com')
     db.session.add(new_user)
     db.session.commit()

     # 데이터 조회(Read)
     user = User.query.filter_by(username='john').first()

     # 데이터 업데이트(Update)
     user.email = 'john@newexample.com'
     db.session.commit()

     # 데이터 삭제
     db.session.delete(user)
     db.session.commit()

     return 'CRUD(Create, Read, Update, Delete) operations completed'SQLAlchemy