from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud_app.sqlite'
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)


@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)


@app.route('/new')
def new_item_page():
    return render_template('new_item.html')


@app.route('/detail/<int:item_id>')
def detail_page(item_id):
    item = Item.query.get(item_id)
    return render_template('detail.html', item=item)


@app.route('/update/<int:item_id>')
def update_item_page(item_id):
    item = Item.query.get(item_id)
    return render_template('update_item.html', item=item)


@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    new_item = Item(name=name, email=email, password=password)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/update/<int:item_id>', methods=['POST'])
def update(item_id):
    updated_name = request.form.get('name')
    updated_email = request.form.get('email')
    updated_password = request.form.get('password')
    item = Item.query.get(item_id)
    item.name = updated_name
    item.email = updated_email
    item.password = updated_password
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:item_id>')
def delete(item_id):
    item = Item.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
