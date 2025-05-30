from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Chave secreta segura

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'equipamentos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Equipamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipamento = db.Column(db.String(200), nullable=False)
    pib = db.Column(db.String(9), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    data = db.Column(db.Date, nullable=False)
    gerencia = db.Column(db.String(100), nullable=False)
    subgerencia = db.Column(db.String(100), nullable=False)
    secao = db.Column(db.String(100), nullable=False)
    matricula_uso = db.Column(db.String(8), nullable=False)
    nome_uso = db.Column(db.String(200), nullable=False)
    matricula_conferente = db.Column(db.String(8), nullable=False)
    nome_conferente = db.Column(db.String(200), nullable=False)

def obter_dados_equipamentos():
    equipamentos = Equipamento.query.all()
    return [{
        "Equipamento": e.equipamento,
        "PIB": e.pib,
        "Descrição": e.descricao,
        "Data": e.data.strftime('%Y-%m-%d'),
        "Gerência": e.gerencia,
        "Subgerência": e.subgerencia,
        "Seção": e.secao,
        "Matrícula Uso": e.matricula_uso,
        "Nome Uso": e.nome_uso,
        "Matrícula Conferente": e.matricula_conferente,
        "Nome Conferente": e.nome_conferente
    } for e in equipamentos]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        try:
            # Validação básica
            campos_obrigatorios = [
                'equipamento', 'pib', 'descricao', 'data', 'gerencia',
                'subgerencia', 'secao', 'matricula_uso', 'nome_uso',
                'matricula_conferente', 'nome_conferente'
            ]
            for campo in campos_obrigatorios:
                if not request.form.get(campo):
                    flash(f'O campo "{campo}" é obrigatório.', 'danger')
                    return redirect(url_for('cadastro'))

            novo = Equipamento(
                equipamento=request.form['equipamento'],
                pib=request.form['pib'],
                descricao=request.form['descricao'],
                data=datetime.strptime(request.form['data'], '%Y-%m-%d'),
                gerencia=request.form['gerencia'],
                subgerencia=request.form['subgerencia'],
                secao=request.form['secao'],
                matricula_uso=request.form['matricula_uso'],
                nome_uso=request.form['nome_uso'],
                matricula_conferente=request.form['matricula_conferente'],
                nome_conferente=request.form['nome_conferente']
            )
            db.session.add(novo)
            db.session.commit()
            flash('Equipamento cadastrado com sucesso!', 'success')
            return redirect(url_for('cadastro'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar: {str(e)}', 'danger')
            return redirect(url_for('cadastro'))

    return render_template('cadastro.html')

@app.route('/leitura')
def leitura():
    flash('Página de leitura em construção.', 'info')
    return render_template('leitura.html')

@app.route('/impressao')
def impressao():
    flash('Página de impressão em construção.', 'info')
    return render_template('impressao.html')

@app.route('/listagem')
def listagem():
    equipamentos = Equipamento.query.all()
    return render_template('listagem.html', equipamentos=equipamentos)

@app.route('/baixa')
def baixa():
    flash('Página de baixa em construção.', 'info')
    return render_template('baixa.html')

@app.route('/exportar/excel')
def exportar_excel():
    try:
        dados = obter_dados_equipamentos()
        df = pd.DataFrame(dados)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Equipamentos')
        output.seek(0)
        return send_file(
            output,
            as_attachment=True,
            download_name='equipamentos.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        flash(f'Erro ao exportar para Excel: {str(e)}', 'danger')
        return redirect(url_for('listagem'))

@app.route('/exportar/pdf')
def exportar_pdf():
    try:
        equipamentos = Equipamento.query.all()
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        y = height - 50
        p.setFont("Helvetica", 12)
        p.drawString(50, y, "Lista de Equipamentos:")
        y -= 30

        for eq in equipamentos:
            texto = f"{eq.equipamento} | PIB: {eq.pib} | {eq.gerencia}/{eq.secao} | {eq.nome_uso} ({eq.matricula_uso})"
            p.drawString(50, y, texto)
            y -= 20
            if y < 50:
                p.showPage()
                y = height - 50

        p.save()
        buffer.seek(0)
        return send_file(
            buffer,
            as_attachment=True,
            download_name='equipamentos.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        flash(f'Erro ao exportar para PDF: {str(e)}', 'danger')
        return redirect(url_for('listagem'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
