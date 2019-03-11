from DB import *
from flask import Flask, render_template, redirect, flash
from loginform import *
from add_message import *
from registerform import *
from answerform import *
from updateform import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'EYokE5GbbNJkL'
# app.config['UPLOAD_FOLDER'] = '/static/files'

db = DB()

users = UsersModel(db.get_connection())
users.init_table()
# users.insert('Ruslik', '123', 'Руслан', 'Хамзин', 'r@gmail.com', 16)

inbox_messages = InboxMessageModel(db.get_connection())
inbox_messages.init_table()

outbox_messages = OutboxMessageModel(db.get_connection())
outbox_messages.init_table()

session = {}


@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
    user = UsersModel(db.get_connection()).get(session['username'])
    return render_template('index.html', username=session['username'],
                           title='Личный кабинет', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    user_model = UsersModel(db.get_connection())
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        age = form.age.data
        exists = user_model.exist(user_name)
        if not exists[0]:
            user_model.insert(user_name, password, name, surname, email, age)
            session['username'] = user_name
            return redirect('/index')
        else:
            flash('Этот Логин уже занят')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(user_name, password)
        if exists[0]:
            session['username'] = user_name
        return redirect("/index")
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    return redirect('/login')


@app.route('/add_message', methods=['GET', 'POST'])
def add_message():
    if 'username' not in session:
        return redirect('/login')
    form = AddMessageForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        recipient = form.recipient.data
        # file = form.file.data
        outbox_message = OutboxMessageModel(db.get_connection())
        outbox_message.insert(title, content, session['username'], recipient)
        inbox_message = InboxMessageModel(db.get_connection())
        inbox_message.insert(title, content, session['username'], recipient)
        flash('Сообщение отправлено')
        return redirect("/index")
    return render_template('add_message.html', title='Новое сообщение',
                           form=form, username=session['username'], recipient=None)


@app.route('/add_message/<recipient>', methods=['GET', 'POST'])
def answer(recipient):
    if 'username' not in session:
        return redirect('/login')
    form = AnswerForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        # file = form.file.data
        outbox_message = OutboxMessageModel(db.get_connection())
        outbox_message.insert(title, content, session['username'], recipient)
        inbox_message = InboxMessageModel(db.get_connection())
        inbox_message.insert(title, content, session['username'], recipient)
        flash('Сообщение отправлено')
        return redirect("/index")
    return render_template('add_message.html', title='Ответ пользователю',
                           form=form, username=session['username'], recipient=recipient)


@app.route('/inbox')
def inbox():
    if 'username' not in session:
        return redirect('/login')
    inbox_message = InboxMessageModel(db.get_connection())
    return render_template('inbox.html', title='Входящие', username=session['username'],
                           mesages=inbox_message.get_all(recipient=session['username']))


@app.route('/outbox')
def outbox():
    if 'username' not in session:
        return redirect('/login')
    outbox_message = OutboxMessageModel(db.get_connection())
    return render_template('outbox.html', title='Исходящие', username=session['username'],
                           mesages=outbox_message.get_all(user_name=session['username']))


@app.route('/delete_inbox/<int:message_id>', methods=['GET'])
def delete_inbox(message_id):
    if 'username' not in session:
        return redirect('/login')
    inbox_message = InboxMessageModel(db.get_connection())
    inbox_message.delete(message_id)
    flash('Сообщение удалено')
    return redirect('/inbox')


@app.route('/delete_outbox/<int:message_id>', methods=['GET'])
def delete_outbox(message_id):
    if 'username' not in session:
        return redirect('/login')
    outbox_message = OutboxMessageModel(db.get_connection())
    outbox_message.delete(message_id)
    inbox_message = InboxMessageModel(db.get_connection())
    inbox_message.delete(message_id)
    flash('Сообщение удалено')
    return redirect('/outbox')


@app.route('/update/<int:message_id>', methods=['GET', 'POST'])
def update(message_id):
    if 'username' not in session:
        return redirect('/login')
    form = UpdateForm()
    outbox_message = OutboxMessageModel(db.get_connection())
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        outbox_message.update(content=content, message_id=message_id, title=title)
        inbox_message = InboxMessageModel(db.get_connection())
        inbox_message.update(content=content, message_id=message_id, title=title)
        flash('Сообщение отредактировано')
        return redirect("/outbox")
    form.title.data = outbox_message.get(message_id)[1]
    form.content.data = outbox_message.get(message_id)[2]
    return render_template('update.html', title='Редактирование сообщения',
                           form=form, username=session['username'])


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')