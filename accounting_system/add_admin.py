import psycopg2

# Conéctate a la base de datos
conn = psycopg2.connect(
    host="dpg-comk19ocmk4c739n55g0-a.oregon-postgres.render.com",
    database="productionccsa",
    user="productionccsa_user",
    password="EhRr6qjUD0gaQib8VdJwJ1WSo8E73fGL",
)

# Crea un cursor
cur = conn.cursor()

# Define los datos del usuario
user_data = {
    "id": "10101010",
    "username": "Admin",
    "email": "ccsa101010@gmail.com",
    "password": "10101010",
    "first_name": "Accounting",
    "last_name": "Admin",
    "is_member": False,
    "is_leader": False,
    "is_superuser": True,
    "is_applicant": False,
    "is_none": False,
}

# Ejecuta una consulta SQL para insertar el nuevo usuario
cur.execute(
    """
    INSERT INTO auth_user_mod (id, username, email, password, first_name, last_name, is_member, is_leader, is_superuser, is_applicant, is_none)
    VALUES (%(id)s, %(username)s, %(email)s, %(password)s, %(first_name)s, %(last_name)s, %(is_member)s, %(is_leader)s, %(is_superuser)s, %(is_applicant)s, %(is_none)s)
    """,
    user_data,
)

# Confirma la transacción
conn.commit()

# Cierra la conexión
cur.close()
conn.close()
