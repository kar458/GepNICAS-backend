from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import psycopg2
import base64
from psycopg2 import sql

app = Flask(__name__)
CORS(app)

# Database connection configuration
DB_CONFIG = {
    'host': '127.0.0.1',  # Replace with your PostgreSQL host
    'dbname': 'gepnicas',  # Replace with your database name
    'user': 'postgres',  # Replace with your PostgreSQL username
    'password': 'Preethi@31',  # Replace with your PostgreSQL password
    'port': '5432'  # Default port is 5432
}

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_CONFIG['host'],
        dbname=DB_CONFIG['dbname'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        port=DB_CONFIG['port']
    )
    return conn
#implement try catch block
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, portalname, logo FROM gepnicas_logos')
    alerts = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Convert binary data to base64 string
    alerts_with_base64 = [
        {
            'id': alert[0],
            'portalname': alert[1],
            'logo': base64.b64encode(alert[2]).decode('utf-8')
        } for alert in alerts
    ]
    
    return render_template('index.html', alerts=alerts_with_base64)

# removed the getvalue sample get method

@app.route('/getImages', methods=['GET'])
def getImages():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id,instancename, portalname, logo FROM gepnicas_logos')
    images = cursor.fetchall()
    cursor.close()
    conn.close()

    images_with_base64 = [
        {
            'id': image[0],
            'instancename':image[1],
            'portalname': image[2],
            'logo': base64.b64encode(image[3]).decode('utf-8')
        } for image in images
    ]

    return jsonify(images_with_base64)
#for logos and images
#################################################################################################
def get_instancename_count(instancename):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to get total count
    query_total = sql.SQL("SELECT COUNT(*) FROM gepnicas_bids_tenders_master WHERE instancename = %s")
    cursor.execute(query_total, (instancename,))
    count_total = cursor.fetchone()[0]

    # Query to get count where archivestatus is 'SyncCompleted'
    query_sync_completed = sql.SQL("SELECT COUNT(*) FROM gepnicas_bids_tenders_master WHERE instancename = %s AND archivestatus = 'SyncCompleted'")
    cursor.execute(query_sync_completed, (instancename,))
    count_sync_completed = cursor.fetchone()[0]

#Softlink created

    query_soft_link_created = sql.SQL("SELECT COUNT(*) FROM gepnicas_bids_tenders_master WHERE instancename = %s AND softlinkstatus = 'SoftLinkCreated'")
    cursor.execute(query_soft_link_created, (instancename,))
    count_soft_link_completed = cursor.fetchone()[0]

#Errors
    query_errors = sql.SQL("SELECT COUNT(*) FROM gepnicas_bids_tenders_master WHERE instancename = %s AND archivestatus = 'SyncError-FolderNotFound'")
    cursor.execute(query_errors, (instancename,))
    count_errors = cursor.fetchone()[0]

#Metalink
    query_meta_link_created = sql.SQL("SELECT COUNT(*) FROM gepnicas_bids_tenders_master WHERE instancename = %s AND metadatastatus = 'MetadataPending'")
    cursor.execute(query_meta_link_created, (instancename,))
    count_meta_link = cursor.fetchone()[0]

#Foldersize
    query_folder_size = sql.SQL("SELECT SUM(foldersize) FROM gepnicas_bids_tenders_master WHERE instancename = %s")
    cursor.execute(query_folder_size, (instancename,))
    instance_storage_size = cursor.fetchone()[0]
    print(type(instance_storage_size))
    if instance_storage_size == None:
        instance_storage_size = 0
    else:

        instance_storage_size=instance_storage_size/1000000000


    logo=sql.SQL("SELECT logo from gepnicas_logos WHERE instancename=%s")
    cursor.execute(logo,(instancename,))
    logo_image=cursor.fetchone()[0]



    cursor.close()
    conn.close()

    return {
        'total_count': count_total,
        'sync_completed_count': count_sync_completed,
        'soft_link_created': count_soft_link_completed,
        'errors_count':count_errors,
        'meta_link_created':count_meta_link,
        'instance_storage_size':instance_storage_size,
        'logo': base64.b64encode(logo_image).decode('utf-8')
    }



@app.route('/getInstanceCount', methods=['GET'])


def getInstanceCount():
    instancename = request.args.get('instancename')
    if not instancename:
        return jsonify({'error': 'instancename parameter is required'}), 400

    counts = get_instancename_count(instancename)
    return jsonify({
        'instancename': instancename,
        'counts': counts
    })
#total counts
####################################################################################################


def get_instancename_count_all():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to get total count
    query_total = sql.SQL("SELECT COUNT(*) FROM gepnicas_bids_tenders_master")
    cursor.execute(query_total)
    count_total = cursor.fetchone()[0]

    # Query to get count where archivestatus is 'SyncCompleted'
    query_sync_completed = sql.SQL("SELECT COUNT(*) FROM gepnicas_bids_tenders_master WHERE archivestatus = 'SyncCompleted'")
    cursor.execute(query_sync_completed)
    count_sync_completed = cursor.fetchone()[0]

#Softlink created

    query_soft_link_created = sql.SQL("SELECT COUNT(*) FROM gepnicas_bids_tenders_master WHERE  softlinkstatus = 'SoftLinkCreated'")
    cursor.execute(query_soft_link_created)
    count_soft_link_completed = cursor.fetchone()[0]

#Errors
    query_errors = sql.SQL("SELECT COUNT(*) FROM gepnicas_bids_tenders_master WHERE  archivestatus like '%SyncError%'")

    cursor.execute(query_errors)
    count_errors = cursor.fetchone()[0]

#Metalink
    query_meta_link_created = sql.SQL("SELECT COUNT(*) FROM gepnicas_bids_tenders_master WHERE  metadatastatus = 'MetadataPending'")
    cursor.execute(query_meta_link_created)
    count_meta_link = cursor.fetchone()[0]

#Foldersize
    query_folder_size = sql.SQL("SELECT SUM(foldersize) FROM gepnicas_bids_tenders_master ")
    cursor.execute(query_folder_size)
    instance_storage_size = cursor.fetchone()[0]
    instance_storage_size=instance_storage_size/1000000000


    



    cursor.close()
    conn.close()

    return {
        'total_count': count_total,
        'sync_completed_count': count_sync_completed,
        'soft_link_created': count_soft_link_completed,
        'errors_count':count_errors,
        'meta_link_created':count_meta_link,
        'instance_storage_size':instance_storage_size
    }



@app.route('/getInstanceCountAll', methods=['GET'])

def getInstanceCountAll():
   

    counts = get_instancename_count_all()
    return jsonify({
        
        'counts': counts
    })




#Total records
##############################################################################################



##############################################################################################
#for sending bids and tenders-for both instance and all 
def fetch_bids_and_tenders(cursor, bids_query, tenders_query, params):
    cursor.execute(bids_query, params)
    bids_total = cursor.fetchall()

    cursor.execute(tenders_query, params)
    tender_total = cursor.fetchall()

    bids = [
        {
            'bids_datafolder': bid[0],
            'bids_archivefolder': bid[1]
        } for bid in bids_total
    ]

    tenders = [
        {
            'tenders_datafolder': tender[0],
            'tenders_archivefolder': tender[1]
        } for tender in tender_total
    ]

    return {'bids': bids, 'tenders': tenders}
@app.route('/getBidsTenderInstance', methods=['GET'])
def getBidsTenderInstance():
    conn = get_db_connection()
    cursor = conn.cursor()
    instancename = request.args.get('instancename')

    if instancename:
        bids_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE instancename = %s AND foldertype = 'bids'"
        )
        tenders_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE instancename = %s AND foldertype = 'tender'"
        )
        params = (instancename,)
    else:
        bids_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE foldertype = 'bids'"
        )
        tenders_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE foldertype = 'tender'"
        )
        params = ()

    result = fetch_bids_and_tenders(cursor, bids_query_total, tenders_query_total, params)

    cursor.close()
    conn.close()

    return jsonify(result)

@app.route('/getBidsTenderInstanceArchived', methods=['GET'])
def getBidsTenderInstanceArchived():
    conn = get_db_connection()
    cursor = conn.cursor()
    instancename = request.args.get('instancename')

    if instancename:
        bids_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE instancename = %s AND foldertype = 'bids' AND softlinkstatus = 'SoftLinkCreated'"
        )
        tenders_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE instancename = %s AND foldertype = 'tender' AND softlinkstatus = 'SoftLinkCreated'"
        )
        params = (instancename,)
    else:
        bids_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE foldertype = 'bids' AND softlinkstatus = 'SoftLinkCreated'"
        )
        tenders_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE foldertype = 'tender' AND softlinkstatus = 'SoftLinkCreated'"
        )
        params = ()

    result = fetch_bids_and_tenders(cursor, bids_query_total, tenders_query_total, params)

    cursor.close()
    conn.close()

    return jsonify(result)

@app.route('/getBidsTenderInstanceMetalink', methods=['GET'])
def getBidsTenderInstanceMetalink():
    conn = get_db_connection()
    cursor = conn.cursor()
    instancename = request.args.get('instancename')

    if instancename:
        bids_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE instancename = %s AND foldertype = 'bids' AND metadatastatus != 'MetadataCreated'"
        )
        tenders_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE instancename = %s AND foldertype = 'tender' AND metadatastatus != 'MetadataCteated'"
        )
        params = (instancename,)
    else:
        bids_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE foldertype = 'bids' AND metadatastatus != 'MetadataCreated'"
        )
        tenders_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE foldertype = 'tender' AND metadatastatus != 'MetadataCreated'"
        )
        params = ()

    result = fetch_bids_and_tenders(cursor, bids_query_total, tenders_query_total, params)

    cursor.close()
    conn.close()

    return jsonify(result)

@app.route('/getBidsTenderInstanceError', methods=['GET'])
def getBidsTenderInstanceError():
    conn = get_db_connection()
    cursor = conn.cursor()
    instancename = request.args.get('instancename')

    if instancename:
        bids_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE instancename = %s AND foldertype = 'bids' AND archivestatus LIKE %s"
        )
        tenders_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE instancename = %s AND foldertype = 'tender' AND archivestatus LIKE %s"
        )
        params = (instancename, '%SyncError%')
    else:
        bids_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE foldertype = 'bids' AND archivestatus LIKE %s"
        )
        tenders_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE foldertype = 'tender' AND archivestatus LIKE %s"
        )
        params = ('%SyncError%',)

    result = fetch_bids_and_tenders(cursor, bids_query_total, tenders_query_total, params)

    cursor.close()
    conn.close()

    return jsonify(result)



@app.route('/getBidsTenderInstanceSoftlink', methods=['GET'])
def getBidsTenderInstanceSoftlink():
    conn = get_db_connection()
    cursor = conn.cursor()
    instancename = request.args.get('instancename')

    if instancename:
        bids_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE instancename = %s AND foldertype = 'bids' AND metadatastatus = 'MetadataCreated' AND softlinkstatus != 'SoftLinkCreated'"
        )
        tenders_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE instancename = %s AND foldertype = 'tender' AND metadatastatus = 'MetadataCteated' AND softlinkstatus != 'SoftLinkCreated'"
        )
        params = (instancename,)
    else:
        bids_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE foldertype = 'bids' AND metadatastatus = 'MetadataCreated' AND softlinkstatus != 'SoftLinkCreated'"
        )
        tenders_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE foldertype = 'tender' AND metadatastatus = 'MetadataCreated' AND softlinkstatus != 'SoftLinkCreated'"
        )
        params = ()

    result = fetch_bids_and_tenders(cursor, bids_query_total, tenders_query_total, params)

    cursor.close()
    conn.close()

    return jsonify(result)



@app.route('/getBidsTenderInstanceOnProcess', methods=['GET'])
def getBidsTenderInstanceOnProcess():
    conn = get_db_connection()
    cursor = conn.cursor()
    instancename = request.args.get('instancename')

    if instancename:
        bids_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE instancename = %s AND foldertype = 'bids' AND archivestatus != 'SyncCompleted' AND archivestatus NOT LIKE %s "
        )
        tenders_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE instancename = %s AND foldertype = 'tender' AND archivestatus != 'SyncCompleted' AND archivestatus NOT LIKE %s"
        )
        params = (instancename, '%SyncError%')
    else:
        bids_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE foldertype = 'bids' AND archivestatus != 'SyncCompleted' AND archivestatus NOT LIKE %s"
        )
        tenders_query_total = sql.SQL(
            "SELECT datafolder, archivefolder FROM gepnicas_bids_tenders_master "
            "WHERE foldertype = 'tender' AND archivestatus != 'SyncCompleted' AND archivestatus NOT LIKE %s"
        )
        params = ('%SyncError%',)

    result = fetch_bids_and_tenders(cursor, bids_query_total, tenders_query_total, params)

    cursor.close()
    conn.close()

    return jsonify(result)

@app.route('/postConfigMaster', methods=['GET'])
def get_data():
    # Create a cursor object to execute SQL queries
    conn=get_db_connection()
    cursor = conn.cursor()

    # SQL query to select data from the database for id=1
    sql_query = "SELECT * FROM gepnicas_config_master WHERE id = 1"
    cursor.execute(sql_query)

    # Fetch the result
    result = cursor.fetchone()

    # Close the cursor
    cursor.close()

    # Return a JSON response with the retrieved data
    if result:
        data = {
            'id': result[0],
            'archive_solution_shortname': result[1],
            'archive_solution_fullname': result[2],
            'archive_age_in_years': result[3],
            'nas_storage_capacity': result[7]
        }
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Data not found'}), 404


# Define a route to handle POST requests
@app.route('/postConfigMaster', methods=['POST'])
def update_data():
    # Get the JSON data from the request
    data = request.get_json()
    conn=get_db_connection()

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






#Total records-Instance
#################################################################



if __name__ == '__main__':
    app.run(host='192.168.0.111', port=5000, debug=True)
