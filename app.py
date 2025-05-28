from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        equipamento = request.form['equipamento']
        pib = request.form['pib']
        descricao = request.form['descricao']
        data = request.form['data']

        gerencia = request.form['gerencia']
        subgerencia = request.form['subgerencia']
        secao = request.form['secao']

        matricula_uso = request.form['matricula_uso']
        nome_uso = request.form['nome_uso']

        matricula_conferente = request.form['matricula_conferente']
        nome_conferente = request.form['nome_conferente']

        # Aqui você pode armazenar os dados como desejar (lista, banco, etc.)
        flash('Equipamento cadastrado com sucesso!', 'success')
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

@app.route('/baixa')
def baixa():
    return render_template('baixa.html')


if __name__ == '__main__':
    app.run(debug=True)
