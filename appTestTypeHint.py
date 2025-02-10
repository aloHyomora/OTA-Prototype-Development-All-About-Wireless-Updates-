from flask import Flask

app = Flask(__name__)

@app.route('/int/<int:var>')
def int_type(var: int):
    return f'Integer: {var}'

@app.route('/float/<float:var>')
def float_type(var: float):
    return f'Float: {var}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'Subpath: {subpath}'

@app.route('/uuid/<uuid:random_id>')
def show_uuid(random_id):
    return f'UUID: {random_id}'