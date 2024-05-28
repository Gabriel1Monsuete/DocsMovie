import os

SECRET_KEY = 'abreu'

SQLALCHEMY_DATABASE_URI =  \
 '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
     SGBD = 'mysql+mysqlconnector',
     usuario = 'root',
     senha = 'Monsuete10',
     servidor = 'localhost',
     database = 'DOCSMOVIE'
 )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
