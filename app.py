from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from enum import Enum

app = Flask(__name__)

# Настройка базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecret'

# Инициализация базы данных
db = SQLAlchemy(app)


class LevelSecret(Enum):
    SECRET = 'Secret'
    SUPERSECRET = 'Super Secret'


# Модель задачи (таблица Task)
class Agents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_name = db.Column(db.String(40), nullable=False, unique=True)
    phone = db.Column(db.Integer)
    email = db.Column(db.String(50), nullable=False)
    secret_level = db.Column(db.Enum(LevelSecret), nullable=False)

    def __repr__(self):
        return f"<Agent {self.code_name}>"


# Создаем таблицу в базе данных
with app.app_context():
    db.create_all()


### 📌 CRUD-МАРШРУТЫ

# 📌 Главная страница: список задач
@app.route('/')
@app.route('/agents', methods=['GET'])
def get_agents():
    agents = Agents.query.all()
    query = Agents.query

    code_name = request.args.get('code-name', '').strip()
    email = request.args.get('email', '').strip()
    secret_level = request.args.get('secret-level', '')

    if code_name:
        query = query.filter(Agents.code_name.ilike(f'%{code_name}%'))
    if email:
        query = query.filter(Agents.email.ilike(f'%{email}%'))
    if secret_level:
        query = query.filter_by(secret_level=secret_level)

    sort_code_name = request.args.get('sort-code-name', '')
    sort_email = request.args.get('sort-email', '')

    match sort_code_name:
        case 'asc':
            query = query.order_by(Agents.code_name.asc())
        case 'desc':
            query = query.order_by(Agents.code_name.desc())
        case 'new':
            query = query.order_by(Agents.id.desc())
        case 'old':
            query = query.order_by(Agents.id.asc())

    match sort_email:
        case 'asc':
            query = query.order_by(Agents.email.asc())
        case 'desc':
            query = query.order_by(Agents.email.desc())

    agents = query.all()
    secret_level = LevelSecret

    return render_template('index.html', agents=agents, theme='light', secret_level=secret_level)




# 📌 Добавление новой задачи
@app.route('/add', methods=['GET', 'POST'])
def add_agent():
    if request.method == 'POST':
        code_name = request.form['code-name'].lower()
        phone_number = request.form['phone']
        email = request.form['email'].lower()
        if request.form['secret-level'] == "0":
            level = LevelSecret.SECRET
        else:
            level = LevelSecret.SUPERSECRET

        if Agents.query.filter_by(code_name=code_name).first():
            flash("Code Name " + code_name.title() + " is already exist")
            return redirect('add')

        if code_name.strip() and email.strip():
            try:
                new_agent = Agents(code_name=code_name, phone=phone_number, email=email, secret_level=level)
                db.session.add(new_agent)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash("Error save. Data is not save. Code Name need to be unique.")
                return redirect('add')
        return redirect(url_for('get_agents'))
    return render_template('add.html', theme='light')


# 📌 Редактирование задачи
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_agent(id):
    agent = Agents.query.get_or_404(id)  # Получаем задачу по ID
    if request.method == 'POST':
        new_code_name = request.form['code-name'].lower()
        new_phone_number = request.form['phone']
        new_email = request.form['email'].lower()
        if request.form['secret-level'] == "0":
            new_level = LevelSecret.SECRET
        else:
            new_level = LevelSecret.SUPERSECRET
        if new_code_name.strip():
            agent.code_name = new_code_name
            agent.phone = new_phone_number
            agent.email = new_email
            agent.secret_level = new_level
            db.session.commit()
        return redirect(url_for('get_agents'))
    return render_template('edit.html', agent=agent, level=LevelSecret, theme='light')


# 📌 Удаление задачи
@app.route('/delete/<int:id>')
def delete_agent(id):
    agent = Agents.query.get_or_404(id)  # Получаем задачу по ID
    db.session.delete(agent)  # Удаляем из базы
    db.session.commit()  # Подтверждаем изменения
    return redirect(url_for('get_agents'))


@app.route('/agent/<int:id>')
def show_agent(id):
    agent = Agents.query.get_or_404(id)
    return render_template('agent.html', agent=agent, theme='light')


@app.route('/erase', methods=["POST", "GET"])
def button():
    if request.method == "POST":
        password = request.form.get("password")
        # Сделаем вид, что это функция проверяет введенный пароль. Я пока не придумала как это сделать нормально
        check_password = "12345678"
        if password == check_password:
            db.session.query(Agents).delete()
            db.session.commit()

        return redirect(url_for("get_agents"))

    return redirect(url_for("get_agents"))


# Запуск сервера
if __name__ == "__main__":
    app.run(debug=True)
