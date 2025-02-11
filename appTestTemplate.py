from flask import Flask, render_template

app = Flask(__name__)

@app.route('/hello/<name>')
def hello_name(name):
    return render_template('hello.html', name=name)

@app.route('/fruits')
def show_fruits():
    fruits = ['Apple', 'Banana','Grape','Cherry',]
    return render_template('fruits_list.html', fruits=fruits)