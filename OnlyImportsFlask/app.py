from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'onlyimports1.clmkgkggqumv.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'weareonlyimports'
app.config['MYSQL_DB'] = 'OnlyImports'

mysql = MySQL(app)

# Function to generate random ID starting with a prefix
def generate_id(prefix):
    return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Home route to display both forms
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('add_inventory.html')

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
@app.route('/add_order_details_form')
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

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query to insert data into OrderDetails table
        cur.execute("INSERT INTO OrderDetails (Order_ID, Car_ID, Customer_ID, Date_Placed, Customer_Name, Customer_City, Phone_Number, Email_Address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (order_id, car_id, customer_id, date_placed, customer_name, customer_city, phone_number, email_address))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        return 'Order details added successfully!'
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
