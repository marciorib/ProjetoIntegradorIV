from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        # Aqui você pode salvar os dados (em memória, arquivo, banco, etc.)
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('cadastro'))
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
