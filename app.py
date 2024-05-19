from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db= SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    info = db.Column(db.Text(20000),nullable=False)
    price = db.Column(db.Integer,nullable=False)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/add', methods=['POST','GET'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        info = request.form['info']
        price = request.form['price']
        article = Product(title=title,info=info,price=price)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return "произошла ошибка"
    else:
        return render_template("add.html")

@app.route('/items')
def items():
    articles = Product.query.order_by(Product.id.desc()).all()
    return render_template("items.html",articles=articles)

@app.route('/delete/<int:id>')
def delete(id):
    article = Product.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return render_template("delete.html")
    except:
        return "ошибка"

@app.route('/buy/<int:id>')
def buy(id):
    return render_template("buy.html")

if __name__ == '__main__':
    app.run(debug=True)