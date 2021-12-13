from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g, make_response
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required
from UserLogin import UserLogin

from FDataBase import FDataBase

DATABASE = '/data/flsite.db'
DEBUG = True
SECRET_KEY = 'dfdf6x655xcbd7sdf5d'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, dbase)

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.db', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


# menu = [{'name': 'Установка', 'url': 'install-flask'},
#         {'name': 'Первое приложение', 'url': 'first-app'},
#         {'name': 'Обратная связь', 'url': 'contact'}
#         ]

dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.route('/')
def index():
    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostsAnonce())


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/add_post', methods=['POST', 'GET'])
def addPost():
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('Ошибка добавления статьи ', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')
    return render_template('add_post.html', menu=dbase.getMenu(), title='Добавить статью')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
                and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], request.form['email'], hash)
            if res:
                flash('Вы успешно зарегистрированы ', category='success')
                return redirect(url_for('login'))
            else:
                flash('Ошибка при добавлении в БД', category='error')
        else:
            flash('Неверно заполнены поля ', category='error')
    return render_template('register.html', menu=dbase.getMenu(), title='Регистрация')


@app.route('/post/<alias>')
@login_required
def showPost(alias):
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)
    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)




@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('index'))
        flash('Неверная пара логин/пароль', 'error')

    return render_template('login.html', menu=dbase.getMenu(), title='Авторизация')





# @app.route('/about')
# def about():
#     print(url_for('about'))
#     return render_template('about.html', title='О сайте', menu=menu)


# @app.route('/profile/<username>')
# def profile(username, path):
#     return f'Ползователь: {username}, {path}'

# @app.route('/contact', methods=['POST', 'GET'])
# def contact():
#     if request.method == 'POST':
#         if len(request.form['username']) > 2:
#             flash('Сообшение отправлено', category='success')
#         else:
#             flash('Ошибка отправки', category='error')
#
#     return render_template('contact.html', title='Обратная связь', menu=menu)
#
#
# @app.errorhandler(404)
# def pageNotFount(error):
#     return render_template('page404.html', title='Страница не найдена', menu=menu), 404
#
#
# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if 'userLogged' in session:
#         return redirect(url_for('profile', username=session['userLogged']))
#     elif request.method == 'POST' and request.form['username'] == 'user' and request.form['psw'] == '123':
#         session['userLogged'] = request.form['username']
#         return redirect(url_for('profile', username=session['userLogged']))
#     return render_template('login.html', title='Авторизация', menu=menu)
#

# cookies
# @app.route('/login')
# def login():
#     log = ' '
#     if request.cookies.get('logged'):
#         log = request.cookies.get('logged')
#
#     res = make_response(f'<h1>Форма аторизации</h1><p>logged:{log}')
#     res.set_cookie('logged', 'yes', 30*24*3600)
#     return res
#
# @app.route('/logout')
# def logout():
#     res = make_response('<p>Вы больше не авторизированны! </p> ')
#     res.set_cookie('logged', '', 0)
#     return res

#
# @app.route('/profile/<username>')
# def profile(username):
#     if 'userLogged' not in session or session['userLogged'] != username:
#         abort(401)
#     return f'Профиль пользователя: {username}'

#
# # with app.test_request_context():
# #     print(url_for('index'))
# #     print(url_for('about'))
# #     print(url_for('profile', username='selfedu'))
#
if __name__ == "__main__":
    app.run(debug=True)
