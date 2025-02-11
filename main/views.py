from flask import Blueprint

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def home():
    return '메인 페이지입니다.'
