import sqlite3

class Ley:
    def __init__(self, n_normativa, fecha, descripcion, o_legislativo, p_clave, tnormativa_id, categoria_id, jurisdiccion_id):
        self.n_normativa = n_normativa
        self.fecha = fecha
        self.descripcion = descripcion
        self.o_legislativo = o_legislativo
        self.p_clave = p_clave
        self.tnormativa_id = tnormativa_id
        self.categoria_id = categoria_id
        self.jurisdiccion_id = jurisdiccion_id

class CRUDLeyes:
    def __init__(self):
        self.connection = sqlite3.connect('legislacion.db')
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tnormativa(
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                nombre VARCHAR(50) NOT NULL
                            )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS categoria(
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                nombre VARCHAR(50) NOT NULL
                            )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS jurisdiccion(
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                nombre VARCHAR(50) NOT NULL
                            )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS leyes(
                                id_registro INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                n_normativa VARCHAR(10) NOT NULL,
                                fecha DATETIME NOT NULL,
                                descripcion VARCHAR(300) NOT NULL,
                                o_legislativo VARCHAR(50)NOT NULL,
                                p_clave VARCHAR(50) NOT NULL,
                                tnormativa_id INTEGER REFERENCES tnormativa(id),
                                categoria_id INTEGER REFERENCES categoria(id),
                                jurisdiccion_id INTEGER REFERENCES jurisdiccion(id)
                            )''')
        self.connection.commit()

    def insert_ley(self, ley):
        self.cursor.execute('''INSERT INTO leyes (
                                n_normativa, fecha, descripcion, o_legislativo, p_clave,
                                tnormativa_id, categoria_id, jurisdiccion_id
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                            (ley.n_normativa, ley.fecha, ley.descripcion, ley.o_legislativo,
                             ley.p_clave, ley.tnormativa_id, ley.categoria_id, ley.jurisdiccion_id))
        self.connection.commit()

    def get_all_leys(self):
        self.cursor.execute('''SELECT * FROM leyes''')
        return self.cursor.fetchall()

    def get_ley_by_p_clave(self, p_clave):
        self.cursor.execute('''SELECT * FROM leyes WHERE p_clave = ?''', (p_clave,))
        return self.cursor.fetchall()

    def update_ley(self, ley):
        self.cursor.execute('''UPDATE leyes SET
                            n_normativa = ?, fecha = ?, descripcion = ?, o_legislativo = ?,
                            tnormativa_id = ?, categoria_id = ?, jurisdiccion_id = ?
                        WHERE p_clave = ?''',
                        (ley.n_normativa, ley.fecha, ley.descripcion, ley.o_legislativo,
                         ley.tnormativa_id, ley.categoria_id, ley.jurisdiccion_id, ley.p_clave))
        self.connection.commit()
    def delete_ley(self, ley):
        self.cursor.execute('''DELETE FROM leyes WHERE p_clave = ?''', (ley.p_clave,))
        self.connection.commit()