from flask import Flask, request, jsonify

app = Flask(__name__)
user_data = {}  # 딕셔너리로 사용자 데이터를 저장합니다.

@app.route('/user/<username>', methods=['GET','POST','PUT','DELETE'])
def manage_user(username=None):
    global user_data # 전역 변수 user_data 사용

    if request.method == 'GET':
        return jsonify({username: user_data.get(username, "Not found")})
    
    elif request.method =='POST':
        new_data = request.json # JSON 형태의 데이터를 받습니다.
        user_data[username] = new_data
        return jsonify(new_data), 201
    
    elif request.method == 'PUT':
        update_data = request.json
        if username in user_data:
            user_data[username].update(update_data)
            return jsonify(update_data)
        else:
            return jsonify({"error": "username not found"}), 404
        
    elif request.method == 'DELETE':
        if username in user_data:
            del user_data[username]
            return jsonify({"result":"deleted"}), 200
        else:
            return jsonify({"error":"username not found"}),404