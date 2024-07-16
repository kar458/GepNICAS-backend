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
def post_config_master():
    data = request.get_json()
    columns = (
        "instancename", "datacentre", "portal_category", "ip_segment", "url", "xmluserid", "msrslno", 
        "nesdcode", "running_from", "storage_box", "primary_webnode1", "primary_webnode2", "primary_webscript1", 
        "primary_webscript2", "primary_workerfile", "primary_gepbalancer", "primary_blueworkder", "primary_greenworkder", 
        "primary_apacheconf", "primary_apachessl", "primary_appnode1", "primary_appnode2", "primary_appscript11", 
        "primary_appscript12", "primary_appscript21", "primary_appscript22", "primary_appuser", "primary_repuser", 
        "primary_repscript11", "primary_repscript21", "primary_mobscript11", "primary_mobscript21", "primary_dbnrdrnode",
        "primary_dbbackupnode", "primary_dbbackuppath"
    )
    values = tuple(data.get(col) for col in columns)

    cursor = conn.cursor()
    sql_query = sql.SQL("""
        INSERT INTO gepnicas_primary_infra ({})
        VALUES ({})
    """).format(
        sql.SQL(', ').join(map(sql.Identifier, columns)),
        sql.SQL(', ').join(sql.Placeholder() * len(columns))
    )
    cursor.execute(sql_query, values)
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Data inserted successfully'}), 200

@app.route('/updateConfigMaster', methods=['POST'])
def update_config_master():
    data = request.get_json()
    columns = (
        "datacentre", "portal_category", "ip_segment", "url", "xmluserid", "msrslno", 
        "nesdcode", "running_from", "storage_box", "primary_webnode1", "primary_webnode2", "primary_webscript1", 
        "primary_webscript2", "primary_workerfile", "primary_gepbalancer", "primary_blueworkder", "primary_greenworkder", 
        "primary_apacheconf", "primary_apachessl", "primary_appnode1", "primary_appnode2", "primary_appscript11", 
        "primary_appscript12", "primary_appscript21", "primary_appscript22", "primary_appuser", "primary_repuser", 
        "primary_repscript11", "primary_repscript21", "primary_mobscript11", "primary_mobscript21", "primary_dbnrdrnode",
        "primary_dbbackupnode", "primary_dbbackuppath"
    )
    values = tuple(data.get(col) for col in columns)
    instancename = data.get('instancename')

    cursor = conn.cursor()
    sql_query = sql.SQL("""
        UPDATE gepnicas_primary_infra
        SET {}
        WHERE instancename = %s
    """).format(
        sql.SQL(', ').join(
            sql.Composed([sql.Identifier(col), sql.SQL(" = "), sql.Placeholder()]) for col in columns
        )
    )
    cursor.execute(sql_query, values + (instancename,))
    conn.commit()
    rows_updated = cursor.rowcount
    cursor.close()

    if rows_updated == 1:
        return jsonify({'message': 'Data updated successfully'}), 200
    else:
        return jsonify({'message': 'No record found for update'}), 404

@app.route('/getConfigMaster', methods=['GET'])
def get_config_master():
    instancename = request.args.get('instancename')
    cursor = conn.cursor()
    if instancename:
        sql_query = "SELECT * FROM gepnicas_primary_infra WHERE instancename = %s"
        cursor.execute(sql_query, (instancename,))
    else:
        sql_query = "SELECT * FROM gepnicas_primary_infra"
        cursor.execute(sql_query)

    records = cursor.fetchall()
    cursor.close()
    records_list = [
        {
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
            'primary_dbnrdrnode': row[32],
            'primary_dbbackupnode': row[33],
            'primary_dbbackuppath': row[34]
        }
        for row in records
    ]
    return jsonify({'records': records_list}), 200

@app.route('/deleteConfigMaster', methods=['DELETE'])
def delete_config_master():
    instancename = request.args.get('instancename')
    if not instancename:
        return jsonify({'error': 'instancename parameter is required'}), 400

    cursor = conn.cursor()
    sql_query = "DELETE FROM gepnicas_primary_infra WHERE instancename = %s"
    cursor.execute(sql_query, (instancename,))
    conn.commit()
    rows_deleted = cursor.rowcount
    cursor.close()

    if rows_deleted == 0:
        return jsonify({'message': 'No records found to delete'}), 404
    else:
        return jsonify({'message': f'{rows_deleted} record(s) deleted'}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(host='192.168.0.112', port=8000, debug=True)
