# buscaminas.py
import tkinter as tk
from tkinter import messagebox
import random
from app_manager import app_manager

class Buscaminas:
    def __init__(self, root):
        self.root = root
        self.iniciar_juego()
    
    def iniciar_juego(self):
        """Inicia el juego de Buscaminas"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Configurar ventana
        self.root.title("Buscaminas - Suite de Juegos")
        self.root.geometry("500x550")
        self.root.configure(bg='#34495E')
        
        # Frame principal
        self.frame_principal = tk.Frame(self.root, bg='#34495E', padx=20, pady=20)
        self.frame_principal.pack(expand=True, fill='both')
        
        # Barra de usuario (si está disponible)
        if app_manager.auth:
            app_manager.auth.crear_barra_usuario(self.frame_principal)
        
        # Título
        titulo = tk.Label(
            self.frame_principal,
            text="💣 BUSCAMINAS",
            font=("Arial", 18, "bold"),
            bg='#34495E',
            fg='#ECF0F1'
        )
        titulo.pack(pady=10)
        
        # Configuración del juego
        self.filas = 8
        self.columnas = 8
        self.minas = 10
        self.casillas_descubiertas = 0
        self.tablero = []
        self.botones = []
        
        # Contador de minas
        self.contador_minas = tk.Label(
            self.frame_principal,
            text=f"Minas: {self.minas}",
            font=("Arial", 12),
            bg='#34495E',
            fg='#E74C3C'
        )
        self.contador_minas.pack()
        
        # Frame para el tablero
        self.frame_tablero = tk.Frame(self.frame_principal, bg='#34495E')
        self.frame_tablero.pack(pady=20)
        
        # Botón de reinicio
        boton_reinicio = tk.Button(
            self.frame_principal,
            text="🔄 Reiniciar Juego",
            font=("Arial", 10, "bold"),
            bg='#3498DB',
            fg='white',
            command=self.reiniciar_buscaminas
        )
        boton_reinicio.pack(pady=10)
        
        # Botón de volver al menú (SIMPLIFICADO)
        boton_volver = tk.Button(
            self.frame_principal,
            text="← Volver al Menú",
            font=("Arial", 10),
            bg='#95A5A6',
            fg='white',
            command=self.volver_menu_simple
        )
        boton_volver.pack()
        
        # Crear el tablero
        self.crear_tablero_buscaminas()
    
    def crear_tablero_buscaminas(self):
        """Crea el tablero de buscaminas"""
        # (MANTENÉ TODO EL CÓDIGO DEL BUSCAMINAS QUE YA FUNCIONA)
        # Inicializar tablero vacío
        self.tablero = [[0 for _ in range(self.columnas)] for _ in range(self.filas)]
        self.botones = [[None for _ in range(self.columnas)] for _ in range(self.filas)]
        
        # Colocar minas aleatorias
        minas_colocadas = 0
        while minas_colocadas < self.minas:
            fila = random.randint(0, self.filas - 1)
            columna = random.randint(0, self.columnas - 1)
            
            if self.tablero[fila][columna] != -1:
                self.tablero[fila][columna] = -1
                minas_colocadas += 1
        
        # Calcular números alrededor de las minas
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if self.tablero[fila][columna] == -1:
                    continue
                
                minas_adyacentes = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        ni, nj = fila + i, columna + j
                        if (0 <= ni < self.filas and 0 <= nj < self.columnas and 
                            self.tablero[ni][nj] == -1):
                            minas_adyacentes += 1
                
                self.tablero[fila][columna] = minas_adyacentes
        
        # Crear botones del tablero
        for fila in range(self.filas):
            for columna in range(self.columnas):
                boton = tk.Button(
                    self.frame_tablero,
                    text="",
                    width=3,
                    height=1,
                    font=("Arial", 10, "bold"),
                    bg='#BDC3C7',
                    relief='raised'
                )
                boton.grid(row=fila, column=columna, padx=1, pady=1)
                boton.bind('<Button-1>', lambda e, f=fila, c=columna: self.descubrir_casilla(f, c))
                boton.bind('<Button-3>', lambda e, f=fila, c=columna: self.marcar_bandera(f, c))
                
                self.botones[fila][columna] = boton
    
    def descubrir_casilla(self, fila, columna):
        """Descubre una casilla cuando se hace click izquierdo"""
        # (MANTENÉ TODO EL CÓDIGO DEL BUSCAMINAS QUE YA FUNCIONA)
        boton = self.botones[fila][columna]
        
        if boton['state'] == 'disabled' or boton['text'] == '🚩':
            return
        
        valor = self.tablero[fila][columna]
        
        if valor == -1:
            boton.config(text='💣', bg='#E74C3C', state='disabled')
            self.mostrar_game_over()
        else:
            boton.config(state='disabled', relief='sunken', bg='#ECF0F1')
            self.casillas_descubiertas += 1
            
            if valor > 0:
                colores = ['', '#3498DB', '#2ECC71', '#E74C3C', '#8E44AD', 
                          '#F39C12', '#16A085', '#2C3E50', '#7F8C8D']
                boton.config(text=str(valor), fg=colores[valor])
            
            if valor == 0:
                self.descubrir_adyacentes(fila, columna)
            
            if self.casillas_descubiertas == (self.filas * self.columnas - self.minas):
                self.mostrar_victoria()
    
    def descubrir_adyacentes(self, fila, columna):
        # (MANTENÉ EL CÓDIGO EXISTENTE)
        for i in range(-1, 2):
            for j in range(-1, 2):
                ni, nj = fila + i, columna + j
                if (0 <= ni < self.filas and 0 <= nj < self.columnas and 
                    self.botones[ni][nj]['state'] != 'disabled'):
                    self.descubrir_casilla(ni, nj)
    
    def marcar_bandera(self, fila, columna):
        # (MANTENÉ EL CÓDIGO EXISTENTE)
        boton = self.botones[fila][columna]
        
        if boton['state'] != 'disabled':
            if boton['text'] == '':
                boton.config(text='🚩', bg='#F1C40F')
            elif boton['text'] == '🚩':
                boton.config(text='', bg='#BDC3C7')
    
    def mostrar_game_over(self):
        messagebox.showinfo("Game Over", "¡Has pisado una mina! 💣\nInténtalo de nuevo.")
        self.reiniciar_buscaminas()
    
    def mostrar_victoria(self):
        messagebox.showinfo("¡Felicidades!", "¡Has ganado! 🎉\nEncontraste todas las minas.")
    
    def reiniciar_buscaminas(self):
        for widget in self.frame_tablero.winfo_children():
            widget.destroy()
        
        self.casillas_descubiertas = 0
        self.contador_minas.config(text=f"Minas: {self.minas}")
        self.crear_tablero_buscaminas()
    
    def volver_menu_simple(self):
        """Vuelve al menú principal de manera simple"""
        app_manager.volver_al_menu_principal()