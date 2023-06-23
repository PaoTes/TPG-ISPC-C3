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
