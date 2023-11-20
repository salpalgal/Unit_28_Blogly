from flask import Flask, render_template, request, redirect

from models import User, db, connect_db, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///posts_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route("/users")
def list_users():
    """Listing all users and show form."""
    users = User.query.all()
    return render_template("list.html", users = users)

@app.route('/users/new')
def create_user():
    return render_template("create.html")

@app.route("/add_to_db", methods = ["POST"])
def add_to_db():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user = User(first_name =first_name , last_name = last_name , image_url = image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_details(user_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.filter(Post.user_id == user_id).all()
    return render_template('details.html', user = user, post = post)

@app.route("/users/<int:user_id>/edit")
def edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user = user)

@app.route("/users/<int:user_id>/edit", methods = ["POST"])
def update_db(user_id):
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    

    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods = ["POST"])
def delete(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")
    
@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
    user =  User.query.get_or_404(user_id)
    return render_template("post_form.html", user = user)

@app.route("/users/<int:user_id>/posts/new" , methods = ["POST"])
def post_form_to_db(user_id):
    title = request.form["title"]
    content = request.form["content"]

    post = Post(title = title , content = content , user_id = user_id)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def post_details(post_id):
    post = Post.query.get_or_404(post_id)
    user_post = post.user_post
    return render_template("post_details.html", post= post, user_post = user_post)

@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    post = Post.query.get(post_id)
    return render_template("post_edit.html", post = post)

@app.route("/posts/<int:post_id>/edit", methods = ["POST"])
def update_edit(post_id):
    title = request.form["title"]
    content = request.form["content"]

    post = Post.query.get(post_id)
    post.title = title
    post.content = content

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")