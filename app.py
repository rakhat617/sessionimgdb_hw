import sqlite3
import os
from flask import (
    Flask,
    render_template,
    redirect,
    request,
    url_for,
    session
)



app = Flask(__name__)
app.secret_key = "nuggets123"
app.config['UPLOAD_FOLDER'] = 'static/upload_images'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET','POST'])
def get_main():
    connection = sqlite3.connect("post.db")
    cursor = connection.cursor()
    cursor.execute(" SELECT * FROM post ")
    posts = cursor.fetchall()
    connection.commit()
    connection.close()
    return render_template('base.html', posts = posts)

@app.route('/profile', methods=['GET','POST'])
def get_profile():
    name = session.get("login", "")
    return render_template('profile.html', name = name)


@app.route('/create_post', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        image_file = request.files['image']
        filename = None

        if image_file:
            filename = image_file.filename
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = sqlite3.connect('post.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO post (title, description, price, image)
            VALUES (?, ?, ?, ?)
        """, (title, description, price, f"upload_images/{filename}"))

        conn.commit()
        conn.close()

        return redirect(url_for('get_main'))  

    return render_template('create_post.html')


@app.route('/log', methods=['GET', 'POST'])
def get_log():
    if request.method == 'POST':
        login = request.form.get('login', type=str)
        password = request.form.get('password', type=str)
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session["login"] = user[1]
            return redirect(url_for('get_main'))
        else:
            error_message = "Неверный логин или пароль"
            return render_template('log.html', error=error_message)

    return render_template('log.html')





@app.route('/reg', methods=['GET','POST'])
def get_reg():
    if request.method == 'POST':
        login = request.form.get('login', type=str)
        email = request.form.get('email', type=str)
        password = request.form.get('password', type=str)
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO users (login, email, password) VALUES (?, ?, ?)', (login, email, password))
        session["login"] = login
        conn.commit()
        conn.close()
        return redirect(url_for('get_main'))

    return render_template('reg.html')

@app.route("/logout", methods=["GET", "POST"])
def log_out():
    session.pop("login", None)
    return redirect(url_for("get_main"))


if __name__ == '__main__':
    app.run(debug=True)