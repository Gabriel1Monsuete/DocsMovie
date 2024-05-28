import mysql.connector
from mysql.connector import errorcode
import bcrypt
import os 
from dotenv import load_dotenv

load_dotenv()

print('Conectando...')

try:
    conn = mysql.connector.connect(
        host='DB_HOST',
        user='DB_USER',
        password='DB_PASSWORD'
    )

    

except mysql.connector.Error as err:
    if err.errno == errorcode.ERACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)
else:
    print('Conectado')

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS DOCSMOVIE;")

cursor.execute("CREATE DATABASE DOCSMOVIE;")

cursor.execute("USE DOCSMOVIE")

# criando tabelas
TABLES = {}

TABLES['Plataformas'] = ('''
    CREATE TABLE `DOCSMOVIE`.`plataformas` (
      `id` INT NOT NULL AUTO_INCREMENT,
      `nome` VARCHAR(20) NOT NULL,
      PRIMARY KEY (`id`))
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8
    COLLATE = utf8_bin;''')

TABLES['Filmes'] = ('''
    CREATE TABLE `DOCSMOVIE`.`filmes` (
      `id` INT NOT NULL AUTO_INCREMENT,
      `nome` VARCHAR(50) NOT NULL,
      `sinopse` VARCHAR(500) NOT NULL,
      `plataforma_id` INT NOT NULL,
      PRIMARY KEY (`id`),
      FOREIGN KEY (`plataforma_id`) REFERENCES `plataformas` (`id`) ON DELETE CASCADE)
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8
    COLLATE = utf8_bin; ''')

TABLES['Usuarios'] = ('''
    CREATE TABLE `DOCSMOVIE`.`usuarios` (      
      `nome` VARCHAR(50) NOT NULL,
      `nickname` VARCHAR(10) NOT NULL,
      `senha` VARCHAR(100) NOT NULL,
      PRIMARY KEY (`nickname`))
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8
    COLLATE = utf8_bin;  ''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print(f'Criando tabela {tabela_nome}')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Tabela já existe')
        else:
            print(err.msg)
    else:
        print('ok')

# inserindo usuários com senhas criptografadas
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) values (%s,%s,%s)'

usuarios = [
    ("Luisandro", "L", bcrypt.hashpw("123".encode('utf-8'), bcrypt.gensalt())),
    ("Dogão", "DOG", bcrypt.hashpw("321".encode('utf-8'), bcrypt.gensalt())),
]

cursor.executemany(usuario_sql, usuarios)

# Inserindo plataformas
plataforma_sql = 'INSERT INTO plataformas (nome) VALUES (%s)'

plataformas = [
    ("Prime Video",),
    ("Netflix",),
    ("Disney Plus",),
    ("HBO Max",),
    ("Apple TV+",),
    ("Hulu",),
    ("Paramount+",),
    ("Peacock",),
    ("Discovery+",),
    ("Crunchyroll",),
    ("Funimation",),
    ("YouTube Premium",),
    ("Sling TV",),
    ("FuboTV",),
    ("Tubi",),
    ("Showtime",),
    ("Starz",),
    ("BBC iPlayer",),
    ("Rakuten Viki",),
]

cursor.executemany(plataforma_sql, plataformas)

# inserindo filmes com referência às plataformas
filme_sql = 'INSERT INTO filmes (nome, sinopse, plataforma_id) values (%s,%s,%s)'

filmes = [
    ("Minha Culpa", "Minha Culpa. Noah deixa sua cidade, namorado e amigas para se mudar para a mansão do novo marido de sua mãe. Lá conhece seu novo meio-irmão, Nick, e suas personalidades não batem desde o início.", 1),
    ("BayWatch", "O ex-atleta olímpico Matt Brody quer se juntar a uma equipe de salva-vidas de elite liderada por Mitch Buchannon. Quando as drogas e o suspeito dono de um resort ameaçam a baía, Mitch e Matt precisam colocar suas diferenças de lado e entrar em ação.", 2),
    ("Os Incríveis", "O Sr. Incrível, um ex-super-herói, vive uma vida tranquila com sua família após o governo banir superpoderes. No entanto, ele anseia por sua antiga vida de aventura. Quando um antigo inimigo ressurge, ele e sua família são obrigados a se unir para derrotá-lo e proteger o mundo mais uma vez.", 3),
    ("Operação Big Hero", "O grande robô inflável está sempre a postos para cuidar de Hiro Hamada. Quando algo devastador assola a cidade, o menino prodígio, seus amigos e o robô formam um grupo de heróis para combater o mal.", 3),
]

cursor.executemany(filme_sql, filmes)

cursor.execute('select * from DOCSMOVIE.filmes')
print('---------------- Filmes ----------------')
for filme in cursor.fetchall():
    print(filme[1])

# commitando pra gravar no banco
conn.commit()

cursor.close()
conn.close()
