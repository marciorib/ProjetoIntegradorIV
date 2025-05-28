from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/leitura')
def leitura():
    return render_template('leitura.html')

@app.route('/impressao')
def impressao():
    return render_template('impressao.html')

@app.route('/listagem')
def listagem():
    return render_template('listagem.html')

if __name__ == '__main__':
    app.run(debug=True)
