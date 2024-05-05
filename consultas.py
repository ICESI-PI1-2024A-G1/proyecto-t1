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

# Ejecuta una consulta SQL para obtener todas las tablas que contienen 'forms' en su nombre
cur.execute(
    """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name LIKE '%forms%'
"""
)

# Obtiene los nombres de las tablas
tables = cur.fetchall()

# Obtiene los nombres de las tablas
for table in tables:
    print(f"Table: {table[0]}")
    cur.execute(f"SELECT * FROM {table[0]} LIMIT 0")
    column_names = [desc[0] for desc in cur.description]
    print("Column names:", column_names)

    # Si la columna 'member_id' existe en la tabla, la elimina
    if "member_id" in column_names:
        cur.execute(f"ALTER TABLE {table[0]} DROP COLUMN member_id")
        conn.commit()
        print(f"Column 'member_id' has been dropped from table {table[0]}")

# Cierra la conexión
cur.close()
conn.close()
