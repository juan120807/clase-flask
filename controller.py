from flask import Blueprint, jsonify, request
import pymysql
from conexion import get_db_connection

# Crea un Blueprint para el endpoint de ciclista
ciclista = Blueprint('ciclista', __name__)

# Create a GET endpoint
@ciclista.route('/ciclista', methods=['GET'])
def get_users():
    try:
        conn = get_db_connection()  # Connect to the database
        cursor = conn.cursor(pymysql.cursors.DictCursor)  # Return results as dictionaries
        cursor.execute('SELECT * FROM ciclista')  # Execute a SQL query
        users = cursor.fetchall()  # Fetch all rows from the result
        return jsonify(users)
    except Exception as e:
        print(f"Ocurrio un error: {e}")
        return jsonify('No se pudo ejecutar la consulta')
    finally:
        print('llega')
        if conn != None:
            conn.close()


@ciclista.route('/ciclistaByDorsal', methods=['GET'])
def get_ciclista_by_id():
    dorsal = request.args.get('dorsal')
    conn = get_db_connection()  # Connect to the database
    cursor = conn.cursor(pymysql.cursors.DictCursor)  # Return results as dictionaries
    cursor.execute('SELECT * FROM ciclista where dorsal='+dorsal)  # Execute a SQL query
    users = cursor.fetchall()  # Fetch all rows from the result
    conn.close()  # Close the database connection

    return jsonify(users)

@ciclista.route('/ciclista', methods=['POST'])
def create_user():
    data = request.get_json()  # Obtener los datos JSON del cuerpo de la solicitud
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Suponiendo que los datos incluyen 'nombre' y 'edad'
        sql = "INSERT INTO ciclista (dorsal, nombre, edad, nomeq) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (data['dorsal'], data['nombre'], data['edad'], data['nomeq']))
        conn.commit()  # Confirmar la transacción
        return jsonify({'message': 'Ciclista creado exitosamente'}), 201
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return jsonify('No se pudo crear el ciclista'), 500
    finally:
        if conn:
            conn.close()

@ciclista.route('/ciclista/<int:dorsal>', methods=['PUT'])
def update_user(dorsal):
    data = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Suponiendo que los datos incluyen 'nombre' y 'edad'
        sql = "UPDATE ciclista SET nombre = %s, edad = %s, nomeq = %s WHERE dorsal = %s"
        cursor.execute(sql, (data['nombre'], data['edad'], data['nomeq'], dorsal))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'Ciclista no encontrado'}), 404
        return jsonify({'message': 'Ciclista actualizado exitosamente'})
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return jsonify('No se pudo actualizar el ciclista'), 500
    finally:
        if conn:
            conn.close()
            
@ciclista.route('/ciclista/<int:dorsal>', methods=['DELETE'])
def delete_user(dorsal):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM ciclista WHERE dorsal = %s"
        cursor.execute(sql, (dorsal,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'message': 'Ciclista no encontrado'}), 404
        return jsonify({'message': 'Ciclista eliminado exitosamente'})
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return jsonify('No se pudo eliminar el ciclista'), 500
    finally:
        if conn:
            conn.close()