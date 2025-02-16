from flask import Flask, request

app = Flask(__name__)

@app.route('/user', methods = ['GET','POST','PUT','DELETE'])
def manage_user():
    if request.method == 'GET':
        # GET 요청 처리 로직
        return "User Data"
    elif request.method == 'POST':
        # POST 요청 처리 로직
        return "Create User"
    elif request.method == 'PUT':
        # PUT 요청 처리 로직
        return "Update User"
    elif request.method == 'DELETE':
        # DELETE 요청 처리 로직
        return "Delete User"