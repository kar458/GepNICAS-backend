from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import psycopg2
import base64
from psycopg2 import sql

app = Flask(__name__)
CORS(app)
# Create the Flask app
app = Flask(__name__)

# Database connection configuration
conn = psycopg2.connect(
    dbname="gias",
    user="postgres",
    password="mathan",
    host="localhost",
    port="5432"
)
@app.route('/',methods=['GET'])
def index():
    return "hello"
# Define a route to handle POST requests
@app.route('/api/update_data', methods=['POST'])
def update_data():
    # Get the JSON data from the request
    data = request.get_json()

    # Extract data from JSON object
    id = 1  # Specify the id you want to update
    short_name = data.get('archive_solution_shortname')
    full_name = data.get('archive_solution_fullname')
    age_in_years = data.get('archive_age_in_years')
    storage_capacity = data.get('nas_storage_capacity')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # SQL query to update data in the database for id=1
    sql_query = "UPDATE gepnicas_config_master SET archive_solution_shortname = %s, archive_solution_fullname = %s, archive_age_in_years = %s, nas_storage_capacity = %s WHERE id = %s"
    cursor.execute(sql_query, (short_name, full_name, age_in_years, storage_capacity, id))

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()

    # Return a JSON response
    return jsonify({'message': 'Data updated successfully'}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(host='192.168.0.107',port=5500,debug=True)
