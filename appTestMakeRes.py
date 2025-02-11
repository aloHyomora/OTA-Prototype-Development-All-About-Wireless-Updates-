from flask import Flask, make_response

app = Flask(__name__)

@app.route('/response')
def response_example():
    # 응답 객체를 생성, 응답 바디, HTTP 상태 코드 설정
    resp = make_response("Hello with header", 200)
    # 사용자 정의 헤더 작성
    resp.headers['Custom-Header'] = 'custom-value'
    return resp