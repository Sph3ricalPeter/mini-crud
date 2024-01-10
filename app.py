from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud_app.sqlite'
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


@app.route('/')
def index():
    items = Item.query.all()
    items = list(filter(lambda item: "Test" not in item.name, items))
    return render_template('index.html', items=items)


@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    new_item = Item(name=name)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/update/<int:item_id>', methods=['POST'])
def update(item_id):
    updated_name = request.form.get('name')
    item = Item.query.get(item_id)
    item.name = updated_name
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
