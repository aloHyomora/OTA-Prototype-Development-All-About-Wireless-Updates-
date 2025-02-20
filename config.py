class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://otauser:Skinova0326!@localhost/ota_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secretkey'  # JWT 또는 세션 사용 시 필요