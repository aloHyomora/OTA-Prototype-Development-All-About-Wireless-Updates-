from flask import Flask, render_template
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE':'simple'})

@app.route('/')
@cache.cached(timeout=60) # 결과를 60초 동안 캐시합니다.
def index():
    return render_template('index.html')