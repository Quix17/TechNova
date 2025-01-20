from flask import render_template
from flask import Flask

app = Flask(__name__)

def register_blogposts(app):
    @app.route('/')
    def index():
        return render_template('KI/ai-projekt.html')

    @app.route('/blogpost1')
    def blogpost1():
        return render_template('KI/blogpost1.html')

    @app.route('/blogpost2')
    def blogpost2():
        return render_template('KI/blogpost2.html')

    @app.route('/blogpost3')
    def blogpost3():
        return render_template('KI/blogpost3.html')
