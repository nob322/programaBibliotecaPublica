"""
----instalar para correr programa-----
pip install reportlab ujson tkcalendar
--------------------------------------
"""
import sys
import os
#Determinar la ruta de 'src' relativa al archivo en ejecución
src_path = os.path.join(os.path.dirname(__file__), 'src')

# Añadir 'src' al sys.path para que Python pueda encontrar los módulos en esa carpeta
#sys.path.append(src_path)
# Verificar que la ruta se añadió correctamente
#print("----------------------------------------")
#print("Ruta añadida al sys.path:", src_path)
#print("Contenido del sys.path:", sys.path)
#print("----------------------------------------")
import tkinter as tk
from tkinter import PhotoImage, messagebox, ttk
from tkinter.ttk import Combobox
from datetime import datetime
from tkcalendar import DateEntry
import random
import ujson
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from src import gestionlibros
from src import gestionprestamos
from src import gestionsocios
from src import interfaz
from src import modules

#modules.saludar1()
# Función para actualizar el reloj
def actualizar_reloj():
   tiempo_actual = datetime.now().strftime("%H:%M:%S")
   label_reloj.config(text=tiempo_actual)
   ventanaPrincipal.after(1000, actualizar_reloj)
    
    
    
# Función para cargar frases desde el archivo frases.json
# Obtener la ruta absoluta de frases.json
file_pathFrases = os.path.join(os.path.dirname(__file__), 'data', 'frases.json')
def cargar_frases():
    with open(file_pathFrases, "r", encoding="utf-8") as file:
        frases = ujson.load(file)
    return frases

# Función para mostrar frases aleatorias cada 10 segundos
def mostrar_frase_aleatoria():
    frase_actual = random.choice(frases)
    top_bar.config(text=frase_actual)
    ventanaPrincipal.after(
        10000, mostrar_frase_aleatoria
    )  # Llamar a mostrar_frase_aleatoria cada 10 segundos




# 1. Registro de Libros:
# Función para leer el archivo JSON y cargar los datos de libros
file_pathLibros = os.path.join(os.path.dirname(__file__), 'data', 'libros.json')
def cargar_datos_libros():
    try:
        with open(file_pathLibros, "r", encoding="utf-8") as f:
            return ujson.load(f)
    except FileNotFoundError:
        return []

# Función para guardar los datos en el archivo JSON
file_pathLibros = os.path.join(os.path.dirname(__file__), 'data', 'libros.json')
def guardar_datos_libros(datos_libros):
    with open(file_pathLibros, "w", encoding="utf-8") as f:
        ujson.dump(datos_libros, f, ensure_ascii=False, indent=4)

datos_libros = cargar_datos_libros()

# Función para buscar un libro en los datos
def buscar_libro(nombre):
    for libro in datos_libros:
        if libro["titulo"].lower() == nombre.lower():
            return libro
    return None

# Función para buscar un libro por ID
def buscar_libro_por_id(id_libro):
    for libro in datos_libros:
        if libro["id_libro"] == id_libro:
            return libro
    return None

# Función para agregar un nuevo libro
def agregar_libro(nuevo_libro):
    global datos_libros
    # Autoincrementar el ID del libro
    nuevo_libro["id_libro"] = max(libro["id_libro"] for libro in datos_libros) + 1
    datos_libros.append(nuevo_libro)
    guardar_datos_libros(datos_libros)

# Función para actualizar un libro existente
def actualizar_libro(id_libro, datos_actualizados):
    for libro in datos_libros:
        if libro["id_libro"] == id_libro:
            libro.update(datos_actualizados)
            guardar_datos_libros(datos_libros)
            return True
    return False

# Función para eliminar un libro
def eliminar_libro(id_libro):
    global datos_libros
    datos_libros = [libro for libro in datos_libros if libro["id_libro"] != id_libro]
    guardar_datos_libros(datos_libros)





# 2. Gestión de Socios:
# Función para leer el archivo JSON y cargar los datos de socios
file_pathSocios = os.path.join(os.path.dirname(__file__), 'data', 'socios.json')
def cargar_datos_socios():
    try:
        with open(file_pathSocios, "r", encoding="utf-8") as f:
            return ujson.load(f)
    except FileNotFoundError:
        return []  # Si el archivo no existe, devuelve una lista vacía

# Función para guardar los datos de socios en el archivo JSON
def guardar_datos_socios(datos_socios):
    socios_ordenados = []
    for socio in datos_socios:
        socio_ordenado = {
            "id_socio": socio["id_socio"],
            "nombre": socio["nombre"],
            "apellido": socio["apellido"],
            "fecha_de_nacimiento": socio["fecha_de_nacimiento"],
            "dirección": socio["dirección"],
            "correo_electrónico": socio["correo_electrónico"],
            "teléfono": socio["teléfono"],
        }
        socios_ordenados.append(socio_ordenado)

    with open(file_pathSocios, "w", encoding="utf-8") as f:
        ujson.dump(datos_socios, f, indent=4, ensure_ascii=False)

# Cargar los datos iniciales de los socios
datos_socios = cargar_datos_socios()

# Función para buscar un socio en los datos
def buscar_socio(nombre):
    for socio in datos_socios:
        if socio["nombre"].lower() == nombre.lower():
            return socio
    return None

# Función para buscar un socio por ID
def buscar_socio_por_id(id_socio):
    for socio in datos_socios:
        if socio["id_socio"] == id_socio:
            return socio
    return None

# Función para modificar un socio existente
def modificar_socio(id_socio, datos_actualizados):
    # Validación de fecha de nacimiento
    if "fecha_nacimiento" in datos_actualizados:
        try:
            datetime.strptime(datos_actualizados["fecha_nacimiento"], "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Error", "Formato de fecha de nacimiento inválido (YYYY-MM-DD)"
            )
            return False

    for socio in datos_socios:
        if socio["id_socio"] == id_socio:
            socio.update(datos_actualizados)
            guardar_datos_socios(datos_socios)
            return True
    return False

# Función para agregar un nuevo socio
def agregar_socio(nuevo_socio):
    # Validación de fecha de nacimiento
    try:
        datetime.strptime(nuevo_socio["fecha_nacimiento"], "%Y-%m-%d")
    except ValueError:
        messagebox.showerror(
            "Error", "Formato de fecha de nacimiento inválido (YYYY-MM-DD)"
        )
        return

    # Asignación automática de ID
    if not datos_socios:
        nuevo_socio["id_socio"] = 1  # Si no hay socios aún, empezar con ID 1
    else:
        nuevo_socio["id_socio"] = max(socio["id_socio"] for socio in datos_socios) + 1

    # Reordenar el nuevo socio con id_socio primero
    nuevo_socio = {
        "id_socio": nuevo_socio["id_socio"],
        "nombre": nuevo_socio["nombre"],
        "apellido": nuevo_socio["apellido"],
        "fecha_de_nacimiento": nuevo_socio["fecha_nacimiento"],
        "dirección": nuevo_socio["direccion"],
        "correo_electrónico": nuevo_socio["correo_electronico"],
        "teléfono": nuevo_socio["telefono"],
    }

    datos_socios.append(nuevo_socio)
    guardar_datos_socios(datos_socios)

# Función para actualizar un socio existente
def actualizar_socio(socio_actualizado):
    for i, socio in enumerate(datos_socios):
        if socio["id_socio"] == socio_actualizado["id_socio"]:
            datos_socios[i] = socio_actualizado
            guardar_datos_socios(datos_socios)
            return

# Función para eliminar un socio existente
def eliminar_socio(id_socio):
    global datos_socios
    datos_socios = [socio for socio in datos_socios if socio["id_socio"] != id_socio]
    guardar_datos_socios(datos_socios)



# 3. Registro de Préstamos y Devoluciones:
# Función para leer el archivo JSON y cargar los datos de préstamos
file_pathPrestamos = os.path.join(os.path.dirname(__file__), 'data', 'prestamos.json')
def cargar_datos_prestamos():
    try:
        with open(file_pathPrestamos, "r", encoding="utf-8") as f:
            return ujson.load(f)
    except FileNotFoundError:
        return []

# Función para guardar los datos de préstamos en el archivo JSON
def guardar_datos_prestamos(datos_prestamos):
    with open(file_pathPrestamos, "w", encoding="utf-8") as f:
        ujson.dump(datos_prestamos, f, indent=4, ensure_ascii=False)

# Cargar los datos iniciales de los préstamos
datos_prestamos = cargar_datos_prestamos()




# Función para manejar el contenido de la búsqueda de libros
def mostrar_busqueda_libros():
    clear_content_frame()

    label = tk.Label(
        content_frame, text="Búsqueda de Libros", font=("Arial", 24), bg="white"
    )
    label.pack(pady=20)

    # Crear la lista desplegable de libros
    lista_libros = [libro["titulo"] for libro in datos_libros]
    combobox_libros = ttk.Combobox(
        content_frame, values=lista_libros, font=("Arial", 14)
    )
    combobox_libros.pack(pady=10)

    result_label = tk.Label(content_frame, font=("Arial", 18), bg="white")
    result_label.pack(pady=10)

    def buscar_y_mostrar_libro():
        titulo_seleccionado = combobox_libros.get()
        libro = buscar_libro(titulo_seleccionado)
        for widget in content_frame.winfo_children():
            if (
                isinstance(widget, tk.Label)
                and widget != label
                and widget != result_label
            ):
                widget.destroy()
        if libro:
            result_label.config(text="")  # Limpiar el mensaje de error previo
            for key, value in libro.items():
                key_text = key.replace(
                    "_", " "
                ).capitalize()  # Formatear la clave para mostrar
                tk.Label(
                    content_frame,
                    text=f"{key_text}: {value}",
                    font=("Arial", 18),
                    bg="white",
                ).pack(pady=2)
        else:
            result_label.config(
                text="Libro inexistente en el registro, intente con otro nombre",
                fg="red",
            )

    button = tk.Button(
        content_frame, text="Buscar", font=("Arial", 18), command=buscar_y_mostrar_libro
    )
    button.pack(pady=10)

# Función para manejar el contenido del registro de libros
def mostrar_registro_libros():
    clear_content_frame()

    label = tk.Label(
        content_frame, text="Registro de Libros", font=("Arial", 24), bg="white"
    )
    label.pack(pady=20)

    campos = [
        "Título",
        "Autor",
        "Editorial",
        "Año de Publicación",
        "Género",
        "Cantidad Disponible",
    ]
    entradas = {}

    for campo in campos:
        tk.Label(content_frame, text=campo, font=("Arial", 18), bg="white").pack(pady=4)
        entry = tk.Entry(content_frame, font=("Arial", 18))
        entry.pack(pady=4)
        entradas[campo] = entry

    result_label = tk.Label(content_frame, font=("Arial", 18), bg="white")
    result_label.pack(pady=10)

    def guardar_libro():
        nuevo_libro = {
            "titulo": entradas["Título"].get(),
            "autor": entradas["Autor"].get(),
            "editorial": entradas["Editorial"].get(),
            "año_de_publicación": int(entradas["Año de Publicación"].get()),
            "genero": entradas["Género"].get(),
            "cantidad_disponible": int(entradas["Cantidad Disponible"].get()),
        }
        agregar_libro(nuevo_libro)
        result_label.config(text="Libro guardado exitosamente", fg="green")
        for entry in entradas.values():
            entry.delete(0, tk.END)

    button = tk.Button(
        content_frame, text="Guardar", font=("Arial", 15), command=guardar_libro
    )
    button.pack(pady=10)

# Función para manejar la modificación de un libro
def mostrar_modificar_libros():
    clear_content_frame()

    label = tk.Label(
        content_frame, text="Modificar Libro", font=("Arial", 24), bg="white"
    )
    label.pack(pady=10)

    label_select = tk.Label(
        content_frame, text="Selecciona un libro:", font=("Arial", 14), bg="white"
    )
    label_select.pack(pady=4)

    lista_libros = [libro["titulo"] for libro in datos_libros]
    combobox_libros = ttk.Combobox(
        content_frame, values=lista_libros, font=("Arial", 14)
    )
    combobox_libros.pack(pady=4)

    campos = [
        "Título",
        "Autor",
        "Editorial",
        "Año de Publicación",
        "Género",
        "Cantidad Disponible",
    ]
    entradas = {}

    for campo in campos:
        tk.Label(content_frame, text=campo + ":", font=("Arial", 14), bg="white").pack(
            pady=4
        )
        entry = tk.Entry(content_frame, font=("Arial", 14))
        entry.pack(pady=4)
        entradas[campo] = entry

    # Bloquear todos los campos excepto "Cantidad Disponible"
    for campo in campos[:-1]:
        entradas[campo].config(state="readonly")

    result_label = tk.Label(content_frame, text="", font=("Arial", 12), bg="white")
    result_label.pack(pady=4)

    def cargar_datos_libro_seleccionado(event):
        titulo_seleccionado = combobox_libros.get()
        libro_a_modificar = next(
            (libro for libro in datos_libros if libro["titulo"] == titulo_seleccionado),
            None,
        )
        if libro_a_modificar:
            entradas["Título"].config(state="normal")
            entradas["Título"].delete(0, tk.END)
            entradas["Título"].insert(0, libro_a_modificar["titulo"])
            entradas["Título"].config(state="readonly")

            entradas["Autor"].config(state="normal")
            entradas["Autor"].delete(0, tk.END)
            entradas["Autor"].insert(0, libro_a_modificar["autor"])
            entradas["Autor"].config(state="readonly")

            entradas["Editorial"].config(state="normal")
            entradas["Editorial"].delete(0, tk.END)
            entradas["Editorial"].insert(0, libro_a_modificar["editorial"])
            entradas["Editorial"].config(state="readonly")

            entradas["Año de Publicación"].config(state="normal")
            entradas["Año de Publicación"].delete(0, tk.END)
            entradas["Año de Publicación"].insert(
                0, libro_a_modificar["año_de_publicación"]
            )
            entradas["Año de Publicación"].config(state="readonly")

            entradas["Género"].config(state="normal")
            entradas["Género"].delete(0, tk.END)
            entradas["Género"].insert(0, libro_a_modificar["genero"])
            entradas["Género"].config(state="readonly")

            entradas["Cantidad Disponible"].delete(0, tk.END)
            entradas["Cantidad Disponible"].insert(
                0, libro_a_modificar["cantidad_disponible"]
            )

    combobox_libros.bind("<<ComboboxSelected>>", cargar_datos_libro_seleccionado)

    def guardar_modificacion_y_finalizar():
        titulo_seleccionado = combobox_libros.get()
        libro_a_modificar = next(
            (libro for libro in datos_libros if libro["titulo"] == titulo_seleccionado),
            None,
        )
        if libro_a_modificar:
            datos_actualizados = {
                "cantidad_disponible": int(entradas["Cantidad Disponible"].get())
            }
            exito = actualizar_libro(libro_a_modificar["id_libro"], datos_actualizados)
            if exito:
                result_label.config(text="Modificación exitosa", fg="green")
            else:
                result_label.config(text="Error en la modificación", fg="red")
        else:
            result_label.config(text="Seleccione un libro para modificar", fg="red")

    tk.Button(
        content_frame,
        text="Guardar y Finalizar",
        font=("Arial", 12),
        command=guardar_modificacion_y_finalizar,
    ).pack(pady=5)

# Función para manejar la eliminación de un libro
def mostrar_eliminar_libros():
    clear_content_frame()

    # Cargar los datos de libros desde el archivo JSON
    global datos_libros #= cargar_datos_libros()

    label = tk.Label(
        content_frame, text="Eliminar Libro", font=("Arial", 24), bg="white"
    )
    label.pack(pady=20)

    listbox = tk.Listbox(content_frame, font=("Arial", 18))
    listbox.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

    # Función para actualizar la lista de libros en el Listbox
    def actualizar_lista_libros():
        listbox.delete(0, tk.END)  # Limpiar la lista antes de actualizar
        for libro in datos_libros:
            listbox.insert(tk.END, libro["titulo"])  # Mostrar solo el título del libro

    # Actualizar la lista de libros al inicio
    actualizar_lista_libros()

    def eliminar_libro():
        selected = listbox.curselection()
        if selected:
            index = selected[0]
            libro_a_eliminar = datos_libros[index]
            datos_libros.remove(libro_a_eliminar)
            guardar_datos_libros(datos_libros)
            clear_content_frame()
            mostrar_eliminar_libros()  # Actualizar la lista después de eliminar
            messagebox.showinfo(
                "Eliminación exitosa",
                f"Libro \"{libro_a_eliminar['titulo']}\" eliminado correctamente.",
            )
        else:
            messagebox.showerror("Error", "Seleccione un libro para eliminar.")

    button = tk.Button(
        content_frame,
        text="Eliminar Libro Seleccionado",
        font=("Arial", 18),
        command=eliminar_libro,
    )
    button.pack(pady=25)



# Función para manejar búsqueda de socios
def mostrar_buscar_socios():
    clear_content_frame()

    # Cargar los datos de socios desde el archivo JSON
    datos_socios = cargar_datos_socios()

    label = tk.Label(
        content_frame, text="Buscar Socios", font=("Arial", 24), bg="white"
    )
    label.pack(pady=20)

    listbox = tk.Listbox(
        content_frame, font=("Arial", 18), height=6, bg="green", fg="white"
    )
    listbox.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

    # Función para actualizar la lista de socios en el Listbox
    def actualizar_lista_socios():
        listbox.delete(0, tk.END)  # Limpiar la lista antes de actualizar
        for socio in datos_socios:
            listbox.insert(
                tk.END, f"{socio['nombre']} {socio['apellido']}"
            )  # Mostrar nombre y apellido del socio

    # Actualizar la lista de socios al inicio
    actualizar_lista_socios()

    # Frame para los campos de detalles del socio
    detail_frame = tk.Frame(content_frame, bg="white")
    detail_frame.pack(pady=20)

    # Función para mostrar detalles del socio al seleccionar uno de la lista
    def seleccionar_socio(event):
        indice_seleccionado = listbox.curselection()
        if indice_seleccionado:
            indice = indice_seleccionado[0]
            socio_seleccionado = datos_socios[indice]

            # Limpiar el frame de detalles antes de agregar nuevos widgets
            for widget in detail_frame.winfo_children():
                widget.destroy()

            # Campos de detalles del socio
            campos = [
                "Nombre",
                "Apellido",
                "Fecha de Nacimiento",
                "Dirección",
                "Correo Electrónico",
                "Teléfono",
            ]
            for campo in campos:
                clave = campo.lower().replace(" ", "_")
                if clave in socio_seleccionado:
                    valor = socio_seleccionado[clave]
                    tk.Label(
                        detail_frame,
                        text=f"{campo}: {valor}",
                        font=("Arial", 18),
                        bg="white",
                    ).pack(pady=5)
                else:
                    print(f"Clave {clave} no encontrada en socio_seleccionado")

    listbox.bind("<<ListboxSelect>>", seleccionar_socio)

# Función para mostrar y agregar socios
def mostrar_agregar_socios():
    clear_content_frame()

    label = tk.Label(
        content_frame, text="Agregar Socio", font=("Arial", 24), bg="white"
    )
    label.pack(pady=20)

    campos = [
        "Nombre",
        "Apellido",
        "Fecha de Nacimiento\n(aaaa-mm-dd)",
        "Dirección",
        "Correo Electrónico",
        "Teléfono",
    ]
    entradas = {}

    for campo in campos:
        tk.Label(content_frame, text=campo, font=("Arial", 16), bg="white").pack(pady=5)
        entry = tk.Entry(content_frame, font=("Arial", 16))
        entry.pack(pady=5)
        entradas[campo] = entry

    result_label = tk.Label(content_frame, text="", font=("Arial", 12), bg="white")
    result_label.pack(pady=10)

    def guardar_socio():
        nuevo_socio = {
            "nombre": entradas["Nombre"].get(),
            "apellido": entradas["Apellido"].get(),
            "fecha_nacimiento": entradas["Fecha de Nacimiento\n(aaaa-mm-dd)"].get(),
            "direccion": entradas["Dirección"].get(),
            "correo_electronico": entradas["Correo Electrónico"].get(),
            "telefono": entradas["Teléfono"].get(),
        }
        agregar_socio(nuevo_socio)
        result_label.config(text="Socio agregado exitosamente", fg="green")
        for entry in entradas.values():
            entry.delete(0, tk.END)

    tk.Button(
        content_frame, text="Guardar Socio", font=("Arial", 16), command=guardar_socio
    ).pack(pady=10)

# Función para editar socios
def mostrar_editar_socios():
    clear_content_frame()

    # Cargar los datos de socios desde el archivo JSON
    datos_socios = cargar_datos_socios()

    label = tk.Label(content_frame, text="Editar Socio", font=("Arial", 24), bg="white")
    label.pack(pady=20)

    listbox_frame = tk.Frame(content_frame)
    listbox_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=False)
    listbox = tk.Listbox(
        listbox_frame, font=("Arial", 18), height=7, bg="green", fg="white"
    )
    listbox.pack(fill=tk.BOTH, expand=True)

    # Función para actualizar la lista de socios en el Listbox
    def actualizar_lista_socios():
        listbox.delete(0, tk.END)  # Limpiar la lista antes de actualizar
        for socio in datos_socios:
            listbox.insert(
                tk.END, f"{socio['nombre']} {socio['apellido']}"
            )  # Mostrar nombre y apellido del socio

    # Actualizar la lista de socios al inicio
    actualizar_lista_socios()

    # Frame para los campos de edición
    edit_frame = tk.Frame(content_frame, bg="white")
    edit_frame.pack(pady=20)

    # Función para mostrar campos de edición al seleccionar un socio
    def seleccionar_socio(event):
        indice_seleccionado = listbox.curselection()
        if indice_seleccionado:
            indice = indice_seleccionado[0]
            socio_seleccionado = datos_socios[indice]

            # Limpiar el frame de edición antes de agregar nuevos widgets
            for widget in edit_frame.winfo_children():
                widget.destroy()

            # Campos de entrada para editar los atributos del socio
            campos = ["Dirección", "Correo Electrónico", "Teléfono"]
            entradas = {}

            for campo in campos:
                tk.Label(edit_frame, text=campo, font=("Arial", 18), bg="white").pack(
                    pady=5
                )
                entry = tk.Entry(edit_frame, font=("Arial", 18))
                clave = campo.lower().replace(" ", "_")
                if clave in socio_seleccionado:
                    entry.insert(0, socio_seleccionado[clave])
                entry.pack(pady=5)
                entradas[clave] = entry

            # Función para guardar los cambios del socio seleccionado
            def guardar_cambios():
                try:
                    for campo in campos:
                        clave = campo.lower().replace(" ", "_")
                        socio_seleccionado[clave] = entradas[clave].get()

                    # Guardar los cambios en el archivo JSON
                    guardar_datos_socios(datos_socios)

                    messagebox.showinfo(
                        "Éxito", "Los cambios han sido guardados correctamente."
                    )
                    actualizar_lista_socios()  # Actualizar la lista después de guardar cambios
                except Exception as e:
                    messagebox.showerror(
                        "Error", f"No se pudo guardar los cambios. Error: {str(e)}"
                    )

            button_guardar = tk.Button(
                edit_frame,
                text="Guardar Cambios",
                font=("Arial", 18),
                command=guardar_cambios,
            )
            button_guardar.pack(pady=10)

    listbox.bind("<<ListboxSelect>>", seleccionar_socio)

# Función para eliminar socios
def mostrar_eliminar_socios():
    clear_content_frame()

    # Cargar los datos de socios desde el archivo JSON
    datos_socios = cargar_datos_socios()

    label = tk.Label(
        content_frame, text="Eliminar Socio", font=("Arial", 24), bg="white"
    )
    label.pack(pady=20)

    listbox_frame = tk.Frame(content_frame)
    listbox_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=False)
    listbox = tk.Listbox(
        listbox_frame, font=("Arial", 18), height=12, bg="green", fg="white"
    )
    listbox.pack(fill=tk.BOTH, expand=True)

    # Función para actualizar la lista de socios en el Listbox
    def actualizar_lista_socios():
        listbox.delete(0, tk.END)  # Limpiar la lista antes de actualizar
        for socio in datos_socios:
            listbox.insert(
                tk.END, f"{socio['nombre']} {socio['apellido']}"
            )  # Mostrar nombre y apellido del socio

    # Actualizar la lista de socios al inicio
    actualizar_lista_socios()

    # Función para eliminar un socio seleccionado
    def eliminar_socio():
        seleccionados = listbox.curselection()
        if not seleccionados:
            messagebox.showwarning(
                "Advertencia", "Por favor, seleccione un socio para eliminar."
            )
            return
        indice = seleccionados[0]
        socio_seleccionado = datos_socios[indice]
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar al socio '{socio_seleccionado['nombre']} {socio_seleccionado['apellido']}'?",
        )
        if confirmacion:
            datos_socios.pop(indice)
            guardar_datos_socios(datos_socios)
            actualizar_lista_socios()
            messagebox.showinfo("Éxito", "El socio ha sido eliminado correctamente.")

    button_eliminar = tk.Button(
        content_frame, text="Eliminar", font=("Arial", 18), command=eliminar_socio
    )
    button_eliminar.pack(pady=10)



# Función para mostrar la pestaña de Préstamos de libro
def mostrar_prestamos():
    clear_content_frame()
    label = tk.Label(content_frame, text="Lista de Préstamos", font=("Arial", 24), bg="white")
    label.pack(pady=20)
        
    # Cargar datos de préstamos, socios y libros
    datos_prestamos = cargar_datos_prestamos()
    datos_socios = cargar_datos_socios()
    datos_libros = cargar_datos_libros()    
        
    # Crear el Treeview con columnas para ID de socio y ID de libro
    tree = ttk.Treeview(content_frame, columns=( "ID Préstamo","ID Socio","Nombre Socio","ID Libro","Nombre Libro","Fecha Préstamo","Fecha Devolución", "Estado"), show="headings")
    tree.pack(pady=10, padx=10, fill=tk.X, expand=True)
   
    # Definir encabezados
    tree.heading("ID Préstamo", text="ID Préstamo", anchor=tk.CENTER)
    tree.heading("ID Socio", text="ID Socio", anchor=tk.CENTER)
    tree.heading("Nombre Socio", text="Nombre Socio", anchor=tk.CENTER)
    tree.heading("ID Libro", text="ID Libro", anchor=tk.CENTER)
    tree.heading("Nombre Libro", text="Nombre Libro", anchor=tk.CENTER)
    tree.heading("Fecha Préstamo", text="Fecha Préstamo", anchor=tk.CENTER)
    tree.heading("Fecha Devolución", text="Fecha Devolución", anchor=tk.CENTER)
    tree.heading("Estado", text="Estado", anchor=tk.CENTER)
    
    # Ajustar el ancho de las columnas
    tree.column("ID Préstamo", width=80, anchor=tk.CENTER)
    tree.column("ID Socio", width=80, anchor=tk.CENTER)
    tree.column("Nombre Socio", width=150, anchor=tk.CENTER)
    tree.column("ID Libro", width=80, anchor=tk.CENTER)
    tree.column("Nombre Libro", width=200, anchor=tk.CENTER)
    tree.column("Fecha Préstamo", width=120, anchor=tk.CENTER)
    tree.column("Fecha Devolución", width=120, anchor=tk.CENTER)
    tree.column("Estado", width=100, anchor=tk.CENTER)
    
    # Insertar datos en el Treeview
    for prestamo in datos_prestamos:
        # Buscar el nombre del socio por su ID Socio
        nombre_socio = ""
        for socio in datos_socios:
            if socio["id_socio"] == prestamo["id_socio"]:
                nombre_socio = f"{socio['nombre']} {socio['apellido']}"
                break
        # Buscar el nombre del libro por su ID Libro
        nombre_libro = ""
        for libro in datos_libros:
            if libro["id_libro"] == prestamo["id_libro"]:
                nombre_libro = libro["titulo"]
                break
        # Insertar fila en el Treeview
        tree.insert(
            "",
            "end",
            values=(
                prestamo["id_prestamo"],
                prestamo["id_socio"],
                nombre_socio,
                prestamo["id_libro"],
                nombre_libro,
                prestamo["fecha_prestamo"],
                prestamo.get("fecha_devolucion", "N/A"),
                prestamo["estado_prestamo"],
            ),
        )

    
    
    # Configurar el número máximo de filas visibles
    num_filas_visibles = 15  # Reducido para dejar espacio suficiente
    alto_maximo = num_filas_visibles * 25  # Aproximadamente 25 pixeles por fila
    tree.config(height=num_filas_visibles)
     
    # Función para guardar la nueva fecha de devolución
    def guardar_fecha():
        seleccionados = tree.selection()
        if not seleccionados:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un préstamo para editar.")
            return
        # Obtener el item seleccionado y el índice
        item = tree.focus()
        indice = int(tree.index(item))
        prestamo_seleccionado = datos_prestamos[indice]
        nueva_fecha = cal.get_date().strftime("%Y-%m-%d")
        prestamo_seleccionado["fecha_devolucion"] = nueva_fecha
        guardar_datos_prestamos(datos_prestamos)
        mostrar_prestamos()
        messagebox.showinfo("Éxito", f"La fecha de devolución del préstamo '{prestamo_seleccionado['id_prestamo']}' ha sido actualizada correctamente.")
    # Crear DateEntry para seleccionar la nueva fecha de devolución
    cal = DateEntry(content_frame, width=22, background='green',
                    foreground='white', borderwidth=3,
                    year=int(datetime.now().strftime('%Y')),
                    month=int(datetime.now().strftime('%m')),
                    day=int(datetime.now().strftime('%d')),
                    date_pattern='yyyy-mm-dd',font=("Arial", 13))
    cal.pack(pady=10)

    label = tk.Label(content_frame, text="Ampliar plazo de entrega para fecha de devolución", font=("Arial", 10), bg="white")
    label.pack(pady=0)
    
    # Botón para guardar los cambios
    tk.Button(content_frame, text="Guardar Cambios", font=("Arial", 18), command=guardar_fecha).pack(pady=90)

# Función para crear un nuevo préstamo con datos ingresados manualmente
def crear_prestamo():
    clear_content_frame()

    datos_socios = cargar_datos_socios()
    datos_libros = cargar_datos_libros()
    datos_prestamos = cargar_datos_prestamos()

    label = tk.Label(
        content_frame, text="Crear Préstamo", font=("Arial", 24), bg="white"
    )
    label.pack(pady=20)

    # Obtener nombres de socios y títulos de libros para las listas desplegables
    nombres_socios = [f"{socio['nombre']} {socio['apellido']}" for socio in datos_socios]
    titulos_libros = [libro['titulo'] for libro in datos_libros]

    # Widget para seleccionar socio
    id_socio_label = tk.Label(
        content_frame, text="Nombre del Socio", font=("Arial", 18), bg="white"
    )
    id_socio_label.pack(pady=5)
    socio_combo = ttk.Combobox(content_frame, values=nombres_socios, font=("Arial", 18), state="readonly")
    socio_combo.pack(pady=5)

    # Widget para seleccionar libro
    id_libro_label = tk.Label(
        content_frame, text="Título del Libro", font=("Arial", 18), bg="white"
    )
    id_libro_label.pack(pady=5)
    libro_combo = ttk.Combobox(content_frame, values=titulos_libros, font=("Arial", 18), state="readonly")
    libro_combo.pack(pady=5)

    fecha_prestamo_label = tk.Label(
        content_frame, text="Fecha de Préstamo", font=("Arial", 18), bg="white"
    )
    fecha_prestamo_label.pack(pady=5)
    fecha_prestamo_entry = DateEntry(
        content_frame,
        selecMode="day",
        year=2024,
        month=7,
        day=10,
        font=("Arial", 13), width=22, background='green', 
    )
    fecha_prestamo_entry.pack(pady=5)

    fecha_devolucion_label = tk.Label(
        content_frame, text="Fecha de Devolución", font=("Arial", 18), bg="white"
    )
    fecha_devolucion_label.pack(pady=5)
    fecha_devolucion_entry = DateEntry(content_frame, selecMode="day", year=2024, month=7, day=20, font=("Arial", 13), width=22, background='green',)
    fecha_devolucion_entry.pack(pady=5)

    result_label = tk.Label(content_frame, font=("Arial", 18), bg="white")
    result_label.pack(pady=10)

    def guardar_prestamo():
        try:
            # Obtener el nombre del socio seleccionado
            nombre_socio_seleccionado = socio_combo.get()
            if not nombre_socio_seleccionado:
                messagebox.showwarning("Advertencia", "Seleccione un socio.")
                return
            id_socio = next((socio['id_socio'] for socio in datos_socios if f"{socio['nombre']} {socio['apellido']}" == nombre_socio_seleccionado), None)

            # Obtener el título del libro seleccionado
            titulo_libro_seleccionado = libro_combo.get()
            if not titulo_libro_seleccionado:
                messagebox.showwarning("Advertencia", "Seleccione un libro.")
                return
            id_libro = next((libro['id_libro'] for libro in datos_libros if libro['titulo'] == titulo_libro_seleccionado), None)

            nuevo_prestamo = {
                "id_prestamo": (
                    max(p["id_prestamo"] for p in datos_prestamos) + 1
                    if datos_prestamos
                    else 1
                ),
                "id_libro": id_libro,
                "id_socio": id_socio,
                "fecha_prestamo": fecha_prestamo_entry.get_date().strftime("%Y-%m-%d"),
                "fecha_devolucion": fecha_devolucion_entry.get_date().strftime("%Y-%m-%d"),
                "estado_prestamo": "En Curso",
            }

            datos_prestamos.append(nuevo_prestamo)
            guardar_datos_prestamos(datos_prestamos)
            result_label.config(text="Préstamo guardado exitosamente", fg="green")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el préstamo. Error: {str(e)}")

    button = tk.Button(
        content_frame,
        text="Guardar Préstamo",
        font=("Arial", 18),
        command=guardar_prestamo,
    )
    button.pack(pady=10)

    print("editar préstamo")

# Función para manejar la eliminación de un préstamo
def mostrar_eliminar_prestamos():
    clear_content_frame()
    # Cargar los datos de préstamos desde el archivo JSON
    datos_prestamos = cargar_datos_prestamos()
    label = tk.Label(
        content_frame, text="Eliminar Préstamo", font=("Arial", 24), bg="white"
    )
    label.pack(pady=20)
    listbox = tk.Listbox(
        content_frame, font=("Arial", 18), height=12, bg="green", fg="white"
    )
    listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def actualizar_lista_prestamos():
        listbox.delete(0, tk.END)
        for prestamo in datos_prestamos:
            socio = buscar_socio_por_id(prestamo['id_socio'])
            libro = buscar_libro_por_id(prestamo['id_libro'])
            if socio and libro:
                listbox.insert(tk.END, f"Préstamo ID: {prestamo['id_prestamo']} - Socio: {socio['nombre']} {socio['apellido']} - Libro: {libro['titulo']}",)

    actualizar_lista_prestamos()

    def eliminar_prestamo():
        seleccionados = listbox.curselection()
        if not seleccionados:
            messagebox.showwarning(
                "Advertencia", "Por favor, seleccione un préstamo para eliminar."
            )
            return
        indice = seleccionados[0]
        prestamo_a_eliminar = datos_prestamos.pop(indice)
        guardar_datos_prestamos(datos_prestamos)
        actualizar_lista_prestamos()
        messagebox.showinfo(
            "Éxito",
            f"El préstamo '{prestamo_a_eliminar['id_prestamo']}' ha sido eliminado correctamente.",
        )

    button_eliminar = tk.Button(
        content_frame,
        text="Eliminar Préstamo",
        font=("Arial", 18),
        command=eliminar_prestamo,
    )
    button_eliminar.pack(pady=10)



# Función para generar reporte por socio
def generar_reporte_socio(nombre_completo):
    datos_socios = cargar_datos_socios()
    datos_libros = cargar_datos_libros()
    datos_prestamos = cargar_datos_prestamos()

    socio = next((s for s in datos_socios if f"{s['nombre']} {s['apellido']}" == nombre_completo), None)
    if not socio:
        messagebox.showerror("Error", "Seleccione un socio válido.")
        return

    id_socio = socio['id_socio']
    prestamos_filtrados = [p for p in datos_prestamos if p['id_socio'] == id_socio]

    generar_reporte(prestamos_filtrados, f"Reporte por Socio - {nombre_completo}")

# Función para generar reporte por libro
def generar_reporte_libro(titulo_libro):
    datos_libros = cargar_datos_libros()
    datos_prestamos = cargar_datos_prestamos()

    if titulo_libro == "Todos los Libros":
        prestamos_filtrados = datos_prestamos
    else:
        libro = next((l for l in datos_libros if l['titulo'] == titulo_libro), None)
        if not libro:
            messagebox.showerror("Error", "Seleccione un libro válido.")
            return
        id_libro = libro['id_libro']
        prestamos_filtrados = [p for p in datos_prestamos if p['id_libro'] == id_libro]

    generar_reporte(prestamos_filtrados, f"Reporte por Libro - {titulo_libro}")

# Función para generar reporte por rango de fechas
def generar_reporte_fechas(fecha_inicio, fecha_fin):
    datos_prestamos = cargar_datos_prestamos()

    try:
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    except ValueError:
        messagebox.showerror("Error", "Formato de fecha incorrecto. Use el formato YYYY-MM-DD.")
        return

    prestamos_filtrados = [p for p in datos_prestamos if fecha_inicio <= datetime.strptime(p['fecha_prestamo'], "%Y-%m-%d").date() <= fecha_fin]

    generar_reporte(prestamos_filtrados, f"Reporte por Rango de Fechas - {fecha_inicio} al {fecha_fin}")




# Función para generar el reporte en PDF
def generar_reporte(prestamos, titulo):
    datos_socios = cargar_datos_socios()
    datos_libros = cargar_datos_libros()

    pdf_filename = "reporte.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    c.drawString(100, 750, titulo)

    y = 720
    line_height = 15

    for prestamo in prestamos:
        socio = next((s for s in datos_socios if s['id_socio'] == prestamo['id_socio']), {})
        libro = next((l for l in datos_libros if l['id_libro'] == prestamo['id_libro']), {})
        texto = f"Socio: {socio.get('nombre', 'N/A')} {socio.get('apellido', 'N/A')} - Libro: {libro.get('titulo', 'N/A')} - Fecha Préstamo: {prestamo['fecha_prestamo']} - Fecha Devolución: {prestamo.get('fecha_devolucion', 'N/A')}"
        c.drawString(100, y, texto)
        y -= line_height

        if y < 100:
            c.showPage()
            c.drawString(100, 750, titulo)
            y = 720

    c.save()
    messagebox.showinfo("Reporte Generado", f"El reporte ha sido generado como {pdf_filename}")

# Función para generar un reporte
def crear_reporte():
    clear_content_frame()

    tk.Label(content_frame, text="Generar Reporte", font=("Arial", 24), bg="white").pack(pady=20)

    criterio = tk.StringVar(value="socio")

    # Radio buttons para seleccionar el criterio de reporte
    tk.Radiobutton(content_frame, text="Por Socio", variable=criterio, value="socio", font=("Arial", 14), bg="white").pack(pady=5)
    tk.Radiobutton(content_frame, text="Por Libro", variable=criterio, value="libro", font=("Arial", 14), bg="white").pack(pady=5)
    tk.Radiobutton(content_frame, text="Por Rango de Fechas", variable=criterio, value="fecha", font=("Arial", 14), bg="white").pack(pady=5)

    # Campos de fechas y comboboxes
    fecha_inicio_label = tk.Label(content_frame, text="Fecha Inicio:", font=("Arial", 18), bg="white")
    fecha_inicio_entry = DateEntry(content_frame, selecMode="day", font=("Helvetica", 17))
    fecha_fin_label = tk.Label(content_frame, text="Fecha Fin:", font=("Arial", 18), bg="white")
    fecha_fin_entry = DateEntry(content_frame, selecMode="day", font=("Helvetica", 17))

    datos_socios = cargar_datos_socios()
    nombres_socios = ["Todos los Socios"] + [f"{socio['nombre']} {socio['apellido']}" for socio in datos_socios]
    socio_combobox = ttk.Combobox(content_frame, values=nombres_socios, font=("Helvetica", 17))

    datos_libros = cargar_datos_libros()
    titulos_libros = ["Todos los Libros"] + [libro['titulo'] for libro in datos_libros]
    libro_combobox = ttk.Combobox(content_frame, values=titulos_libros, font=("Helvetica", 17))

    # Función para mostrar los campos según el criterio seleccionado
    def mostrar_campos_criterio():
        # Limpiar todos los widgets antes de mostrar los correspondientes al criterio
        fecha_inicio_label.pack_forget()
        fecha_inicio_entry.pack_forget()
        fecha_fin_label.pack_forget()
        fecha_fin_entry.pack_forget()
        socio_combobox.pack_forget()
        libro_combobox.pack_forget()
        btn_generar_pdf.pack_forget()  # Ocultar el botón antes de mostrarlo nuevamente

        if criterio.get() == "fecha":
            fecha_inicio_label.pack(pady=5)
            fecha_inicio_entry.pack(pady=5)
            fecha_fin_label.pack(pady=5)
            fecha_fin_entry.pack(pady=5)
            btn_generar_pdf.pack(pady=10)  # Mostrar el botón después de los campos de fecha
        elif criterio.get() == "socio":
            socio_combobox.pack(pady=5)
            btn_generar_pdf.pack(pady=10)  # Mostrar el botón después del combobox de socio
        elif criterio.get() == "libro":
            libro_combobox.pack(pady=5)
            btn_generar_pdf.pack(pady=10)  # Mostrar el botón después del combobox de libro

    criterio.trace('w', lambda *args: mostrar_campos_criterio())

    # Botón para generar el PDF
    btn_generar_pdf = tk.Button(content_frame, text="Generar PDF", font=("Arial", 18), command=lambda: generar_pdf(criterio.get(), socio_combobox.get(), libro_combobox.get(), fecha_inicio_entry.get_date(), fecha_fin_entry.get_date()))

    # Mostrar inicialmente los campos según el criterio seleccionado
    mostrar_campos_criterio()

# Función para generar el reporte en PDF
def generar_pdf(criterio, nombre_completo=None, titulo_libro=None, fecha_inicio=None, fecha_fin=None):
    datos_socios = cargar_datos_socios()
    datos_libros = cargar_datos_libros()
    datos_prestamos = cargar_datos_prestamos()

    prestamos_filtrados = []

    if criterio == "socio":
        if nombre_completo == "Todos los Socios":
            prestamos_filtrados = datos_prestamos
        else:
            socio = next((s for s in datos_socios if f"{s['nombre']} {s['apellido']}" == nombre_completo), None)
            if socio:
                id_socio = socio['id_socio']
                prestamos_filtrados = [p for p in datos_prestamos if p['id_socio'] == id_socio]
            else:
                messagebox.showerror("Error", "Seleccione un socio válido.")
                return
        titulo_reporte = f"Reporte en PDF por socio: {nombre_completo}"
    elif criterio == "libro":
        if titulo_libro == "Todos los Libros":
            prestamos_filtrados = datos_prestamos
        else:
            libro = next((l for l in datos_libros if l['titulo'] == titulo_libro), None)
            if libro:
                id_libro = libro['id_libro']
                prestamos_filtrados = [p for p in datos_prestamos if p['id_libro'] == id_libro]
            else:
                messagebox.showerror("Error", "Seleccione un libro válido.")
                return
        titulo_reporte = f"Reporte en PDF por libro: {titulo_libro}"
    elif criterio == "fecha":
        prestamos_filtrados = [p for p in datos_prestamos if fecha_inicio <= datetime.strptime(p['fecha_prestamo'], "%Y-%m-%d").date() <= fecha_fin]
        titulo_reporte = f"Reporte en PDF por rango de fechas: {fecha_inicio} - {fecha_fin}"

    if not prestamos_filtrados:
        messagebox.showinfo("Sin datos", "No se encontraron préstamos con los criterios seleccionados.")
        return

    # Generar un nombre único para el archivo PDF usando la fecha y hora actual
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"reporte_{timestamp}.pdf"

    c = canvas.Canvas(pdf_filename, pagesize=landscape(letter))

    left_margin = 50
    top_margin = 550
    line_height = 15

    # Título centralizado del reporte
    c.setFont("Helvetica-Bold", 16)
    text_width = c.stringWidth(titulo_reporte, "Helvetica-Bold", 16)
    c.drawString((letter[1] - text_width) / 2, top_margin + 20, titulo_reporte)

    # Línea horizontal bajo el título
    c.line(left_margin, top_margin + 10, letter[1] - left_margin, top_margin + 10)

    # Encabezados de columna
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_margin, top_margin, "Socio")
    c.drawString(left_margin + 150, top_margin, "Libro")
    c.drawString(left_margin + 350, top_margin, "Fecha Préstamo")
    c.drawString(left_margin + 500, top_margin, "Fecha Devolución")

    y = top_margin - 20

    for prestamo in prestamos_filtrados:
        socio = next((s for s in datos_socios if s['id_socio'] == prestamo['id_socio']), {})
        libro = next((l for l in datos_libros if l['id_libro'] == prestamo['id_libro']), {})
        
        # Datos de cada préstamo
        texto_socio = f"{socio.get('nombre', 'N/A')} {socio.get('apellido', 'N/A')}"
        texto_libro = libro.get('titulo', 'N/A')
        texto_fecha_prestamo = prestamo['fecha_prestamo']
        texto_fecha_devolucion = prestamo.get('fecha_devolucion', 'N/A')

        # Dibujar los datos en el PDF
        c.setFont("Helvetica", 12)
        c.drawString(left_margin, y, texto_socio)
        c.drawString(left_margin + 150, y, texto_libro)
        c.drawString(left_margin + 350, y, texto_fecha_prestamo)
        c.drawString(left_margin + 500, y, texto_fecha_devolucion)
        
        y -= line_height

        if y < 100:
            c.showPage()
            # Volver a dibujar el encabezado en una nueva página
            c.setFont("Helvetica-Bold", 16)
            c.drawString((letter[1] - text_width) / 2, top_margin + 20, titulo_reporte)
            c.line(left_margin, top_margin + 10, letter[1] - left_margin, top_margin + 10)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(left_margin, top_margin, "Socio")
            c.drawString(left_margin + 150, top_margin, "Libro")
            c.drawString(left_margin + 350, top_margin, "Fecha Préstamo")
            c.drawString(left_margin + 500, top_margin, "Fecha Devolución")
            y = top_margin - 20

    c.save()
    messagebox.showinfo("Reporte Generado", f"El reporte ha sido generado como {pdf_filename}")




# Función para limpiar el contenido del frame
def clear_content_frame():
    for widget in content_frame.winfo_children():
        widget.destroy()

# Configuración de la interfaz gráfica
ventanaPrincipal = tk.Tk()
ventanaPrincipal.title("Administración de biblioteca Viva La Libertad")

# Configuración del icono de la ventana
# Construir la ruta a la imagen (en este caso, relativa a 'main.py')
file_pathIco = os.path.join(os.path.dirname(__file__), 'img', 'ico.png')
icono = PhotoImage(file=file_pathIco)# Tamaño recomendado 32x32 píxeles
ventanaPrincipal.iconphoto(True, icono)

# Configuración del tamaño de la ventana
ancho_pantalla = ventanaPrincipal.winfo_screenwidth()
alto_pantalla = ventanaPrincipal.winfo_screenheight()

# Configurar el tamaño de la ventana para que ocupe todo el ancho y alto de la pantalla
ventanaPrincipal.geometry(f"{ancho_pantalla}x{alto_pantalla}")
ventanaPrincipal.configure(bg="#177245")

# Definir el ancho del menú (20% de la pantalla)
menu_width = int(ancho_pantalla * 0.2)
content_width = int(ancho_pantalla * 0.8)

# Configurar el menú (20% de la pantalla) con fondo negro
menu_frame = tk.Frame(ventanaPrincipal, width=menu_width, height=alto_pantalla, bg="black")
menu_frame.pack(side="left", fill="y")

# Etiqueta para la barra superior (mostrará frases aleatorias)
top_bar = tk.Label(ventanaPrincipal, text="", bg="black", fg="white", height=2, anchor="w", font=("PT Sans", 10),)
top_bar.pack(fill=tk.X)

# Opciones del menú
opcion0_button = tk.Button(menu_frame, text="Búsqueda de Libros", command=mostrar_busqueda_libros, bg="#228B22", fg="white", font=("Arial", 11), width=10,)
opcion0_button.pack(pady=(130, 10), fill="x")

opcion1_button = tk.Button(menu_frame, text="Registrar Libro", command=mostrar_registro_libros, bg="#228B22", fg="white", font=("Arial", 11),)
opcion1_button.pack(pady=10, fill="x")

opcion2_button = tk.Button(menu_frame, text="Modificar un libro", command=mostrar_modificar_libros, bg="#228B22", fg="white", font=("Arial", 11),)
opcion2_button.pack(pady=10, fill="x")

opcion3_button = tk.Button(menu_frame, text="Eliminar un libro", command=mostrar_eliminar_libros, bg="#228B22", fg="white", font=("Arial", 11),)
opcion3_button.pack(pady=10, fill="x")

opcion4_button = tk.Button(menu_frame, text="Buscar Socio", command=mostrar_buscar_socios, bg="#228B22", fg="white", font=("Arial", 11),)
opcion4_button.pack(pady=10, fill="x")

opcion5_button = tk.Button(menu_frame, text="Agregar Socio", command=mostrar_agregar_socios, bg="#228B22", fg="white", font=("Arial", 11),)
opcion5_button.pack(pady=10, fill="x")

opcion6_button = tk.Button(menu_frame, text="Editar Socio", command=mostrar_editar_socios, bg="#228B22", fg="white", font=("Arial", 11),)
opcion6_button.pack(pady=10, fill="x")

opcion7_button = tk.Button( menu_frame, text="Eliminar Socio", command=mostrar_eliminar_socios, bg="#228B22", fg="white", font=("Arial", 11),)
opcion7_button.pack(pady=10, fill="x")

opcion8_button = tk.Button(menu_frame, text="Ver/Editar Préstamos", command=mostrar_prestamos, bg="#228B22", fg="white", font=("Arial", 11), )
opcion8_button.pack(pady=10, fill="x")

opcion9_button = tk.Button(menu_frame, text="Crear un préstamo", command=crear_prestamo, bg="#228B22", fg="white", font=("Arial", 11),)
opcion9_button.pack(pady=10, fill="x")

opcion10_button = tk.Button(menu_frame, text="Eliminar un préstamo", command=mostrar_eliminar_prestamos, bg="#228B22", fg="white", font=("Arial", 11),)
opcion10_button.pack(pady=10, fill="x")

opcion11_button = tk.Button(menu_frame, text="Generar Reporte", command=crear_reporte, bg="#228B22", fg="white", font=("Arial", 11))
opcion11_button.pack(pady=10, fill="x")


# Área de contenido (80% de la pantalla) con fondo blanco
content_frame = tk.Frame(
    ventanaPrincipal, width=content_width, height=alto_pantalla, bg="white"
)
content_frame.pack(side="right", fill="both", expand=True)

# Reloj en la barra superior (para que no se borre al cambiar de contenido)
label_reloj = tk.Label(top_bar, font=("Arial", 24), bg="black", fg="white")
label_reloj.pack(side="right", padx=(0, 5))
actualizar_reloj()

# Función para cargar frases aleatorias desde el archivo JSON
frases = cargar_frases()

# Mostrar una frase aleatoria inicial
mostrar_frase_aleatoria()

# Cargar la imagen del logo
# Construir la ruta a la imagen (en este caso, relativa a 'main.py')
file_pathLogo = os.path.join(os.path.dirname(__file__), 'img', 'logo.png')
imagen = PhotoImage(file=file_pathLogo)
label_imagen = tk.Label(content_frame, image=imagen, width=410, bg="white")
label_imagen.pack(pady=(225, 0))

# Cargar los datos iniciales de los libros
datos_libros = cargar_datos_libros()
datos_socios = cargar_datos_socios()

# Iniciar el bucle principal de la aplicación
ventanaPrincipal.mainloop()