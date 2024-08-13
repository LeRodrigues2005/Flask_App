from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

# Criação do aplicativo Flask
app = Flask(__name__)

# Chave gerada aleatoriamente, necessária para usar flash messages
app.secret_key = 'b6d12e1f17c8b28f89114e44f8d9209b5e18e5e179a940b5a3f9f2a8e2d8b3f4'

# Configuração do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.sqlite3"  # Nome do banco de dados

# Inicialização do SQLAlchemy com a configuração
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    author = db.Column(db.String())

# Função utilizada para converter um objeto em um dicionário Python:

    def to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result


# Criar as tabelas no banco de dados
with app.app_context():
    db.create_all()


@app.route("/")  # Rota para a página inicial
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

##### API #####


@app.route("/api/posts")
def api_list_posts():
    try:
        posts = Post.query.all()
        return jsonify([post.to_dict() for post in posts])
    except Exception as error:
        print("Error", error)

    return jsonify([])


@app.route("/api/post", methods=["PUT"])
def api_add_posts():
    try:
        data = request.get_json()  # transforma o corpo da requisição em dicionário
        post = Post(title=data["title"], content=data["content"], author=data["author"])
        db.session.add(post)
        db.session.commit()
        flash('Post criado com sucesso!', 'success')
        return jsonify({"success": True})
    except Exception as error:
        print(error)
        flash("Erro ao adicionar post. Tente novamente.", "error")

    return jsonify({"success": False})


@app.route("/api/post/<id>", methods=["DELETE"])
def api_delete_post(id):
    try:
        post = Post.query.get(id)
        db.session.delete(post)
        db.session.commit()
        flash("Post excluído com sucesso!", "success")
        return jsonify({"success": True})
    except Exception as error:
        print("Error", error)
        flash("Post não encontrado.", "error")

    return jsonify({"success": False})


@app.route("/api/post/<id>", methods=["PUT"])
def api_edit_post(id):
    try:
        post = Post.query.get(id)
        data = request.get_json()
        post.title = data["title"]
        post.content = data["content"]
        post.author = data["author"]
        db.session.commit()
        flash("Post editado com sucesso!", "success")
        return jsonify({"success": True})
    except Exception as error:
        print(error)
        flash("Erro ao editar post.", "error")

    return jsonify({"success": False})


# Header seguro:

@app.after_request
def add_header(response):
    # Impede que outro site crie um iframe desse site; protege contra ataques de clickjacking:
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "script-src 'none';"  # Impede a execução de scripts
    # Permite a execução de scripts inline e eventos inline:
    # response.headers["Content-Security-Policy"] = "script-src 'none';"
    return response


if __name__ == "__main__":  # Executar o aplicativo
    app.run(debug=True)
