import psycopg


class UserConnection():

    conn = None

    def __init__(self):
        try:
            self.conn = psycopg.connect(
                "dbname=fastapi_usuarios user=postgres password=postgres host=localhost port=5432")

        except psycopg.OperationalError as err:
            print(err)
            self.conn.close()

    def read_all(self):
        with self.conn.cursor() as cur:
            data = cur.execute("""
                               SELECT * FROM "usuario"
                               """)
            return data.fetchall()

    def read_one(self, id_user):
        with self.conn.cursor() as cur:
            data = cur.execute("""
                               SELECT * FROM "usuario" WHERE id = %s
                               """, (id_user,))
            return data.fetchone()

    def read_one_by_dni(self, dni):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM usuario WHERE dni = %s", (dni,))
        user_data = cur.fetchone()
        cur.close()
        return user_data

    def read_by_city(self, ciudad):
        with self.conn.cursor() as cur:
            cur.execute("""
                        SELECT id, nombre, apellidos, dni, ciudad
                        FROM "usuario" WHERE ciudad = %s
                        """, (ciudad,))
            users_data = cur.fetchall()
        return users_data

    def read_by_province(self, provincia):
        with self.conn.cursor() as cur:
            cur.execute("""
                        SELECT id, dni, ciudad, provincia 
                        FROM "usuario" WHERE provincia = %s
                        """, (provincia,))
            users_data = cur.fetchall()
        return users_data

    def write(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO "usuario"(nombre, apellidos, edad, email, telefono,
                        dni, direccion, ciudad, provincia) VALUES(
                            %(nombre)s, %(apellidos)s, %(edad)s, %(email)s, %(telefono)s,
                            %(dni)s, %(direccion)s, %(ciudad)s, %(provincia)s)
                        """, data)
        self.conn.commit()

    def update(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
                        UPDATE "usuario" SET nombre = %(nombre)s, apellidos = %(apellidos)s, edad = %(edad)s,
                        email = %(email)s, telefono = %(telefono)s, dni = %(dni)s,
                        direccion = %(direccion)s, ciudad = %(ciudad)s, provincia = %(provincia)s
                        WHERE dni = %(dni)s
                        """, data)
        self.conn.commit()

    def delete(self, dni):
        with self.conn.cursor() as cur:
            cur.execute("""
                        DELETE FROM "usuario" WHERE dni = %s
                        """, (dni,))
        self.conn.commit()

    def __def__(self):
        self.conn.close()
