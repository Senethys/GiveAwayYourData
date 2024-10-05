# Install Flask using the following command:
# pip install Flask

# Save this file as `app.py`

from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'your_secret_key'  # Needed for flash messages

# SQL Server connection settings
server = 'YOUR_SERVER_NAME'  # Replace with your server name
username = 'YOUR_USERNAME'    # Replace with your username
password = 'YOUR_PASSWORD'    # Replace with your password
database = 'YOUR_DATABASE'    # Replace with your database

# Establish connection
connection = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)
cursor = connection.cursor()

# SQL table creation
cursor.execute('''
    IF OBJECT_ID('personal_data', 'U') IS NULL
    CREATE TABLE personal_data (
        id INT PRIMARY KEY IDENTITY(1,1),
        first_name NVARCHAR(50),
        last_name NVARCHAR(50),
        email NVARCHAR(100),
        phone NVARCHAR(20),
        address NVARCHAR(200),
        passwords NVARCHAR(200)
    )
''')
connection.commit()

# Define routes for the app
@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        passwords = request.form['passwords']

        # Validation check for empty fields
        if not first_name or not last_name or not email or not phone or not address or not passwords:
            flash('All fields are required!', 'error')
            return redirect(url_for('index'))

        # Insert user data into the SQL database
        cursor.execute('''
            INSERT INTO personal_data (first_name, last_name, email, phone, address, passwords)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, phone, address, passwords))
        connection.commit()

        flash('Data submitted successfully!', 'success')
        return redirect(url_for('index'))

    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    app.run(debug=True)