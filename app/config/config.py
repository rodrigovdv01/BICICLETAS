class Config():
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/bicicletas'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = './static/img/'
    confirm_deleted_rows=False