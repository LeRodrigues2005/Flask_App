from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Criação do aplicativo Flask
app = Flask(__name__)

# Necessário para usar flash messages
app.secret_key = 'b6d12e1f17c8b28f89114e44f8d9209b5e18e5e179a940b5a3f9f2a8e2d8b3f4'

# Configuração do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.sqlite3"  # nome do banco de dados

# Inicialização do SQLAlchemy com a configuração
db = SQLAlchemy(app)

# Definição do modelo


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    author = db.Column(db.String())

# Criar as tabelas no banco de dados


with app.app_context():
    db.create_all()

# Rota para a página inicial


@app.route("/")
def home():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


@app.route("/post/add", methods=["POST"])
def add_post():
    try:
        form = request.form
        post = Post(title=form["title"], content=form["content"], author=form["author"])
        db.session.add(post)
        db.session.commit()
        flash('Post criado com sucesso!', 'success')
    except Exception as error:
        print(error)
        flash("Erro ao adicionar post. Tente novamente.", "error")

    return redirect(url_for("home"))


@app.route("/post/<id>/delete")
def delete_post(id):
    try:
        post = Post.query.get(id)
        db.session.delete(post)
        db.session.commit()
        flash("Post excluído com sucesso!", "success")
    except Exception as error:
        print("Error", error)
        flash("Post não encontrado.", "error")

    return redirect(url_for("home"))


@app.route("/post/<id>/edit", methods=["POST", "GET"])
def edit_post(id):
    if request.method == "POST":
        try:
            post = Post.query.get(id)
            form = request.form
            post.title = form["title"]
            post.content = form["content"]
            post.author = form["author"]
            db.session.commit()
            flash("Post editado com sucesso!", "success")
        except Exception as error:
            print(error)
            flash("Erro ao editar post.", "error")

        return redirect(url_for("home"))
    else:
        try:
            post = Post.query.get(id)
            return render_template("edit.html", post=post)
        except Exception as error:
            print("Error", error)

    return redirect(url_for("home"))

# Executar o aplicativo


if __name__ == "__main__":
    app.run(debug=True)
