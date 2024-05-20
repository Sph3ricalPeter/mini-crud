from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud_app.sqlite'
db = SQLAlchemy(app)


class Item(db.Model):
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)


def get_items() -> list[Item]:
    return Item.query.all()


def get_item(item_id) -> Item:
    return Item.query.get(item_id)


def item_exists(item_id) -> bool:
    return Item.query.get(item_id) is not None


def email_exists(email) -> bool:
    return Item.query.filter_by(email=email).first() is not None


def add_item(name, email, password) -> Item:
    new_item = Item(name=name, email=email, password=password)
    db.session.add(new_item)
    db.session.commit()
    return new_item


def update_item(item_id, name, email, password) -> None:
    item = Item.query.get(item_id)
    item.name = name
    item.email = email
    item.password = password
    db.session.commit()


def delete_item(item_id) -> None:
    item = Item.query.get(item_id)
    db.session.delete(item)
    db.session.commit()


@app.route('/')
def index():
    # vrati HTML vyplnene o seznam itemu s pouzitim dane sablony
    items = get_items()
    return render_template('index.html', items=items)


@app.route('/new')
def new_item_page():
    return render_template('new_item.html')


@app.route('/detail/<int:item_id>')
def detail_page(item_id):
    item = get_item(item_id)
    return render_template('detail.html', item=item)


@app.route('/update/<int:item_id>')
def update_item_page(item_id):
    item = get_item()
    return render_template('update_item.html', item=item)


@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if email_exists(email):
        # redirect to /add with error message
        return render_template('new_item.html', error='Email already exists')
    
    add_item(name, email, password)
    return redirect(url_for('index'))


@app.route('/update/<int:item_id>', methods=['POST'])
def update(item_id):
    updated_name = request.form.get('name')
    updated_email = request.form.get('email')
    updated_password = request.form.get('password')
    update_item(item_id, updated_name, updated_email, updated_password)
    return redirect(url_for('index'))


@app.route('/delete/<int:item_id>')
def delete(item_id):
    delete_item(item_id)
    return redirect(url_for('index'))


@app.route('/api/items')
def api_items():
    # vrati JSON se seznamem itemu (JEN DATA)
    items = get_items()
    return jsonify([item.serialize() for item in items])


@app.route('/api/items/<int:item_id>')
def api_item(item_id):
    # vrati JSON s jednim itemem (JEN DATA)
    if not item_exists(item_id):
        return '', 404
    
    item = Item.query.get(item_id)
    return jsonify(item.serialize())


@app.route('/api/items', methods=['POST'])
def api_add_item():
    # prida novy item
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    if email_exists(email):
        return jsonify({'error': 'Email already exists'}), 400

    new_item = add_item(name, email, password)
    return jsonify(new_item.serialize())

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def api_update_item(item_id):
    # upravi item pokud existuje
    updated_name = request.json.get('name')
    updated_email = request.json.get('email')
    updated_password = request.json.get('password')

    if not item_exists(item_id):
        return '', 404

    update_item(item_id, updated_name, updated_email, updated_password)
    return '', 204


@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def api_delete_item(item_id):
    # smaze item pokud existuje
    if not item_exists(item_id):
            return '', 404

    delete_item(item_id)
    return '', 204


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
