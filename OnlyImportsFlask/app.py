from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import random
import string
from datetime import datetime

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'onlyimports1.clmkgkggqumv.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'weareonlyimports'
app.config['MYSQL_DB'] = 'OnlyImports'

mysql = MySQL(app)

# Function to generate random ID starting with a prefix
def generate_id(prefix):
    return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))

# Sales representatives and their IDs
sales_reps = [
    {'name': 'Bob Smith', 'id': 'SR1'},
    {'name': 'Jimmy Joe', 'id': 'SR2'},
    {'name': 'Jill Johnson', 'id': 'SR3'}
]

# Route to display the home page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# Route to display the add car inventory form
@app.route('/add_inventory')
def add_inventory_form():
    return render_template('add_inventory.html')

# Route to handle adding car inventory
@app.route('/add_inventory', methods=['POST'])
def add_inventory():
    try:
        # Get form data
        car_id = request.form['car_id']
        dealership_id = request.form['dealership_id']
        car_name = request.form['car_name']
        year = request.form['year']
        engine_type = request.form['engine_type']
        fuel_type = request.form['fuel_type']
        mileage = request.form['mileage']

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query to insert data into Inventory table
        cur.execute("INSERT INTO Inventory (Car_ID, Dealership_ID, Car_Name, Year, Engine_Type, Fuel_Type, Mileage) VALUES (%s, %s, %s, %s, %s, %s, %s)", (car_id, dealership_id, car_name, year, engine_type, fuel_type, mileage))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        return 'Car inventory added successfully!'
    except Exception as e:
        return str(e)

# Route to display the add order details form
@app.route('/add_order_details')
def add_order_details_form():
    return render_template('add_order_details.html', order_id=generate_id('O'), car_id=generate_id('Car'), customer_id=generate_id('Customer'), date_placed=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# Route to handle adding order details
@app.route('/add_order_details', methods=['POST'])
def add_order_details():
    try:
        # Get form data
        customer_name = request.form['customer_name']
        customer_city = request.form['customer_city']
        phone_number = request.form['phone_number']
        email_address = request.form['email_address']
        order_id = request.form['order_id']
        car_id = request.form['car_id']
        customer_id = request.form['customer_id']
        date_placed = request.form['date_placed']

        # Select a random sales representative
        sales_rep = random.choice(sales_reps)
        sales_rep_id = sales_rep['id']

        # Create cursor
        cur = mysql.connection.cursor()

        # Insert data into Customer table
        cur.execute("INSERT INTO Customer (Customer_ID, Customer_Name, Customer_City, Phone_Number, Email_Address, Order_ID, SalesRep_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)", (customer_id, customer_name, customer_city, phone_number, email_address, order_id, sales_rep_id))

        # Insert data into Orders table
        cur.execute("INSERT INTO Orders (Order_ID, Car_ID, Customer_ID, Date_Placed) VALUES (%s, %s, %s, %s)", (order_id, car_id, customer_id, date_placed))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        return 'Order details added successfully!'
    except Exception as e:
        return str(e)

    # Route to get inventory data
@app.route('/inventory', methods=['GET'])
def get_inventory():
    try:
        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query to fetch all data from Inventory table
        cur.execute("SELECT Car_Name, Year, Mileage, imageURL FROM Inventory")

        # Fetch all rows
        inventory_data = cur.fetchall()

        # Close connection
        cur.close()

        # Render HTML template with inventory data
        return render_template('inventory.html', inventory_data=inventory_data)

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=False)
