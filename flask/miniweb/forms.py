from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[Email('Некорректный email')])
    psw = PasswordField('Пароль', validators=[DataRequired(),
                                              Length(min=4, max=100, message='Пароль должен содержать от 4 символов')])
    remember = BooleanField('Запомнить', default=False)
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    name = StringField('Имя: ', validators=[Length(min=4, max=100, message='Имя должно содержать не менее 4 символов')])
    email = StringField('Email: ',
                        validators=[Length(min=4, max=100, message='Email должен содержать не менее 4 символов')])
    psw = PasswordField('Пароль:', validators=[DataRequired(), Length(min=4, max=100,
                                                                      message='Пароль должен содержать не менее 4 символов')])
    psw2 = PasswordField('Повтор пароля :', validators=[DataRequired(), EqualTo('psw', message='Пароли не совпадают')])
    submit = SubmitField('Регистрация')
