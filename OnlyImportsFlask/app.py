from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'onlyimports1.clmkgkggqumv.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'weareonlyimports'
app.config['MYSQL_DB'] = 'OnlyImports'

mysql = MySQL(app)

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

if __name__ == '__main__':
    app.run(debug=True)