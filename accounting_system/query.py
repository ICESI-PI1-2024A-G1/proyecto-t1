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

# Ejecuta una consulta SQL para obtener todas las tablas en la base de datos
cur.execute(
    """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
"""
)

# Obtiene los nombres de las tablas
tables = cur.fetchall()

# Para cada tabla, ejecuta una consulta DROP TABLE para eliminar la tabla
for table in tables:
    print(f"Dropping table: {table[0]}")
    cur.execute(
        f"""
        DO $$ BEGIN
            IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table[0]}') THEN
                EXECUTE 'DROP TABLE IF EXISTS "{table[0]}" CASCADE';
            END IF;
        END $$;
    """
    )
    conn.commit()

# Cierra la conexión
cur.close()
conn.close()
