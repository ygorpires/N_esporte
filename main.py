from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__,template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///nunesesporte.sqlite3"

db = SQLAlchemy(app)

class Produto (db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    descricao = db.Column(db.String(100))
    preco = db.Column(db.Float)

    def __init__(self, descricao, preco):
        self.descricao = descricao
        self.preco = preco



@app.route('/')
def index():
    produtos = Produto.query.all()

    return render_template('index.html',produtos = produtos)

@app.route('/add', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        descricao = request.form['descricao']
        preco = request.form['preco']

        produtos = Produto(descricao, preco)
        db.session.add(produtos)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('form_cadastro.html') 


@app.route('/delete/<int:id>')
def delete(id):

    produto = Produto.query.get(id)
    if produto is not None:
        db.session.delete(produto)
        db.session.commit()
    else:
        return redirect(url_for('index')) 
    return redirect(url_for('index'))  

@app.route('/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):
    produtos = Produto.query.get(id)
    if produtos is not None:
        if request.method == 'POST':
            produtos.descricao = request.form['descricao']
            produtos.preco = request.form['preco']
            db.session.commit()

            return redirect(url_for('index'))
    else:
            return redirect(url_for('index'))
    return render_template('form_edit.html', produtos = produtos)    




if __name__   == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True) 