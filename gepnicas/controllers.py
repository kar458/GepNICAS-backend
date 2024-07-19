from psycopg2 import sql
from database import db

class ConfigController:
    @staticmethod
    def create_data(table_name, data):
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

        db.execute(query, values)
        return {'message': 'Data inserted successfully'}

    @staticmethod
    def read_data(table_name, instancename=None):
        if instancename:
            query = sql.SQL("SELECT * FROM {table} WHERE instancename = %s").format(
                table=sql.Identifier(table_name)
            )
            records = db.fetchall(query, (instancename,))
        else:
            query = sql.SQL("SELECT * FROM {table}").format(
                table=sql.Identifier(table_name)
            )
            records = db.fetchall(query)
        return records

    @staticmethod
    def update_data(table_name, instancename, data):
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

        db.execute(query, values + [instancename])
        return {'message': 'Data updated successfully'}

    @staticmethod
    def delete_data(table_name, instancename):
        query = sql.SQL("""
        DELETE FROM {table}
        WHERE instancename = %s
        """).format(
            table=sql.Identifier(table_name)
        )

        db.execute(query, (instancename,))
        return {'message': 'Data deleted successfully'}
