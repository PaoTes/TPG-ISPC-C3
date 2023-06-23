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

def mostrar_menu():
    print("==== MENÚ ====")
    print("1. Agregar ley")
    print("2. Mostrar todas las leyes")
    print("3. Buscar ley por palabra clave")
    print("4. Actualizar ley")
    print("5. Eliminar ley")
    print("6. Salir")

crud = CRUDLeyes()

while True:
    mostrar_menu()
    opcion = input("Ingrese una opción: ")

    if opcion == "1":
        n_normativa = input("Ingrese el número de normativa: ")
        fecha = input("Ingrese la fecha: ")
        descripcion = input("Ingrese la descripción: ")
        o_legislativo = input("Ingrese el órgano legislativo: ")
        p_clave = input("Ingrese la palabra clave: ")
        tnormativa_id = int ( input("\n Seleccione normativa\n1. ley\n2. Norma\n3. Resolucion\nIngrese el ID de la normativa: "))
        categoria_id = int ( input("\n Seleccione categoría\n1. Laboral \n2. Penal \n3. Civil\n4. Comercial\n5. Familia y Sucesiones\n6. Agrario y Ambiental\n7. Minería\n8. Derecho informático\n	Ingrese el ID de la categoría: "))
        jurisdiccion_id = int ( input("\n Seleccion jurisdicción\n1. Nacional\n2. Provincial\n Ingrese el ID de la jurisdicción: "))

        ley = Ley(n_normativa, fecha, descripcion, o_legislativo, p_clave, tnormativa_id, categoria_id, jurisdiccion_id)
        crud.insert_ley(ley)
        print("Ley agregada correctamente.")

    elif opcion == "2":
        leyes = crud.get_all_leys()
        for ley in leyes:
            print(ley)

    elif opcion == "3":
        p_clave = input("Ingrese la palabra clave a buscar: ")
        leyes = crud.get_ley_by_p_clave(p_clave)
        for ley in leyes:
            print(ley)

    elif opcion == "4":
        p_clave = input("Ingrese la palabra clave de la ley a actualizar: ")
        leyes = crud.get_ley_by_p_clave(p_clave)
        if leyes:
            ley_actualizar = leyes[0]
            print("Ingrese los nuevos valores (deje en blanco para mantener los valores existentes):")
            n_normativa = input("Nuevo número de normativa: ")
            fecha = input("Nueva fecha: ")
            descripcion = input("Nueva descripción: ")
            o_legislativo = input("Nuevo órgano legislativo: ")
            tnormativa_id = input("Nuevo ID de la normativa: ")
            categoria_id = input("Nuevo ID de la categoría: ")
            jurisdiccion_id = input("Nuevo ID de la jurisdicción: ")

        if n_normativa:
            ley_actualizar.n_normativa = n_normativa
        if fecha:
            ley_actualizar.fecha = fecha
        if descripcion:
            ley_actualizar.descripcion = descripcion
        if o_legislativo:
            ley_actualizar.o_legislativo = o_legislativo
        if tnormativa_id:
            ley_actualizar.tnormativa_id = tnormativa_id
        if categoria_id:
            ley_actualizar.categoria_id = categoria_id
        if jurisdiccion_id:
            ley_actualizar.jurisdiccion_id = jurisdiccion_id

        crud.update_ley(ley_actualizar)
        print("Ley actualizada correctamente.")

    elif opcion == "5":
        p_clave = input("Ingrese la palabra clave de la ley a eliminar: ")
        leyes = crud.get_ley_by_p_clave(p_clave)
        if leyes:
            ley_eliminar = leyes[0]
            confirmacion = input (f"¿Está seguro de eliminar la ley con palabra clave {ley_eliminar.p_clave}? (S/N): ")
            if confirmacion.upper() == "S":
                crud.delete_ley(ley_eliminar)
                print("Ley eliminada correctamente.")
            else:
                print("La ley no se eliminó.")

    elif opcion == "6":
        break

    else:
        print("Opción inválida. Intente nuevamente.")
