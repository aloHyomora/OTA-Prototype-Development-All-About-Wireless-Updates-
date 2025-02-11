from flask import Flask
import logging

app = Flask(__name__)

# 로그 레벨을 DEBUG로 설정합니다.
app.logger.setLevel(logging.DEBUG)

# 로그를 파일로 저장합니다. 추가적으로 날짜와 시간, 로그 레벨도 포함하도록 합니다.
logging.basicConfig(filename='application.log', level=logging.DEBUG, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

@app.route('/')
def home():
    # 다른 레벨 로그 테스트
    app.logger.debug('Debug level log')
    app.logger.info('info level log')
    app.logger.warning('warning level log')
    app.logger.error('Error level log')
    app.logger.critical('Critical level log')
    return 'Hello World!'