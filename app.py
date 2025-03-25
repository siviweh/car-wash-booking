from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carwash.db'
db = SQLAlchemy(app)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    car_model = db.Column(db.String(100), nullable=False)
    car_registration = db.Column(db.String(20), nullable=False)
    booking_time = db.Column(db.DateTime, nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    bookings = Booking.query.order_by(Booking.booking_time).all()
    return render_template('index.html', bookings=bookings)

@app.route('/book', methods=['POST'])
def book():
    try:
        customer_name = request.form['customer_name']
        car_model = request.form['car_model']
        car_registration = request.form['car_registration']
        booking_time = datetime.strptime(request.form['booking_time'], '%Y-%m-%dT%H:%M')
        service_type = request.form['service_type']

        booking = Booking(
            customer_name=customer_name,
            car_model=car_model,
            car_registration=car_registration,
            booking_time=booking_time,
            service_type=service_type
        )
        db.session.add(booking)
        db.session.commit()
        flash('Booking successful!', 'success')
    except Exception as e:
        flash('Booking failed. Please try again.', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_booking(id):
    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    flash('Booking cancelled successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
