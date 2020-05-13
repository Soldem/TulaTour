from flask import Flask, flash
from data import db_session, users
from flask import render_template
from flask_login import LoginManager, login_user
from werkzeug.utils import redirect


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/blogs.sqlite")

login_manager = LoginManager()
login_manager.init_app(app)


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(users.User).get(user_id)

@app.route('/')
def return_sample_page():
    return render_template('index.1.html')

@app.route('/index.0')
def return_index():
    return render_template('index.0.html')

@app.route('/index.2')
def return_index1():
    return render_template('index.2.html')

@app.route('/order')
def return_order():
    return render_template('order.html')

@app.route('/about')
def return_about():
    return render_template('about.html')

@app.route('/contact')
def return_contact():
    return render_template('contact.html')

@app.route('/kulikovo_pole')
def return_kulikovo_pole():
    return render_template('kulikovo_pole.html')

@app.route('/polenovo')
def return_polenovo():
    return render_template('polenovo.html')

@app.route('/jasnaya_polyana')
def return_jasnaya_polyana():
    return render_template('jasnaya_polyana.html')

@app.route('/weapon_museum')
def return_weapon_museum():
    return render_template('weapon_museum.html')

@app.route('/weapon_museum_addres')
def return_weapon_museum_addres():
    return render_template('weapon_museum_addres.html')

@app.route('/polenovo_addres')
def return_polenovo_addres():
    return render_template('polenovo_addres.html')

@app.route('/jasnaya_polyana_addres')
def return_jasnaya_polyana_addres():
    return render_template('jasnaya_polyana_addres.html')

@app.route('/kulikovo_pole_addres')
def return_kulikovo_pole_addres():
    return render_template('kulikovo_pole_addres.html')


def main():
    db_session.global_init("db/blogs.sqlite")
    app.run()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(users.User).filter(users.User.email1 == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("index.0")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
        db_session.global_init("db/blogs.sqlite")
        app.run()
