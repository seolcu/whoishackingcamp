from flask import Flask, request, render_template_string, make_response

app = Flask(__name__)

login_page = '''
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
'''

FLAG = "flag{example_flag}"
admin_pass = 'example_password'

@app.route('/', methods=['GET', 'POST'])
def login():
    role = request.cookies.get('role', 'non')
    message = "Login me!"
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'guest' and password == 'guest':
            resp = make_response(render_template_string(login_page, message="Hello, guest!"))
            resp.set_cookie('role', 'guest')
            return resp
        elif username == 'admin' and password == admin_pass:
            resp = make_response(render_template_string(login_page, message=f"Hello, admin! Here is your flag: {FLAG}"))
            resp.set_cookie('role', 'admin')
            return resp
        else:
            resp = make_response(render_template_string(login_page, message="Invalid credentials. Please try again."))
            resp.set_cookie('role', 'guest')
            return resp
    else:
        if role == 'admin':
            message = f"Hello, admin! Here is your flag: {FLAG}"
        elif role == 'guest':
            message = "Hello, guest!"
        else:
            message = "Login me!"

    return render_template_string(login_page, message=message)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
