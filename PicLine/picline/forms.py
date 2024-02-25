from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from picline.models import Usuario


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    botao_confirmacao = SubmitField('Entrar')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError('Este e-mail não está relacionado a nenhuma conta. Crie uma conta')


class FormCriarConta(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    nome = StringField('Nome', validators=[DataRequired(), Length(min=5)])
    username = StringField('Nome de usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=20)])
    confirmacao_senha = PasswordField('Confirmação de senha', validators=[DataRequired(), EqualTo('senha')])
    botao_confirmacao = SubmitField('Criar conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Faça login para continuar')

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Esse nome de usuário já está sendo utilizado')


class FormFoto(FlaskForm):
    foto = FileField('Imagem', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    botao_confirmacao = SubmitField('Postar')

