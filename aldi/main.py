from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'rahasia'

# Data user sederhana
users = {
    "admin": {"password": "123", "role": "admin"},
    "user": {"password": "123", "role": "user"}
}

# ROOT - Saat membuka link utama
@app.route('/')
def root():
    if 'username' in session and 'role' in session:
        if session['role'] == 'admin':
            return redirect(url_for('home'))
        else:
            return redirect(url_for('user_index'))
    else:
        return redirect(url_for('login'))

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)

        if user and user['password'] == password:
            session['username'] = username
            session['role'] = user['role']

            flash(f"Login berhasil sebagai {user['role']}!", 'success')

            return redirect(url_for('root'))  # Redirect ke route /
        else:
            return render_template('login.html', error="Username atau password salah.")
    return render_template('login.html')

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('login'))

# USER
@app.route('/user/home')
def user_index():
    if 'role' not in session or session['role'] != 'user':
        return redirect(url_for('login'))
    return render_template('user/index.html')

@app.route('/tentang')
def tentang():
    return render_template('user/tentang.html')

@app.route('/kontak')
def kontak():
    return render_template('user/kontak.html')

# ADMIN
@app.route('/admin/home')
def home():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    return render_template('admin/index.html')

@app.route('/admin/admin-kelola-barang')
def kelolabarang():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    return render_template('admin/barang.html')


if __name__ == '__main__':
    app.run(debug=True)
