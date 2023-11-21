# cargadedatos.py
from faker import Faker
import psycopg2
import random

# Configuración de Faker
fake = Faker()

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname="swiftserve",
    user="postgres",
    password="123",
    host="localhost"
)
cursor = conn.cursor()

# Funciones para generar datos ficticios
def generar_datos_restaurante():
    nombre = fake.company()
    direccion = fake.address()
    tipo_cocina = random.choice(['italiana', 'mexicana', 'japonesa', 'china', 'americana'])
    capacidad_maxima = random.randint(10, 100)
    horario_apertura = fake.time()
    horario_cierre = fake.time()
    return nombre, direccion, tipo_cocina, capacidad_maxima, horario_apertura, horario_cierre

# Función para generar datos de cliente con simulación de datos faltantes
def generar_datos_cliente():
    nombre = fake.name()
    direccion = None if random.random() < 0.15 else fake.address()
    telefono = None if random.random() < 0.2 else fake.phone_number()[:20]
    correo = None
    if random.random() > 0.1:
        while True:
            correo = fake.email()
            cursor.execute("SELECT correo FROM Cliente WHERE correo = %s", (correo,))
            if cursor.fetchone() is None:  # Si no hay resultados, el correo es único
                break
    return (nombre, direccion, telefono, correo)


def generar_datos_mesa(restaurante_id):
    numero_mesa = random.randint(1, 20)
    estado = random.choice(['disponible', 'ocupada', 'reservada'])
    capacidad = random.choice([2, 4, 6, 8])
    return numero_mesa, estado, capacidad, restaurante_id

def generar_datos_reserva(mesa_id, cliente_id):
    hora = fake.time()
    numero_comensales = random.randint(1, 8)
    observaciones = fake.sentence(nb_words=6)
    estado = random.choice(['pendiente', 'confirmada', 'cancelada'])
    fecha = fake.date_between(start_date='-1y', end_date='today')
    return hora, numero_comensales, observaciones, estado, fecha, mesa_id, cliente_id

def generar_datos_platos(restaurante_id):
    nombre = fake.word()
    descripcion = fake.text(max_nb_chars=50)
    precio = round(random.uniform(5, 50), 2)
    tipo = random.choice(['entrada', 'principal', 'postre', 'bebida'])
    return nombre, descripcion, precio, tipo, restaurante_id


def generar_datos_proveedor():
    nombre = fake.company()
    direccion = fake.address()
    # Asegurarse de que el teléfono no exceda los 20 caracteres
    telefono = fake.phone_number()[:20]
    tipo_suministro = random.choice(['alimentos', 'bebidas', 'utensilios', 'limpieza'])
    return (nombre, direccion, telefono, tipo_suministro)


# Función para insertar datos y devolver el ID generado
def insertar_datos_devolver_id(sql, data):
    cursor.execute(sql, data)
    conn.commit()  # Asegura que la transacción se complete y el ID se genere
    return cursor.fetchone()[0]# Función para verificar la cantidad de registros en una tabla

def contar_registros(tabla):
    cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
    count = cursor.fetchone()[0]
    print(f"Total de registros en {tabla}: {count}")

# Función para mostrar algunos registros de una tabla
def mostrar_muestra_registros(tabla, limit=10):
    cursor.execute(f"SELECT * FROM {tabla} LIMIT {limit}")
    registros = cursor.fetchall()
    for registro in registros:
        print(registro)



# Consultas SQL con RETURNING para obtener el ID generado
sql_restaurante = """
INSERT INTO Restaurante (nombre, direccion, tipo_cocina, capacidad_maxima, horario_apertura, horario_cierre)
VALUES (%s, %s, %s, %s, %s, %s) RETURNING restaurante_id;
"""
sql_cliente = """
INSERT INTO Cliente (nombre, direccion, telefono, correo)
VALUES (%s, %s, %s, %s) RETURNING cliente_id;
"""
sql_mesa = """
INSERT INTO Mesa (numero_mesa, estado, capacidad, restaurante_id)
VALUES (%s, %s, %s, %s) RETURNING mesa_id;
"""
sql_reserva = """
INSERT INTO Reserva (hora, numero_comensales, observaciones, estado, fecha, mesa_id, cliente_id)
VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING reserva_id;
"""
sql_platos = """
INSERT INTO Platos (nombre, descripcion, precio, tipo, restaurante_id)
VALUES (%s, %s, %s, %s, %s) RETURNING plato_id;
"""
sql_proveedor = """
INSERT INTO Proveedor (nombre, direccion, telefono, tipo_suministro)
VALUES (%s, %s, %s, %s) RETURNING proveedor_id;
"""

# Cantidad de registros a generar por tabla
num_registros = 1000000  # Ejemplo para 1000, 10000, 100000, 1000000

# Generar y añadir datos
for _ in range(num_registros):
    while True:
        try:
            datos_cliente = generar_datos_cliente()
            cliente_id = insertar_datos_devolver_id(sql_cliente, datos_cliente)
            break  # Si la inserción fue exitosa, salimos del bucle
        except psycopg2.errors.UniqueViolation:
            conn.rollback()  # Deshace la transacción actual
            continue  # Genera nuevos datos y reintenta la inserción
               
    datos_restaurante = generar_datos_restaurante()
    restaurante_id = insertar_datos_devolver_id(sql_restaurante, datos_restaurante)
    
    datos_cliente = generar_datos_cliente()
    cliente_id = insertar_datos_devolver_id(sql_cliente, datos_cliente)
    
    datos_mesa = generar_datos_mesa(restaurante_id)
    mesa_id = insertar_datos_devolver_id(sql_mesa, datos_mesa)
    
    datos_reserva = generar_datos_reserva(mesa_id, cliente_id)
    reserva_id = insertar_datos_devolver_id(sql_reserva, datos_reserva)
    
    datos_platos = generar_datos_platos(restaurante_id)
    plato_id = insertar_datos_devolver_id(sql_platos, datos_platos)
    
    datos_proveedor = generar_datos_proveedor()
    proveedor_id = insertar_datos_devolver_id(sql_proveedor, datos_proveedor)
    
# Ejecuta las funciones de verificación después de la inserción de datos
contar_registros('Restaurante')
contar_registros('Cliente')
contar_registros('Mesa')
contar_registros('Reserva')
contar_registros('Platos')
contar_registros('Proveedor')

mostrar_muestra_registros('Cliente')
mostrar_muestra_registros('Reserva')

# Confirmar transacciones y cerrar conexión
cursor.close()
conn.close()
