from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2 import sql

app = Flask(__name__)
CORS(app)

# Function to get a database connection
def get_db_connection():
    return psycopg2.connect(
        dbname="gepnicas_infra",
        user="postgres",
        password="Preethi@31",
        host="localhost",
        port="5432"
    )

# Create a new record
@app.route('/postConfig', methods=['POST'])
def create_data():
    try:
        table_name = request.args.get('table')
        data = request.get_json()

        conn = get_db_connection()
        cursor = conn.cursor()

        columns = list(data.keys())
        values = list(data.values())

        query = sql.SQL("""
        INSERT INTO {table} ({fields})
        VALUES ({placeholders})
        """).format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
            placeholders=sql.SQL(', ').join(sql.Placeholder() * len(values))
        )

        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Data inserted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Read all records
@app.route('/getConfig', methods=['GET'])
def read_data():
    try:
        table_name = request.args.get('table')
        instancename = request.args.get('instancename')

        conn = get_db_connection()
        cursor = conn.cursor()

        if instancename:
            query = sql.SQL("SELECT * FROM {table} WHERE instancename = %s").format(
                table=sql.Identifier(table_name)
            )
            cursor.execute(query, (instancename,))
        else:
            query = sql.SQL("SELECT * FROM {table}").format(
                table=sql.Identifier(table_name)
            )
            cursor.execute(query)

        records = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        cursor.close()
        conn.close()

        result = [dict(zip(columns, row)) for row in records]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
#update
@app.route('/updateConfig', methods=['POST'])
def update_data():
    try:
        table_name = request.args.get('table')
        data = request.get_json()

        conn = get_db_connection()
        cursor = conn.cursor()

        instancename = data.pop('instancename')
        columns = list(data.keys())
        values = list(data.values())

        set_clause = sql.SQL(', ').join(
            sql.SQL("{} = {}").format(sql.Identifier(col), sql.Placeholder()) for col in columns
        )

        query = sql.SQL("""
        UPDATE {table}
        SET {set_clause}
        WHERE instancename = %s
        """).format(
            table=sql.Identifier(table_name),
            set_clause=set_clause
        )

        cursor.execute(query, values + [instancename])
        conn.commit()
        rowcount = cursor.rowcount

        cursor.close()
        conn.close()

        if rowcount == 1:
            return jsonify({'message': 'Data updated successfully'}), 200
        else:
            return jsonify({'message': 'No record found for update'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete a record
@app.route('/deleteConfig', methods=['DELETE'])
def delete_data():
    try:
        table_name = request.args.get('table')
        instancename = request.args.get('instancename')

        if not instancename:
            return jsonify({'error': 'Instance name (instancename) is required in the request'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        query = sql.SQL("""
        DELETE FROM {table}
        WHERE instancename = %s
        """).format(
            table=sql.Identifier(table_name)
        )

        cursor.execute(query, (instancename,))
        conn.commit()
        rowcount = cursor.rowcount

        cursor.close()
        conn.close()

        if rowcount == 1:
            return jsonify({'message': 'Data deleted successfully'}), 200
        else:
            return jsonify({'message': 'No record found for deletion'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='192.168.0.112', port=8111, debug=True)
