from DOCSMOVIE import app
from flask import render_template, request, redirect, session, flash, url_for
from models import Usuarios
from helpers import FormularioUsuario
import bcrypt

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, form=form)



@app.route('/autenticar', methods=['POST', ])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    
    if usuario and bcrypt.checkpw(form.senha.data.encode('utf-8'), usuario.senha.encode('utf-8')):
        session['usuario_logado'] = usuario.nickname
        flash(usuario.nickname + ' logou com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout Efetuado com sucesso !')
    return redirect(url_for('index'))