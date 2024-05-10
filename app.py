from flask import Flask, render_template
from flask_vite import Vite

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')
vite = Vite(app)


@app.route('/')
def index():
    return render_template('layout.j2')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
