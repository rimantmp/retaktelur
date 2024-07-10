from flask import Blueprint, request, redirect, render_template, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from config.database import get_database_connection

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        conn = get_database_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO user (username, password, email) VALUES (%s, %s, %s)",
                (username, password, email)  # Storing the plain text password
            )
            conn.commit()
            return redirect(url_for('auth.login'))  # Corrected redirect to 'auth.login'
        except Exception as err:
            print(err)
        finally:
            cursor.close()
            conn.close()
    return render_template('admin_pages/register.html')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Login'
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_database_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM user WHERE username = %s", (username,)
            )
            user = cursor.fetchone()
            if user and user['password'] == password:  # Direct comparison of plain text passwords
                session['user_id'] = user['user_id']
                return redirect(url_for('dashboard'))  # Ensure this matches your blueprint and function name
            else:
                flash('Invalid username or password')
        except Exception as err:
            print(err)
        finally:
            cursor.close()
            conn.close()
    return render_template('admin_pages/login.html', title=title)

@auth_blueprint.route('/logout')
def logout():
    session.clear()  # Clear all session data
    flash('Pesan :', 'Anda telah logout dari sistem.')
    return redirect(url_for('auth.login'))