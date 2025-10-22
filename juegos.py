# juegos.py 
import tkinter as tk
from tkinter import messagebox
import random

class SuiteJuegos:
    def __init__(self):
        self.root = tk.Tk()
        self.crear_menu_principal()
    
    def crear_menu_principal(self):
        """Crea el menú principal con el diseño"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Configurar ventana
        self.root.title("Suite de Juegos - Menú Principal")
        self.root.geometry("600x500")
        self.root.configure(bg='#2C3E50')
        
        # Frame principal
        frame_principal = tk.Frame(self.root, bg='#2C3E50', padx=20, pady=20)
        frame_principal.pack(expand=True, fill='both')
        
        # Título
        titulo = tk.Label(frame_principal, text="🎮 MI SUITE DE JUEGOS 🎮", 
                         font=("Arial", 20, "bold"), bg='#2C3E50', fg='white',
                         pady=20)
        titulo.pack()
        
        # Subtítulo
        subtitulo = tk.Label(frame_principal, text="Elige tu aventura favorita",
                           font=("Arial", 14), bg='#2C3E50', fg='#BDC3C7',
                           pady=10)
        subtitulo.pack()
        
        # Frame para botones
        frame_botones = tk.Frame(frame_principal, bg='#2C3E50', pady=30)
        frame_botones.pack(expand=True)
        
        # Botones de juegos con colores
        botones_info = [
            ("🔤 SOPA DE LETRAS", "#E74C3C", self.sopa_letras),
            ("🧩 CRUZIGRAMA", "#3498DB", self.cruzigrama), 
            ("💣 BUSCAMINAS", "#2ECC71", self.buscaminas),
            ("📊 PUNTAJES", "#F39C12", self.puntajes),
            ("🚪 SALIR", "#95A5A6", self.root.quit)
        ]
        
        for texto, color, comando in botones_info:
            btn = tk.Button(frame_botones, text=texto, 
                          font=("Arial", 12, "bold"),
                          bg=color, fg='white', 
                          activebackground=color,
                          activeforeground='white',
                          width=20, height=2,
                          relief='flat',
                          border=0,
                          cursor='hand2',
                          command=comando)
            btn.pack(pady=8)
            
            # Efecto hover
            self.configurar_hover(btn, color)
        
        # Footer con nombre
        footer = tk.Label(frame_principal, 
                         text="Desarrollado por Hernán Ariel Ortega Agüero con Python y Tkinter",
                         font=("Arial", 10), bg='#2C3E50', fg='#7F8C8D',
                         pady=20)
        footer.pack(side='bottom')
    
    def configurar_hover(self, boton, color_original):
        """Agrega efecto hover a los botones"""
        def on_enter(e):
            boton['bg'] = self.aclarar_color(color_original)
        
        def on_leave(e):
            boton['bg'] = color_original
        
        boton.bind("<Enter>", on_enter)
        boton.bind("<Leave>", on_leave)
    
    def aclarar_color(self, hex_color, factor=0.2):
        """Aclara un color hexadecimal para efecto hover"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, int(c + (255 - c) * factor)) for c in rgb)
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
    
    def buscaminas(self):
        """Juego de Buscaminas con diseño preferido"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Configurar ventana para buscaminas
        self.root.title("Buscaminas - Suite de Juegos")
        self.root.geometry("500x550")
        self.root.configure(bg='#34495E')
        
        # Frame principal
        self.frame_principal = tk.Frame(self.root, bg='#34495E', padx=20, pady=20)
        self.frame_principal.pack(expand=True, fill='both')
        
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
        
        # Botón de volver al menú
        boton_volver = tk.Button(
            self.frame_principal,
            text="← Volver al Menú",
            font=("Arial", 10),
            bg='#95A5A6',
            fg='white',
            command=self.crear_menu_principal
        )
        boton_volver.pack()
        
        # Crear el tablero
        self.crear_tablero_buscaminas()
    
    def crear_tablero_buscaminas(self):
        """Crea el tablero de buscaminas"""
        # Inicializar tablero vacío
        self.tablero = [[0 for _ in range(self.columnas)] for _ in range(self.filas)]
        self.botones = [[None for _ in range(self.columnas)] for _ in range(self.filas)]
        
        # Colocar minas aleatorias
        minas_colocadas = 0
        while minas_colocadas < self.minas:
            fila = random.randint(0, self.filas - 1)
            columna = random.randint(0, self.columnas - 1)
            
            if self.tablero[fila][columna] != -1:  # -1 representa una mina
                self.tablero[fila][columna] = -1
                minas_colocadas += 1
        
        # Calcular números alrededor de las minas
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if self.tablero[fila][columna] == -1:
                    continue
                
                # Contar minas adyacentes
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
        boton = self.botones[fila][columna]
        
        # Si ya está descubierta o marcada, no hacer nada
        if boton['state'] == 'disabled' or boton['text'] == '🚩':
            return
        
        valor = self.tablero[fila][columna]
        
        if valor == -1:  # Mina
            boton.config(text='💣', bg='#E74C3C', state='disabled')
            self.mostrar_game_over()
        else:
            boton.config(state='disabled', relief='sunken', bg='#ECF0F1')
            self.casillas_descubiertas += 1
            
            if valor > 0:
                # Mostrar número con color
                colores = ['', '#3498DB', '#2ECC71', '#E74C3C', '#8E44AD', 
                          '#F39C12', '#16A085', '#2C3E50', '#7F8C8D']
                boton.config(text=str(valor), fg=colores[valor])
            
            if valor == 0:
                # Descubrir casillas adyacentes automáticamente
                self.descubrir_adyacentes(fila, columna)
            
            # Verificar victoria
            if self.casillas_descubiertas == (self.filas * self.columnas - self.minas):
                self.mostrar_victoria()
    
    def descubrir_adyacentes(self, fila, columna):
        """Descubre casillas adyacentes recursivamente"""
        for i in range(-1, 2):
            for j in range(-1, 2):
                ni, nj = fila + i, columna + j
                if (0 <= ni < self.filas and 0 <= nj < self.columnas and 
                    self.botones[ni][nj]['state'] != 'disabled'):
                    self.descubrir_casilla(ni, nj)
    
    def marcar_bandera(self, fila, columna):
        """Marca/desmarca una bandera con click derecho"""
        boton = self.botones[fila][columna]
        
        if boton['state'] != 'disabled':
            if boton['text'] == '':
                boton.config(text='🚩', bg='#F1C40F')
            elif boton['text'] == '🚩':
                boton.config(text='', bg='#BDC3C7')
    
    def mostrar_game_over(self):
        """Muestra mensaje de Game Over"""
        messagebox.showinfo("Game Over", "¡Has pisado una mina! 💣\nInténtalo de nuevo.")
        self.reiniciar_buscaminas()
    
    def mostrar_victoria(self):
        """Muestra mensaje de victoria"""
        messagebox.showinfo("¡Felicidades!", "¡Has ganado! 🎉\nEncontraste todas las minas.")
    
    def reiniciar_buscaminas(self):
        """Reinicia el juego de buscaminas"""
        # Limpiar tablero actual
        for widget in self.frame_tablero.winfo_children():
            widget.destroy()
        
        # Reiniciar variables
        self.casillas_descubiertas = 0
        self.contador_minas.config(text=f"Minas: {self.minas}")
        
        # Crear nuevo tablero
        self.crear_tablero_buscaminas()
    
    def sopa_letras(self):
        messagebox.showinfo("Próximamente", "¡Sopa de Letras en desarrollo! 🔤")
    
    def cruzigrama(self):
        messagebox.showinfo("Próximamente", "¡Cruzigrama en desarrollo! 🧩")
    
    def puntajes(self):
        messagebox.showinfo("Próximamente", "¡Sistema de puntajes en desarrollo! 📊")
    
    def ejecutar(self):
        self.root.mainloop()

# EJECUTAR EL PROGRAMA
if __name__ == "__main__":
    app = SuiteJuegos()
    app.ejecutar()
