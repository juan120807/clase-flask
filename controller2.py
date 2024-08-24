from flask import Blueprint, jsonify, request
import pymysql
from conexion import get_db_connection
from conexion import get_db_connection

# Crea un Blueprint para el endpoint de maillot
maillot = Blueprint('maillot', __name__)

# Create a GET endpoint
@maillot.route('/maillot', methods=['GET'])
def get_users():
    try:
        conn = get_db_connection()  # Connect to the database
        cursor = conn.cursor(pymysql.cursors.DictCursor)  # Return results as dictionaries
        cursor.execute('SELECT * FROM maillot')  # Execute a SQL query
        users = cursor.fetchall()  # Fetch all rows from the result
        return jsonify(users)
    except Exception as e:
        print(f"Ocurrio un error: {e}")
        return jsonify('No se pudo ejecutar la consulta')
    finally:
        print('llega')
        if conn != None:
            conn.close()


@maillot.route('/maillotbycolor', methods=['GET'])
def get_maillot_by_id():
    codigo = request.args.get('color')
    conn = get_db_connection()  # Connect to the database
    cursor = conn.cursor(pymysql.cursors.DictCursor)  # Return results as dictionaries
    cursor.execute('SELECT * FROM maillot where codigo='+codigo)  # Execute a SQL query
    users = cursor.fetchall()  # Fetch all rows from the result
    conn.close()  # Close the database connection

    return jsonify(users)

@maillot.route('/maillot', methods=['POST'])
def create_user():
    data = request.get_json()  # Obtener los datos JSON del cuerpo de la solicitud
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Suponiendo que los datos incluyen 'codigo' y 'color'
        sql = "INSERT INTO maillot(codigo, tipo, color,premio) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (data['codigo'], data['tipo'], data['color'], data['premio']))
        conn.commit()  # Confirmar la transacción
        return jsonify({'message': 'maillot creado exitosamente'}), 201
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return jsonify('No se pudo crear el maillot'), 500
    finally:
        if conn:
            conn.close()
            
@maillot.route('/maillot/<string:codigo>', methods=['PUT'])
def update_user(codigo):
    data = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Suponiendo que los datos incluyen 'tipo' y 'color'
        sql = "UPDATE maillot SET tipo = %s, color = %s, premio = %s WHERE codigo = %s"
        cursor.execute(sql, (data['tipo'], data['color'], data['premio'], codigo))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'maillot no encontrado'}), 404
        return jsonify({'message': 'maillot actualizado exitosamente'})
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return jsonify('No se pudo actualizar el maillot'), 500
    finally:
        if conn:
            conn.close()
