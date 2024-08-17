from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

login_page = """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <h2>Login Page</h2>
    <form method="post">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    <p>{{ message }}</p>
</body>
</html>
"""

FLAG = "flag{example_flag}"


def get_db_connection():
    conn = sqlite3.connect("database.db")
    return conn


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "guest" and password == "guest":
            message = "Hello, guest!"
        else:
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            user = cursor.fetchone()
            conn.close()

            if user:
                if user[0] == "admin":
                    message = f"Hello, admin! Here is your flag: {FLAG}"
                else:
                    message = "Hello, user!"
            else:
                message = "Invalid credentials. Please try again."
    else:
        message = ""

    return render_template_string(login_page, message=message)


if __name__ == "__main__":
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    cursor.execute(
        "INSERT INTO users (username, password) VALUES ('admin', 'admin_pass')"
    )
    conn.commit()
    conn.close()

    app.run(host="0.0.0.0", port=5000, debug=True)
