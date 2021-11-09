from flask import Flask, render_template
from utils.view_modifiers import response

app = Flask(__name__)

def get_films():
    return [
        {
            'id': ' 1 ',
            'title': 'название фильма первого',
            'release_date': 'дата выхода '
        },
        {
            'id': ' 2 ',
            'title': 'название фильма второго',
            'release_date': 'дата выхода '
        },
    ]

@app.route('/')
@app.route('/hello')
@response(template_file='hello.html')
def hello():
    films = get_films()
    return {'films': films}

@app.route('/about')
def about():
    return render_template('about.html', title='abaut')

@app.route('/<string:name>')
def greting(name: str):
    return f'Hello , {name.capitalize()}'

if __name__ == '__main__':
    app.run()
