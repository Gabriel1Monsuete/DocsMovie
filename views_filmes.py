from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from DOCSMOVIE import app, db
from models import Filmes, Plataformas
from sqlalchemy import or_
from helpers import recupera_imagem, deleta_arquivo, FormularioFilme
import time
import bcrypt

@app.route('/')
def index():
    lista = Filmes.query.order_by(Filmes.id)
    return render_template('lista.html', titulo='Filmes', filmes=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioFilme()
    plataformas = Plataformas.query.all()  # Obter todas as plataformas
    return render_template('novo.html', titulo='Novo Filme', form=form, plataformas=plataformas)

@app.route('/criar', methods=["POST"])
def criar():
    form = FormularioFilme(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    sinopse = form.sinopse.data
    plataforma_id = form.plataforma.data  # Obter o ID da plataforma selecionada

    filme = Filmes.query.filter_by(nome=nome).first()

    if filme:
        flash('Filme já existente !')
        return redirect(url_for('index'))

    novo_filme = Filmes(nome=nome, sinopse=sinopse, plataforma_id=plataforma_id)  # Usar o ID da plataforma
    db.session.add(novo_filme)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_filme.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    filme = Filmes.query.filter_by(id=id).first()
    form = FormularioFilme()
    form.nome.data = filme.nome
    form.sinopse.data = filme.sinopse
    form.plataforma.data = filme.plataforma_id  # Usar o ID da plataforma
    capa_filme = recupera_imagem(id)
    plataformas = Plataformas.query.all()  # Obter todas as plataformas
    return render_template('editar.html', titulo='Editando Filme', id=id, capa_filme=capa_filme, form=form, plataformas=plataformas)

@app.route('/atualizar', methods=["POST"])
def atualizar():
    form = FormularioFilme(request.form)

    if form.validate_on_submit():
        filme = Filmes.query.filter_by(id=request.form['id']).first()
        filme.nome = form.nome.data
        filme.sinopse = form.sinopse.data
        filme.plataforma_id = form.plataforma.data  # Usar o ID da plataforma

        db.session.add(filme)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(filme.id)
        arquivo.save(f'{upload_path}/capa{filme.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    
    Filmes.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Filme apagado com sucesso !')

    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

@app.route('/pesquisar')
def pesquisar():
    query = request.args.get('query')

    if query:
        resultados = Filmes.query.join(Plataformas).filter(or_(
            Filmes.nome.ilike(f"%{query}%"),
            Filmes.sinopse.ilike(f"%{query}%"),
            Plataformas.nome.ilike(f"%{query}%")  # Pesquisar também pelo nome da plataforma
        )).all()
    else:
        resultados = Filmes.query.all()

    return render_template('lista.html', titulo='Filmes', filmes=resultados)

if __name__ == "__main__":
    app.run(debug=True)
