from DOCSMOVIE import db


class Plataformas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)


class Filmes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    sinopse = db.Column(db.String(500), nullable=False)
    plataforma_id = db.Column(db.Integer, db.ForeignKey('plataformas.id'), nullable=False)
    plataforma = db.relationship('Plataformas', backref=db.backref('filmes', lazy=True))

    def __repr__(self):
        return '<Name %r>' % self.nome


class Usuarios(db.Model):
    nickname = db.Column(db.String(10), primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.nome
