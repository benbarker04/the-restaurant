from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# Get database URL from environment variable
DATABASE_URL = os.environ['postgres://apzdnqje:cG-h_wvZQXjG2hSOUNowcQ3Gn4besIcq@flora.db.elephantsql.com/apzdnqje']

# Define a function to create a connection to the ElephantSQL database
def create_connection():
    return psycopg2.connect(DATABASE_URL)

# Define a function to create a table in the database if it doesn't exist already
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bookings
                      (id SERIAL PRIMARY KEY,
                       name TEXT,
                       email TEXT,
                       phone TEXT,
                       date DATE,
                       time TIME,
                       guests INTEGER,
                       special_requests TEXT)''')
    conn.commit()
    conn.close()

# Route for the booking form
@app.route('/booking', methods=['GET'])
def booking_form():
    return render_template('booking.html')

# Route to handle form submission
@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    create_table()  # Ensure the table exists
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        date = request.form['date']
        time = request.form['time']
        guests = request.form['guests']
        special_requests = request.form['special_requests']

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO bookings
                          (name, email, phone, date, time, guests, special_requests)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                       (name, email, phone, date, time, guests, special_requests))
        conn.commit()
        conn.close()

        return "Booking submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)
