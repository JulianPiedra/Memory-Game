import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
mensaje_ventana=None
# Crear una baraja de cartas (puede inicializarse vacía y se llenará según la elección del jugador)
baraja = []
# Lista para llevar un registro de las cartas acertadas
cartas_acertadas = []
puntos = {}  # Usar un diccionario para almacenar los puntos de cada jugador
turno = 1  # Inicializar el turno en 1

# Crear el tablero (inicialmente vacío)
tablero = []

# Variables globales para contar cartas volteadas y cartas seleccionadas
cartas_volteadas = 0
cartas_seleccionadas = []

# Función para iniciar el juego con la configuración seleccionada
def iniciar_juego():
    global baraja, tablero, cartas_volteadas, cartas_seleccionadas, puntos, turno
    if not entrada_jugadores.get():
        messagebox.showerror("Error", "The number of players is required.")
        return
    if not entrada_jugadores.get().isdigit():
        messagebox.showerror("Error", "The number of players must be an number.")
        return
    # Reiniciar puntos y turno
    puntos = {}
    turno = 1

    # Reiniciar cartas seleccionadas y volteadas
    cartas_volteadas = 0
    cartas_seleccionadas = []

    # Cambiar la lista de imágenes según la temática seleccionada
    if var_tematica.get() == 1:
        # Frutas
        baraja = [f"assets/fruta{i}.png" for i in range(1, 11)]
    elif var_tematica.get() == 2:
        # Deportes
        baraja = [f"assets/deporte{i}.png" for i in range(1, 11)]
    elif var_tematica.get() == 3:
        # Videojuegos
        baraja = [f"assets/videojuego{i}.png" for i in range(1, 11)]
    
    if var_juego.get() == 3:
        # Si el jugador eligió tríos, agregar tres copias de cada carta a la baraja
        cartas_unicas = list(set(baraja))
        baraja = cartas_unicas * 3
    else:
        # Si el jugador eligió parejas, duplicar las cartas para crear pares
        baraja *= 2

    # Mezclar las cartas
    random.shuffle(baraja)

    # Ocultar el menú principal
    menu_frame.grid_forget()

    # Mostrar el tablero de juego
    mostrar_tablero()

# Función para mostrar el tablero de juego
def mostrar_tablero():
    global baraja, tablero, botones
    # Ocultar la ventana de opciones
    menu_frame.grid_forget()
    ventana.resizable(False, False)
    # Mostrar el tablero de juego
    ventana.deiconify() 
    # Determinar el tamaño del tablero según la elección del jugador
    filas = 6 if var_juego.get() == 3 else 4
    columnas = 5 if var_juego.get() == 3 else 5
    tablero = [[' ' for _ in range(columnas)] for _ in range(filas)]

    # Crear un Label para mostrar el contador de puntos y el turno
    puntos_label.config(text=f"Player #{turno} turn - Points: {puntos.get(turno, 0)}")

    # Crear los botones del tablero
    botones = []
    for fila in range(filas):
        fila_botones = []
        for columna in range(columnas):
            boton = tk.Button(ventana, image=back_image, command=lambda fila=fila, columna=columna: manejar_clic(fila, columna))
            boton.grid(row=fila + 1, column=columna)
            fila_botones.append(boton)
        botones.append(fila_botones)

    # Mostrar la ventana principal
    ventana.mainloop()

# Función para seleccionar una carta
def seleccionar_carta(fila, columna):
    return baraja[fila * 5 + columna]

# Función para voltear una carta
def voltear_carta(fila, columna):
    if tablero[fila][columna] == ' ':
        tablero[fila][columna] = seleccionar_carta(fila, columna)
        mostrar_carta(fila, columna)

# Función para ocultar una carta
def ocultar_carta(fila, columna):
    if tablero[fila][columna] != ' ':
        tablero[fila][columna] = ' '
        botones[fila][columna].config(image=back_image)

# Función para mostrar una carta
def mostrar_carta(fila, columna):
    if tablero[fila][columna] != ' ':
        img = Image.open(tablero[fila][columna])
        img.thumbnail((100, 100))
        img = ImageTk.PhotoImage(img)
        botones[fila][columna].config(image=img)
        botones[fila][columna].image = img

# Función para verificar si las cartas son iguales
def cartas_iguales(fila1, columna1, fila2, columna2):
    carta1 = seleccionar_carta(fila1, columna1)
    carta2 = seleccionar_carta(fila2, columna2)
    return carta1 == carta2

# Función para contar las cartas de cada jugador
def contar_cartas():
    contador = {}
    for fila in tablero:
        for carta in fila:
            if carta != ' ':
                if carta in contador:
                    contador[carta] += 1
                else:
                    contador[carta] = 1
    return contador

# Función para determinar al ganador
def actualizar_puntos():
    global puntos, turno
    puntos[turno] = puntos.get(turno, 0) + 1
    puntos_label.config(text=f"Player #{turno} turn - Points: {puntos.get(turno, 0)}")
# Función para manejar el clic en un botón
def verificar_cartas():
    global cartas_volteadas, cartas_seleccionadas, cartas_acertadas, turno

    if all(cartas_iguales(*carta1, *carta2) for carta1, carta2 in zip(cartas_seleccionadas[:-1], cartas_seleccionadas[1:])):
        actualizar_puntos()
        for fila, columna in cartas_seleccionadas:
            # Agregar cartas acertadas al registro
            cartas_acertadas.append((fila, columna))

        if len(cartas_acertadas) == len(baraja):
            ganador = max(puntos, key=puntos.get)  # Obtener el jugador con más puntos
            mostrar_mensaje_ganador(ganador, puntos[ganador])
            ventana.update()
        else:
            # No todas las cartas han sido acertadas, el jugador actual sigue jugando
            # No cambies de turno automáticamente
            cartas_volteadas = 0
            cartas_seleccionadas = []
    else:
        for fila, columna in cartas_seleccionadas:
            # Ocultar cartas solo si no están en el registro de cartas acertadas
            if (fila, columna) not in cartas_acertadas:
                ocultar_carta(fila, columna)

        # Limpiar las cartas seleccionadas
        cartas_volteadas = 0
        cartas_seleccionadas = []
        
        # Cambiar el turno al siguiente jugador
        turno = (turno % int(entrada_jugadores.get())) + 1
        puntos_label.config(text=f"Player #{turno} turn - Points: {puntos.get(turno, 0)}")


# Función para manejar el clic en un botón
def manejar_clic(fila, columna):
    global cartas_volteadas, cartas_seleccionadas, cartas_acertadas, turno

    if cartas_volteadas < var_juego.get() and (fila, columna) not in cartas_seleccionadas:
        if (fila, columna) in cartas_acertadas:
            # La carta ya ha sido acertada, no hacer nada
            return
        voltear_carta(fila, columna)
        botones[fila][columna].config(state=tk.DISABLED)  # Deshabilitar el botón temporalmente
        cartas_volteadas += 1
        cartas_seleccionadas.append((fila, columna))
        if cartas_volteadas == var_juego.get():
            ventana.after(1000, verificar_cartas)
            for fila, columna in cartas_seleccionadas:
                botones[fila][columna].config(state=tk.NORMAL)  # Habilitar el botón nuevamente
def mostrar_mensaje_ganador(jugador_ganador, puntos_ganador):
    global mensaje_ventana  # Utiliza la variable global mensaje_ventana

    # Verificar si hay empate (más de un jugador con la misma puntuación máxima)
    empate = False
    max_puntos = max(puntos.values())
    if list(puntos.values()).count(max_puntos) > 1:
        empate = True

    # Crea una ventana para mostrar el mensaje de fin de juego
    mensaje_ventana = tk.Toplevel(ventana)
    mensaje_ventana.resizable(False, False)
    mensaje_ventana.title("Game Over")

    if empate:
        # Si hay empate, muestra un mensaje indicando el empate
        mensaje_label = tk.Label(mensaje_ventana, text="It's a tie! There's no winner.")
    else:
        # Si no hay empate, muestra el mensaje del ganador
        mensaje_label = tk.Label(mensaje_ventana, text=f"Player {jugador_ganador} wins with {puntos_ganador} points!")

    mensaje_label.pack()

    # Agrega un marco para los botones de reiniciar y cerrar
    botones_frame = tk.Frame(mensaje_ventana)
    botones_frame.pack()

    # Agrega el botón de reinicio
    reiniciar_button = tk.Button(botones_frame, text="Restart game", command=reiniciar_juego)
    reiniciar_button.pack(side=tk.LEFT)

    # Agrega el botón de cerrar
    cerrar_button = tk.Button(botones_frame, text="Close game", command=cerrar_juego)
    cerrar_button.pack(side=tk.RIGHT)

    # Muestra la ventana del mensaje del ganador
    mensaje_ventana.transient(ventana)  # Asocia la ventana del mensaje con la ventana principal
    mensaje_ventana.grab_set()  # Bloquea eventos de otras ventanas
    ventana.wait_window(mensaje_ventana)  # Espera hasta que se cierre la ventana del mensaje



def reiniciar_juego():
    global baraja, tablero, cartas_volteadas, cartas_seleccionadas, cartas_acertadas, puntos, turno, mensaje_ventana

    # Reiniciar todas las variables y el tablero
    baraja = []
    cartas_acertadas = []
    puntos = {}
    turno = 1
    tablero = []
    cartas_volteadas = 0
    cartas_seleccionadas = []

    # Mostrar la ventana de opciones en la ventana de ganador
    mensaje_ventana.destroy()  # Cierra la ventana de ganador
    menu_frame.grid(row=0, column=0, columnspan=5)
    reiniciar_button.pack_forget()  # Ocultar el botón de reinicio
    cerrar_button.pack_forget()  # Ocultar el botón de cerrar
    # Cerrar la ventana de mensaje del ganador si está abierta
    if mensaje_ventana:
        mensaje_ventana.destroy()

def cerrar_juego():
    ventana.destroy()
    
# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Memory game")
ventana.resizable(False, False)
# Crear un Label para mostrar el contador de puntos
puntos_label = tk.Label(ventana, text="Points: 0")
puntos_label.grid(row=0, column=0, columnspan=5, sticky="n")

back_image = Image.open("assets/carta_cerrada.png")
back_image.thumbnail((100, 100))
back_image = ImageTk.PhotoImage(back_image)

# Crear un menú principal con opciones para el jugador
menu_frame = tk.Frame(ventana)
menu_frame.grid(row=0, column=0, columnspan=5)

# Etiqueta para elegir el tipo de juego
tk.Label(menu_frame, text="Select the number of cards to match:").pack()

# Variable para almacenar la elección del jugador (parejas o tríos)
var_juego = tk.IntVar()
var_juego.set(2)  # Inicialmente, seleccionar tríos por defecto

# Botones de radio para seleccionar el tipo de juego
tk.Radiobutton(menu_frame, text="Pairs", variable=var_juego, value=2).pack()
tk.Radiobutton(menu_frame, text="Triplets", variable=var_juego, value=3).pack()

# Etiqueta para elegir la temática
tk.Label(menu_frame, text="Select the theme:").pack()

# Variable para almacenar la elección del jugador (frutas, deportes o videojuegos)
var_tematica = tk.IntVar()
var_tematica.set(1)  # Inicialmente, seleccionar frutas por defecto

# Botones de radio para seleccionar la temática
tk.Radiobutton(menu_frame, text="Fruits", variable=var_tematica, value=1).pack()
tk.Radiobutton(menu_frame, text="Sports", variable=var_tematica, value=2).pack()
tk.Radiobutton(menu_frame, text="Videogames", variable=var_tematica, value=3).pack()

# Etiqueta para ingresar la cantidad de jugadores
tk.Label(menu_frame, text="Enter the number of players:").pack()
entrada_jugadores = tk.Entry(menu_frame)
entrada_jugadores.pack()

reiniciar_button = tk.Button(menu_frame, text="Restart game", command=reiniciar_juego)
cerrar_button = tk.Button(menu_frame, text="Close game", command=cerrar_juego)
reiniciar_button.pack_forget()
cerrar_button.pack_forget()

# Botón para iniciar el juego con la configuración seleccionada
tk.Button(menu_frame, text="Start game", command=iniciar_juego).pack()

# Mostrar la ventana principal
ventana.mainloop()