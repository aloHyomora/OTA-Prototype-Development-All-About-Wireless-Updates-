from flask import Flask, request, url_for
app = Flask(__name__)

# 기본 홈페이지 경로
@app.route('/')
def index():
    # show_user_profile 뷰로 이동하는 URL을 생성합니다.
    user_url = url_for("show_user_profile", username='Alohyomora')
    # show_post 뷰로 이동하는 URL을 생성합니다.
    post_url = url_for("show_post", year='2025', month='02', day='01')
    return f'홈페이지에 오신 것을 환영합니다! User URL: {user_url}<br>Post URL: {post_url}'

@app.route("/user/<username>")
def show_user_profile(username):
    # url_for()를 사용하여 'index' 뷰 함수의 URL을 생성합니다.
    return f'''{username}님의 프로필 페이지입니다.
    홈으로 가기: {url_for("index")}'''

@app.route("/post/<year>/<month>/<day>")
def show_post(year, month, day):
    return f'Post for {year}/{month}/{day}'

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        return "Logging in..."
    else:
        return "Login Form"

if __name__ == '__main__':
    app.run(debug=True)