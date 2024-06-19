from flask import render_template, url_for, redirect
from picline import app, database, bcrypt
from picline.models import Usuario, Foto
from picline.forms import FormLogin, FormCriarConta, FormFoto
from flask_login import login_required, login_user, logout_user, current_user
import os
from werkzeug.utils import secure_filename
import uuid


@app.route("/", methods=['GET', 'POST'])
def homepage():
    form_login = FormLogin()

    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha.encode("utf-8"), form_login.senha.data):
            login_user(usuario)
            return redirect(url_for('perfil', username=usuario.username))

    return render_template("homepage.html", form=form_login)


@app.route("/criar-conta", methods=['GET', 'POST'])
def criar_conta():
    form_criar_conta = FormCriarConta()

    if form_criar_conta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criar_conta.senha.data).decode("utf-8")
        usuario = Usuario(username=form_criar_conta.username.data, nome=form_criar_conta.nome.data,
                          email=form_criar_conta.email.data, senha=senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for('perfil', username=usuario.username))

    return render_template("criarconta.html", form=form_criar_conta)


@app.route("/perfil/<username>", methods=['GET', 'POST'])
@login_required
def perfil(username):
    usuario = Usuario.query.filter_by(username=username).first()
    if int(usuario.id) == int(current_user.id):
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            _, extensao = os.path.splitext(arquivo.filename)
            nome_uuid = str(uuid.uuid4())
            nome_seguro = secure_filename(nome_uuid + extensao)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        return render_template("perfil.html", usuario=usuario, form=None)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()[:50]
    return render_template("feed.html", fotos=fotos)


@app.route("/excluir-imagem/<id_imagem>", methods=["GET"])
@login_required
def excluir_imagem(id_imagem):
    foto = Foto.query.get_or_404(id_imagem)
    if foto and foto.id_usuario == current_user.id:
        database.session.delete(foto)
        database.session.commit()
        nome_arquivo = foto.imagem
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config["UPLOAD_FOLDER"], nome_arquivo)
        if os.path.exists(caminho):
            os.remove(caminho)
        return redirect(url_for("perfil", username=current_user.username))

