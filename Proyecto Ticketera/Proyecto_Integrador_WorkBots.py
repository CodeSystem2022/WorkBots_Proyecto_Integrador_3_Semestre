from typing import List
import psycopg2
import datetime


class Producto:
    def __init__(self, descripcion: str, precio: int, cantidad: int):
        self.descripcion = descripcion
        self.precio = precio
        self.cantidad = cantidad
        self.subtotal = precio * cantidad


# Función para establecer la conexión a la base de datos
def establecer_conexion():
    try:
        conexion = psycopg2.connect(
            host="127.0.0.1",
            database="Ticketera",
            user="postgres",
            password="admin"
        )
        print("Conexión establecida correctamente")
        return conexion
    except (Exception, psycopg2.Error) as error:
        print("Error al conectar a la base de datos:", error)

#funcion para crear las tablas en la base de datos
def crear_tablas():
    conexion = establecer_conexion()
    if conexion is not None:
        try:
            cursor = conexion.cursor()

            # Crear tabla de productos
            crear_tabla_productos = """
            CREATE TABLE IF NOT EXISTS productos (
                id SERIAL PRIMARY KEY,
                descripcion VARCHAR(100) NOT NULL,
                precio NUMERIC(10, 2) NOT NULL
            )
            """
            cursor.execute(crear_tabla_productos)
            conexion.commit()

            # Crear tabla de clientes
            crear_tabla_clientes = """
            CREATE TABLE IF NOT EXISTS clientes (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL
            )
            """
            cursor.execute(crear_tabla_clientes)
            conexion.commit()

            # Crear tabla de ventas
            crear_tabla_ventas = """
            CREATE TABLE IF NOT EXISTS ventas (
                id SERIAL PRIMARY KEY,
                fecha TIMESTAMP DEFAULT NOW(),
                id_cliente INTEGER REFERENCES clientes (id),
                id_producto INTEGER REFERENCES productos (id),
                cantidad NUMERIC(10, 2) NOT NULL
            )
            """
            cursor.execute(crear_tabla_ventas)
            conexion.commit()

            cursor.close()
            print("Tablas creadas correctamente")

        except (Exception, psycopg2.Error) as error:
            print("Error al crear las tablas:", error)
        finally:
            if conexion is not None:
                conexion.close()
                print("Conexión cerrada")

# Función para obtener precio del producto
def obtener_precio_producto(producto_id):
    conexion = establecer_conexion()
    if conexion is not None:
        try:
            cursor = conexion.cursor()
            # consultar el precio del producto en la bd

            cursor.execute("SELECT precio FROM productos WHERE id = %s", (producto_id))
            result = cursor.fetchone()
            if result:
                precio = int(result[0])
                return precio
            else:
                return None
        except (Exception, psycopg2.Error) as error:
            print("Error en la busqueda de precio de producto: ", error)
        finally:
            if conexion is not None:
                conexion.close()
                print("Conexión cerrada")


#funcion para obtener la descripcion del producto
def obtener_descripcion_producto(producto_id):
    conexion = establecer_conexion()

    if conexion is not None:
        try:
            cursor = conexion.cursor()
            # consultar el precio del producto en la bd
            cursor.execute("SELECT descripcion FROM productos WHERE id = %s", (producto_id))
            result = cursor.fetchone()
            if result:
                descripcion = result[0]
                return descripcion
            else:
                return None
        except (Exception, psycopg2.Error) as error:
            print("Error en la busqueda de descripcion de producto: ", error)
        finally:
            if conexion is not None:
                conexion.close()
                print("Conexión cerrada")


# Función para insertar un cliente en la base de datos
def insertar_cliente(nombre):
    conexion = establecer_conexion()
    if conexion is not None:
        try:
            cursor = conexion.cursor()

            insertar_cliente = """
            INSERT INTO clientes (nombre)
            VALUES (%s)
            """
            cursor.execute(insertar_cliente, (nombre,))
            conexion.commit()

            cursor.close()
            print("Cliente insertado correctamente")
        except (Exception, psycopg2.Error) as error:
            print("Error al insertar el cliente:", error)
        finally:
            if conexion is not None:
                conexion.close()
                print("Conexión cerrada")

# Función para insertar una venta en la base de datos
def insertar_venta(id_cliente, id_producto, cantidad):
    conexion = establecer_conexion()
    if conexion is not None:
        try:
            cursor = conexion.cursor()

            insertar_venta = """
            INSERT INTO ventas (id_cliente, id_producto, cantidad)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insertar_venta, (id_cliente, id_producto, cantidad))
            conexion.commit()

            cursor.close()
            print("Venta registrada correctamente")
        except (Exception, psycopg2.Error) as error:
            print("Error al registrar la venta:", error)
        finally:
            if conexion is not None:
                conexion.close()
                print("Conexión cerrada")

# Función para agregar un producto al carrito de compras
def agregar_producto(productos: List[Producto]):
    producto_id = input('Ingrese el id del producto: ')
    descripcion = obtener_descripcion_producto(producto_id)
    precio = obtener_precio_producto(producto_id)
    cantidad = int(input('Ingrese la cantidad del producto: '))
    producto = Producto(descripcion, precio, cantidad)
    productos.append(producto)

#funcion para solicitar indice que se usa para cambiar o borrar producto
def solicitarIndice():
    return int(input("Ingresa el número de producto (el primero es 0): "))

#funcion para cambiar cantidad del producto
def cambiarCantidad(productos: List[Producto]):
    indice = solicitarIndice()


    if indice < len(productos):
        for producto in productos:
            p = productos[indice]
            nuevaCantidad = float(input("Ingrese nueva Cantidad: "))
            producto.cantidad = nuevaCantidad
            producto.subtotal = producto.precio * nuevaCantidad
            productos[indice] = p
    else:
        print("Numero erroneo, producto no encontrado")
