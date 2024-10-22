from flask import Flask, render_template, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
import os, bcrypt, sqlalchemy
from sqlalchemy.sql import func
from config import static_articles, secret_article
from flask_session import Session
import secrets, sys, hashlib
from functools import wraps
import json

# Il sorgente è semplificato, mancanca il file config che contiene solo le informazioni mostrate sulla pagina

app = Flask(__name__)
db = SQLAlchemy(app)


user_articles = db.Table('user_articles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'))
)
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=False, default="")
    price = db.Column(db.Float, nullable=False)
    img = db.Column(db.String(100), nullable=False, default="")
    secret_content = db.Column(db.String(300), nullable=False, default="")    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    password = db.Column(db.String(72), nullable=False)
    wallet = db.Column(db.Float, nullable=False, default=23.00)
    articles = db.relationship('Article', secondary=user_articles, backref='users')
    
    def verify_password(self, password):
        if isinstance(password, str):
            password = password.encode()
        pwhash = bcrypt.hashpw(password, self.password)
        return self.password == pwhash

def hash_psw(password):
    if isinstance(password, str):
        password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())

def authorize(mandatory=True):
    def authorize_inner(f):
        def on_failure(*args, **kws):
            if mandatory:
                return redirect(url_for('login'), code=302)
            else:
                return f(None, *args, **kws) 
        @wraps(f)
        def decorated_function(*args, **kws):
            if session.get("user", None) is None:
                return on_failure(*args, **kws)
            user = User.query.filter_by(username=session.get("user", None)).first()
            if user is None:
                session["user"] = None
                return on_failure(*args, **kws)
            return f(user, *args, **kws)            
        return decorated_function
    return authorize_inner

@app.route('/', methods=['GET'])
@authorize(mandatory=False)
def home(user:User):
    return render_template("home.html", user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if not session.get("user", None) is None:
        return redirect("/store", code=302)
    if request.method == 'POST':
        if not "user" in request.form or not "psw" in request.form:
            return render_template("login.html", error="La richiesta non è valida")
        username = request.form["user"].strip().lower()
        if len(username) < 3 or len(request.form["psw"]) < 3:
            return render_template("login.html", error="La password e l'username devono essere almeno lunghi 3 caratteri")
        user = User.query.filter_by(username=username).first()
        if user is None:
            return render_template("login.html", error="L'username non è registrato!")
        if user.verify_password(request.form["psw"]):
            session["user"] = user.username
            session["failed_login"] = 0
            return redirect(url_for('store'), code=302)
        else:
            return render_template("login.html", error="La password non è valida!")
    session["failed_login"] = 0
    return render_template("login.html", error=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if not session.get("user", None) is None:
        return redirect("/store", code=302)
    if request.method == 'POST':
        if not "user" in request.form or not "psw" in request.form:
            return render_template("register.html", error="La richiesta non è valida")
        username = request.form["user"].strip().lower()
        if len(username) < 3 or len(request.form["psw"]) < 3:
            return render_template("register.html", error="La password e l'username devono essere almeno lunghi 3 caratteri")
        user = User.query.filter_by(username=username).first()
        if not user is None:
            return render_template("register.html", error="Questo username è stato già utilizzato")
        user = User(
            username=username,
            password=hash_psw(request.form["psw"]),
        )
        try:
            db.session.add(user)
            session["user"] = user.username
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return render_template("register.html", error="Questo username è stato già utilizzato") 
        return redirect(url_for('store'), code=302)
    return render_template("register.html", error=None)

@app.route('/ABCDEFGHI_FREE_MONEY__123_SECRET/<int:money>', methods=['PATCH'])
@authorize()
def free_money(user:User, money:int):
    user.wallet += money
    db.session.merge(user)
    db.session.commit()
    return "Aggiunto denaro", 200

@app.route('/logout', methods=['GET'])
def logout():
    session["user"] = None
    return redirect(url_for('login'), code=302)

@app.route('/store', methods=['GET']) 
@authorize()
def store(user:User):
    return render_template("store.html", user=user, articles=Article.query.all())

@app.route('/store/<int:article_id>/buy', methods=['GET', 'POST'])
@authorize()
def buy(user:User, article_id):
    article = Article.query.filter_by(id=article_id).first()
    if article is None:
        return redirect(url_for('store'), code=302)
    if request.method == 'POST':
        if article in user.articles:
            return render_template("article.html", user=user, article=article, error="Hai già acquistato questo articolo", success=False)
        if user.wallet < article.price:
            return render_template("article.html", user=user, article=article, error="Non hai abbastanza denaro!", success=False)
        if "Samsung Smart Fridge" in article.description:
            if request.headers.get("X-Teamperature") != hashlib.md5(b"-10deg $_$").hexdigest():
                return render_template("article.html", user=user, article=article, error="Accettate solo richieste a -10° 🥶", success=False)
        user.wallet -= article.price
        user.articles.append(article)
        db.session.merge(user)
        db.session.commit()
        return render_template("article.html", user=user, article=article, error=None, success=True)
    return render_template("article.html", user=user, article=article, error=None, success=None)


@app.route('/cats', methods=['GET'])
@authorize()
def cats(user:User):
    data = {}
    try:
        cat_json = '{"cat_lover":false'
        if request.headers.get("X-Additional-Info") is not None:
            cat_json += f',{request.headers.get("X-Additional-Info")}'
        cat_json += "}"
        data = json.loads(cat_json)
    except Exception:
        return "Errore", 400
    if not data.get("cat_lover", False) and not data.get("cat", False):
        return "Non sei un amante dei gatti", 200
    return render_template("article.html", user=user, article=secret_article, error=None, success=True, force_show_secret=True)    
    
