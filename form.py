from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

import base64
from psycopg2 import sql

app = Flask(__name__)
CORS(app)

# Database connection configuration
conn = psycopg2.connect(
    dbname="gepnicas_infra",
    user="postgres",
    password="Preethi@31",
    host="localhost",
    port="5432"
)

# Define a route to handle POST requests
@app.route('/postConfigMaster', methods=['POST'])
def update_data():
    # Get the JSON data from the request
    data = request.get_json()

    # Extract data from JSON object
    instancename = data.get('instancename')
    datacentre = data.get('datacentre')
    portal_category = data.get('portal_category')
    ip_segment = data.get('ip_segment')
    url = data.get('url')
    xmluserid = data.get('xmluserid')
    msrslno = data.get('msrslno')
    nesdcode = data.get('nesdcode')
    running_from = data.get('running_from')
    storage_box = data.get('storage_box')
    primary_webnode1 = data.get('primary_webnode1')
    primary_webnode2 = data.get('primary_webnode2')
    primary_webscript1 = data.get('primary_webscript1')
    primary_webscript2 = data.get('primary_webscript2')
    primary_workerfile = data.get('primary_workerfile')
    primary_gepbalancer = data.get('primary_gepbalancer')
    primary_blueworkder = data.get('primary_blueworkder')
    primary_greenworkder = data.get('primary_greenworkder')
    primary_apacheconf = data.get('primary_apacheconf')
    primary_apachessl = data.get('primary_apachessl')
    primary_appnode1 = data.get('primary_appnode1')
    primary_appnode2 = data.get('primary_appnode2')
    primary_appscript11 = data.get('primary_appscript11')
    primary_appscript12 = data.get('primary_appscript12')
    primary_appscript21 = data.get('primary_appscript21')
    primary_appscript22 = data.get('primary_appscript22')
    primary_appuser = data.get('primary_appuser')
    primary_repuser = data.get('primary_repuser')
    primary_repscript11 = data.get('primary_repscript11')
    primary_repscript21 = data.get('primary_repscript21')
    primary_mobscript11 = data.get('primary_mobscript11')
    primary_mobscript21 = data.get('primary_mobscript21')
    primary_dbnrdrnode = data.get('primary_dbnrdrnode')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # SQL query to insert data into the database
    sql_query = """
    INSERT INTO gepnicas_primary_infra (
        instancename, datacentre, portal_category, ip_segment, url, xmluserid, msrslno, nesdcode, running_from, storage_box,
        primary_webnode1, primary_webnode2, primary_webscript1, primary_webscript2, primary_workerfile, primary_gepbalancer,
        primary_blueworkder, primary_greenworkder, primary_apacheconf, primary_apachessl, primary_appnode1, primary_appnode2,
        primary_appscript11, primary_appscript12, primary_appscript21, primary_appscript22, primary_appuser, primary_repuser,
        primary_repscript11, primary_repscript21, primary_mobscript11, primary_mobscript21, primary_dbnrdrnode
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql_query, (
        instancename, datacentre, portal_category, ip_segment, url, xmluserid, msrslno, nesdcode, running_from, storage_box,
        primary_webnode1, primary_webnode2, primary_webscript1, primary_webscript2, primary_workerfile, primary_gepbalancer,
        primary_blueworkder, primary_greenworkder, primary_apacheconf, primary_apachessl, primary_appnode1, primary_appnode2,
        primary_appscript11, primary_appscript12, primary_appscript21, primary_appscript22, primary_appuser, primary_repuser,
        primary_repscript11, primary_repscript21, primary_mobscript11, primary_mobscript21, primary_dbnrdrnode
    ))

    # Commit the transaction
    conn.commit()

    # Close the cursor
    cursor.close()

    # Return a JSON response
    return jsonify({'message': 'Data inserted successfully'}), 200



@app.route('/updateConfigMaster', methods=['POST'])
def update():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extract data from JSON object
        instancename = data.get('instancename')
        datacentre = data.get('datacentre')
        portal_category = data.get('portal_category')
        ip_segment = data.get('ip_segment')
        url = data.get('url')
        xmluserid = data.get('xmluserid')
        msrslno = data.get('msrslno')
        nesdcode = data.get('nesdcode')
        running_from = data.get('running_from')
        storage_box = data.get('storage_box')
        primary_webnode1 = data.get('primary_webnode1')
        primary_webnode2 = data.get('primary_webnode2')
        primary_webscript1 = data.get('primary_webscript1')
        primary_webscript2 = data.get('primary_webscript2')
        primary_workerfile = data.get('primary_workerfile')
        primary_gepbalancer = data.get('primary_gepbalancer')
        primary_blueworkder = data.get('primary_blueworkder')
        primary_greenworkder = data.get('primary_greenworkder')
        primary_apacheconf = data.get('primary_apacheconf')
        primary_apachessl = data.get('primary_apachessl')
        primary_appnode1 = data.get('primary_appnode1')
        primary_appnode2 = data.get('primary_appnode2')
        primary_appscript11 = data.get('primary_appscript11')
        primary_appscript12 = data.get('primary_appscript12')
        primary_appscript21 = data.get('primary_appscript21')
        primary_appscript22 = data.get('primary_appscript22')
        primary_appuser = data.get('primary_appuser')
        primary_repuser = data.get('primary_repuser')
        primary_repscript11 = data.get('primary_repscript11')
        primary_repscript21 = data.get('primary_repscript21')
        primary_mobscript11 = data.get('primary_mobscript11')
        primary_mobscript21 = data.get('primary_mobscript21')
        primary_dbnrdrnode = data.get('primary_dbnrdrnode')

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # SQL query to update data in the database
        sql_query = """
        UPDATE gepnicas_primary_infra
        SET 
            datacentre = %s, 
            portal_category = %s, 
            ip_segment = %s, 
            url = %s, 
            xmluserid = %s, 
            msrslno = %s, 
            nesdcode = %s, 
            running_from = %s, 
            storage_box = %s, 
            primary_webnode1 = %s, 
            primary_webnode2 = %s, 
            primary_webscript1 = %s, 
            primary_webscript2 = %s, 
            primary_workerfile = %s, 
            primary_gepbalancer = %s, 
            primary_blueworkder = %s, 
            primary_greenworkder = %s, 
            primary_apacheconf = %s, 
            primary_apachessl = %s, 
            primary_appnode1 = %s, 
            primary_appnode2 = %s, 
            primary_appscript11 = %s, 
            primary_appscript12 = %s, 
            primary_appscript21 = %s, 
            primary_appscript22 = %s, 
            primary_appuser = %s, 
            primary_repuser = %s, 
            primary_repscript11 = %s, 
            primary_repscript21 = %s, 
            primary_mobscript11 = %s, 
            primary_mobscript21 = %s, 
            primary_dbnrdrnode = %s
        WHERE instancename = %s
        """

        cursor.execute(sql_query, (
            datacentre, portal_category, ip_segment, url, xmluserid, msrslno, nesdcode, running_from, storage_box,
            primary_webnode1, primary_webnode2, primary_webscript1, primary_webscript2, primary_workerfile, primary_gepbalancer,
            primary_blueworkder, primary_greenworkder, primary_apacheconf, primary_apachessl, primary_appnode1, primary_appnode2,
            primary_appscript11, primary_appscript12, primary_appscript21, primary_appscript22, primary_appuser, primary_repuser,
            primary_repscript11, primary_repscript21, primary_mobscript11, primary_mobscript21, primary_dbnrdrnode,
            instancename
        ))

        # Commit the transaction
        conn.commit()

        # Close the cursor
        cursor.close()

        # Check if any rows were updated
        if cursor.rowcount == 1:
            return jsonify({'message': 'Data updated successfully'}), 200
        else:
            return jsonify({'message': 'No record found for update'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/getConfigMaster', methods=['GET'])
def get_records_by_instancename():
    try:
        # Get the JSON data from the request
        instancename = request.args.get('instancename')

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        if instancename:
            # SQL query to select records by instancename
            sql_query = """
            SELECT * FROM gepnicas_primary_infra
            WHERE instancename = %s
            """

            # Execute the query
            cursor.execute(sql_query, (instancename,))
        else:
            # SQL query to select all records when no instancename is provided
            sql_query = "SELECT * FROM gepnicas_primary_infra"

            # Execute the query
            cursor.execute(sql_query)

        # Fetch all records
        records = cursor.fetchall()

        # Close the cursor
        cursor.close()

        # Convert records to a list of dictionaries for JSON serialization
        records_list = []
        for row in records:
            record_dict = {
                'instancename': row[0],
                'datacentre': row[1],
                'portal_category': row[2],
                'ip_segment': row[3],
                'url': row[4],
                'xmluserid': row[5],
                'msrslno': row[6],
                'nesdcode': row[7],
                'running_from': row[8],
                'storage_box': row[9],
                'primary_webnode1': row[10],
                'primary_webnode2': row[11],
                'primary_webscript1': row[12],
                'primary_webscript2': row[13],
                'primary_workerfile': row[14],
                'primary_gepbalancer': row[15],
                'primary_blueworkder': row[16],
                'primary_greenworkder': row[17],
                'primary_apacheconf': row[18],
                'primary_apachessl': row[19],
                'primary_appnode1': row[20],
                'primary_appnode2': row[21],
                'primary_appscript11': row[22],
                'primary_appscript12': row[23],
                'primary_appscript21': row[24],
                'primary_appscript22': row[25],
                'primary_appuser': row[26],
                'primary_repuser': row[27],
                'primary_repscript11': row[28],
                'primary_repscript21': row[29],
                'primary_mobscript11': row[30],
                'primary_mobscript21': row[31],
                'primary_dbnrdrnode': row[32]
            }
            records_list.append(record_dict)

        # Return JSON response with matching records
        return jsonify({'records': records_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='192.168.0.113', port=8000, debug=True)
