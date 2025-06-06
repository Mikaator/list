from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from urllib.parse import urlparse

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-123')

# Datenbank-URL für Render.com anpassen
database_url = os.environ.get('DATABASE_URL', 'sqlite:///shopping.db')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Group(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    shopping_lists = db.relationship('ShoppingList', backref='group', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ShoppingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    items = db.relationship('Item', backref='shopping_list', lazy=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50), default='shopping-cart')
    completed = db.Column(db.Boolean, default=False)
    shopping_list_id = db.Column(db.Integer, db.ForeignKey('shopping_list.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Group.query.get(int(user_id))

# Datenbank initialisieren
def init_db():
    with app.app_context():
        try:
            db.create_all()
            print("Datenbank erfolgreich initialisiert!")
        except Exception as e:
            print(f"Fehler bei der Datenbankinitialisierung: {str(e)}")

# Initialisiere die Datenbank beim Start
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        group_name = request.form.get('group_name')
        password = request.form.get('password')
        group = Group.query.filter_by(name=group_name).first()
        
        if group and group.check_password(password):
            login_user(group)
            return redirect(url_for('dashboard'))
        flash('Ungültige Anmeldedaten')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        group_name = request.form.get('group_name')
        password = request.form.get('password')
        
        if Group.query.filter_by(name=group_name).first():
            flash('Gruppenname bereits vergeben')
            return redirect(url_for('register'))
        
        group = Group(name=group_name)
        group.set_password(password)
        db.session.add(group)
        db.session.commit()
        
        login_user(group)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# API Routes für Einkaufslisten
@app.route('/api/lists', methods=['POST'])
@login_required
def create_list():
    data = request.get_json()
    new_list = ShoppingList(name=data['name'], group_id=current_user.id)
    db.session.add(new_list)
    db.session.commit()
    return jsonify({'id': new_list.id, 'name': new_list.name})

@app.route('/api/lists/<int:list_id>', methods=['PUT'])
@login_required
def update_list(list_id):
    list = ShoppingList.query.get_or_404(list_id)
    if list.group_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    list.name = data['name']
    db.session.commit()
    return jsonify({'id': list.id, 'name': list.name})

@app.route('/api/lists/<int:list_id>', methods=['DELETE'])
@login_required
def delete_list(list_id):
    list = ShoppingList.query.get_or_404(list_id)
    if list.group_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(list)
    db.session.commit()
    return jsonify({'success': True})

# API Routes für Items
@app.route('/api/items', methods=['POST'])
@login_required
def create_item():
    data = request.get_json()
    list = ShoppingList.query.get_or_404(data['list_id'])
    if list.group_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    new_item = Item(
        name=data['name'],
        icon=data.get('icon', 'shopping-cart'),
        shopping_list_id=list.id
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({
        'id': new_item.id,
        'name': new_item.name,
        'icon': new_item.icon,
        'completed': new_item.completed
    })

@app.route('/api/items/<int:item_id>', methods=['PUT'])
@login_required
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.shopping_list.group_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    if 'name' in data:
        item.name = data['name']
    if 'icon' in data:
        item.icon = data['icon']
    if 'completed' in data:
        item.completed = data['completed']
    
    db.session.commit()
    return jsonify({
        'id': item.id,
        'name': item.name,
        'icon': item.icon,
        'completed': item.completed
    })

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.shopping_list.group_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(item)
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True) 