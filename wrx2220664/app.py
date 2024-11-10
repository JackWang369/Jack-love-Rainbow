from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# 配置 MySQL 连接
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'data'
app.secret_key = 'your_secret_key'  # 设置一个安全的密钥
mysql = MySQL(app)

# 创建数据库表，如果表已存在则不会重复创建
with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    ''')
    mysql.connection.commit()

@app.route('/', methods=['GET'])
def a():
    return render_template('a.html')

@app.route('/b', methods=['POST'])
def login():
    username = request.form.get('username')
    if not username:
        return "用户名不能为空", 400
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
    if user:
        session['username'] = username  # 将用户名存储在会话中
        return redirect(url_for('b'))
    else:
        return "用户名不存在", 401

@app.route('/b')
def b():
    username = session.get('username')  # 从会话中获取用户名
    if not username:
        return redirect(url_for('a'))  # 如果没有用户名，重定向到登录页面
    return render_template('b.html', username=username)

@app.route('/users')
def show_users():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)