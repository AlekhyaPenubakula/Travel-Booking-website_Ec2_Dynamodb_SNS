from flask import Flask, render_template, request, redirect, session
import uuid
import boto3
import os
from decimal import Decimal
from boto3.dynamodb.conditions import Attr

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'devkey')

# AWS Setup
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
sns = boto3.client('sns', region_name='ap-south-1')

# Tables
users_table = dynamodb.Table('travel-Users')
bookings_table = dynamodb.Table('Bookings')

# Static data
from utils.data import transport_data, hotel_data


@app.route('/')
def home():
    return render_template('index.html', logged_in='user' in session)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        response = users_table.get_item(Key={'email': email})
        if 'Item' in response:
            return render_template('register.html', message="User already exists.")
        users_table.put_item(Item={
            'email': email,
            'name': request.form['name'],
            'password': request.form['password'],
            'logins': 0
        })
        return redirect('/login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        response = users_table.get_item(Key={'email': email})
        user = response.get('Item')
        if user and user['password'] == password:
            session['user'] = email
            users_table.update_item(
                Key={'email': email},
                UpdateExpression="ADD logins :inc",
                ExpressionAttributeValues={':inc': Decimal(1)}
            )
            return '''
                <script>
                    localStorage.setItem("loggedIn", "true");
                    window.location.href = "/dashboard";
                </script>
            '''
        return render_template('login.html', message="Invalid credentials.")
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    email = session['user']
    user = users_table.get_item(Key={'email': email}).get('Item')
    response = bookings_table.scan(FilterExpression=Attr('user_email').eq(email))
    return render_template('dashboard.html', name=user['name'], bookings=response['Items'])


# -------- Transport Pages --------

@app.route('/bus', methods=['GET', 'POST'])
def bus():
    if request.method == 'POST':
        s, d, dt = request.form['source'], request.form['destination'], request.form['date']
        buses = [b for b in transport_data['bus'] if b['source'] == s and b['destination'] == d]
        return render_template('bus.html', buses=buses, source=s, destination=d, date=dt)
    return render_template('bus.html', buses=None)


@app.route('/train', methods=['GET', 'POST'])
def train():
    if request.method == 'POST':
        s, d, dt = request.form['source'], request.form['destination'], request.form['date']
        trains = [t for t in transport_data['train'] if t['source'] == s and t['destination'] == d]
        return render_template('train.html', trains=trains, source=s, destination=d, date=dt)
    return render_template('train.html', trains=None)


@app.route('/flight', methods=['GET', 'POST'])
def flight():
    if request.method == 'POST':
        s, d, dt = request.form['source'], request.form['destination'], request.form['date']
        flights = [f for f in transport_data['flight'] if f['source'] == s and f['destination'] == d]
        return render_template('flight.html', flights=flights, source=s, destination=d, date=dt)
    return render_template('flight.html', flights=None)


@app.route('/hotels', methods=['GET', 'POST'])
def hotels():
    if request.method == 'POST':
        city = request.form['city']
        hotels = [h for h in hotel_data if h['location'] == city]
        return render_template('hotels.html', hotels=hotels, city=city)
    return render_template('hotels.html', hotels=None)


@app.route('/select_seats')
def select_seats():
    return render_template("select_seats.html")


@app.route('/book', methods=['POST'])
def book():
    if 'user' not in session:
        return redirect('/login')

    session['pending_booking'] = {
        "booking_id": str(uuid.uuid4())[:8],
        "type": request.form['type'],
        "source": request.form['source'],
        "destination": request.form['destination'],
        "date": request.form['date'],
        "seat": request.form.get('seat', 'N/A'),
        "details": request.form['details'],
        "price": Decimal(request.form['price']),  # Use Decimal for DynamoDB
        "user_email": session['user'],
        "email": session['user']  # Partition key for Bookings
    }
    return render_template("payment.html", booking=session['pending_booking'])


@app.route('/payment', methods=['POST'])
def payment():
    if 'user' not in session or 'pending_booking' not in session:
        return redirect('/login')

    booking = session.pop('pending_booking')
    booking['payment_method'] = request.form['method']
    booking['payment_reference'] = request.form['reference']

    # Save booking in DynamoDB
    bookings_table.put_item(Item=booking)

    # Send Notification
    try:
        sns.publish(
            TopicArn=os.getenv('SNS_TOPIC_ARN'),
            Message=f"Booking Confirmed:\n{booking['details']} on {booking['date']} for ₹{booking['price']}",
            Subject="TravelGo Booking"
        )
    except Exception as e:
        print("SNS Error:", e)

    return redirect('/dashboard')


@app.route('/remove_booking', methods=['POST'])
def remove_booking():
    if 'user' not in session:
        return redirect('/login')
    email = session['user']
    booking_id = request.form.get('booking_id')

    try:
        bookings_table.delete_item(Key={'email': email, 'booking_id': booking_id})
    except Exception as e:
        print("Delete Error:", e)

    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return '''
        <script>
            localStorage.setItem("loggedIn", "false");
            window.location.href = "/";
        </script>
    '''


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
