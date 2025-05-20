from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Настройки подключения к MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'hotel_db'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        guest_name = request.form['guest_name']
        passport = request.form['passport']
        phone = request.form['phone']
        room_id = request.form['room_id']
        check_in = request.form['check_in']
        check_out = request.form['check_out']
        employee_id = request.form['employee_id']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                # Добавление гостя
                cursor.execute(
                    "INSERT INTO Guests (guest_name, passport, phone) VALUES (%s, %s, %s)",
                    (guest_name, passport, phone)
                )
                guest_id = cursor.lastrowid

                # Добавление бронирования
                cursor.execute(
                    "INSERT INTO Bookings (guest_book_id, room_book_id, check_in_date, check_out_date, employee_book_id) VALUES (%s, %s, %s, %s, %s)",
                    (guest_id, room_id, check_in, check_out, employee_id)
                )
                conn.commit()
                flash('Бронирование успешно создано!', 'success')
            except Error as e:
                conn.rollback()
                flash(f'Ошибка при создании бронирования: {e}', 'error')
            finally:
                cursor.close()
                conn.close()
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Rooms")
    rooms = cursor.fetchall()
    cursor.execute("SELECT * FROM Employees")
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('book.html', rooms=rooms, employees=employees)

@app.route('/view')
def view():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.bookings_id, g.guest_name, r.room_number, b.check_in_date, b.check_out_date, e.employees_name
        FROM Bookings b
        JOIN Guests g ON b.guest_book_id = g.guest_id
        JOIN Rooms r ON b.room_book_id = r.room_id
        JOIN Employees e ON b.employee_book_id = e.employees_id
    """)
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view.html', bookings=bookings)

@app.route('/edit/<int:booking_id>', methods=['GET', 'POST'])
def edit(booking_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        check_in = request.form['check_in']
        check_out = request.form['check_out']
        room_id = request.form['room_id']
        employee_id = request.form['employee_id']

        try:
            cursor.execute(
                "UPDATE Bookings SET room_book_id = %s, check_in_date = %s, check_out_date = %s, employee_book_id = %s WHERE bookings_id = %s",
                (room_id, check_in, check_out, employee_id, booking_id)
            )
            conn.commit()
            flash('Бронирование успешно обновлено!', 'success')
        except Error as e:
            conn.rollback()
            flash(f'Ошибка при обновлении бронирования: {e}', 'error')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('view'))

    cursor.execute("SELECT * FROM Bookings WHERE bookings_id = %s", (booking_id,))
    booking = cursor.fetchone()
    cursor.execute("SELECT * FROM Rooms")
    rooms = cursor.fetchall()
    cursor.execute("SELECT * FROM Employees")
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('edit.html', booking=booking, rooms=rooms, employees=employees)

@app.route('/delete/<int:booking_id>', methods=['POST'])
def delete(booking_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Bookings WHERE bookings_id = %s", (booking_id,))
        conn.commit()
        flash('Бронирование успешно удалено!', 'success')
    except Error as e:
        conn.rollback()
        flash(f'Ошибка при удалении бронирования: {e}', 'error')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('view'))

if __name__ == '__main__':
    app.run(debug=True)