# menu_principal.py
import tkinter as tk
from tkinter import messagebox

class MenuPrincipal:
    def __init__(self, root, auth, database):
        self.root = root
        self.auth = auth
        self.database = database
        self.crear_menu_principal()
    
    def crear_menu_principal(self):
        """Crea el menú principal con sistema de usuarios"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Configurar ventana - más ancha para tres columnas
        self.root.title("Suite de Juegos - Menú Principal")
        self.root.geometry("900x650")
        self.root.configure(bg='#2C3E50')
        
        # Frame principal
        frame_principal = tk.Frame(self.root, bg='#2C3E50', padx=20, pady=20)
        frame_principal.pack(expand=True, fill='both')
        
        # Barra de usuario
        self.auth.crear_barra_usuario(frame_principal)
        
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
        
        # Frame para botones con TRES COLUMNAS
        frame_botones = tk.Frame(frame_principal, bg='#2C3E50', pady=30)
        frame_botones.pack(expand=True)
        
        # COLUMNA IZQUIERDA - Juegos principales
        frame_col_izq = tk.Frame(frame_botones, bg='#2C3E50')
        frame_col_izq.pack(side='left', padx=15)
        
        botones_izq = [
            ("🔤 SOPA DE LETRAS", "#E74C3C", self.sopa_letras),
            ("🧩 CRUCIGRAMA", "#3498DB", self.cruzigrama), 
            ("💣 BUSCAMINAS", "#2ECC71", self.buscaminas),
            ("🔴 CONECTA PUNTOS", "#9B59B6", self.conecta_puntos),
        ]
        
        for texto, color, comando in botones_izq:
            btn = tk.Button(frame_col_izq, text=texto, 
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
            self.configurar_hover(btn, color)
        
        # COLUMNA CENTRAL - Laberinto, Ahorcado, Torre de Hanói y Sudoku
        frame_col_centro = tk.Frame(frame_botones, bg='#2C3E50')
        frame_col_centro.pack(side='left', padx=15)
        
        botones_centro = [
            ("🧭 LABERINTO", "#E67E22", self.laberinto),
            ("🎯 AHORCADO", "#1ABC9C", self.ahorcado),
            ("🗼 TORRE DE HANÓI", "#16A085", self.torre_hanoi),
            ("🔢 SUDOKU", "#8E44AD", self.sudoku)
        ]
        
        for texto, color, comando in botones_centro:
            btn = tk.Button(frame_col_centro, text=texto, 
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
            self.configurar_hover(btn, color)
        
        # COLUMNA DERECHA - Pong, Puntajes, Usuarios y Salir
        frame_col_der = tk.Frame(frame_botones, bg='#2C3E50')
        frame_col_der.pack(side='left', padx=15)
        
        botones_der = [
            ("🏓 PONG", "#3498DB", self.pong),  # AÑADÍ EL BOTÓN PONG
            ("📊 PUNTAJES", "#F39C12", self.mostrar_puntajes),
            ("👤 USUARIOS", "#16A085", self.menu_usuarios),
            ("🚪 SALIR", "#95A5A6", self.root.quit)
        ]
        
        for texto, color, comando in botones_der:
            btn = tk.Button(frame_col_der, text=texto, 
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
            self.configurar_hover(btn, color)
        
        # Footer con tu nombre
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
    
    def menu_usuarios(self):
        """Menú de gestión de usuarios"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Gestión de Usuarios")
        self.root.geometry("400x300")
        self.root.configure(bg='#2C3E50')
        
        frame_principal = tk.Frame(self.root, bg='#2C3E50', padx=20, pady=20)
        frame_principal.pack(expand=True, fill='both')
        
        # Barra de usuario
        self.auth.crear_barra_usuario(frame_principal)
        
        titulo = tk.Label(frame_principal, text="👤 GESTIÓN DE USUARIOS", 
                         font=("Arial", 16, "bold"), bg='#2C3E50', fg='white',
                         pady=10)
        titulo.pack()
        
        # Botones de usuario
        frame_botones = tk.Frame(frame_principal, bg='#2C3E50', pady=20)
        frame_botones.pack(expand=True)
        
        if self.auth.usuario_actual:
            # Usuario logueado
            tk.Label(frame_botones, text=f"Conectado como: {self.auth.usuario_actual}", 
                    font=("Arial", 12, "bold"), bg='#2C3E50', fg='#2ECC71').pack(pady=10)
            
            tk.Button(frame_botones, text="🚪 Cerrar Sesión", 
                     font=("Arial", 12), bg='#E74C3C', fg='white', width=20,
                     command=self.cerrar_sesion).pack(pady=10)
        else:
            # Usuario no logueado
            tk.Button(frame_botones, text="📝 Registrar Usuario", 
                     font=("Arial", 12), bg='#3498DB', fg='white', width=20,
                     command=self.registrar_usuario).pack(pady=10)
            
            tk.Button(frame_botones, text="🔓 Iniciar Sesión", 
                     font=("Arial", 12), bg='#2ECC71', fg='white', width=20,
                     command=self.iniciar_sesion).pack(pady=10)
        
        tk.Button(frame_botones, text="← Volver al Menú", 
                 font=("Arial", 10), bg='#95A5A6', fg='white',
                 command=self.crear_menu_principal).pack(pady=20)
    
    def registrar_usuario(self):
        """Abre ventana de registro"""
        self.auth.mostrar_ventana_registro(self.root, self.crear_menu_principal)
    
    def iniciar_sesion(self):
        """Abre ventana de login"""
        self.auth.mostrar_ventana_login(self.root, self.crear_menu_principal)
    
    def cerrar_sesion(self):
        """Cierra la sesión"""
        self.auth.cerrar_sesion(self.crear_menu_principal)
    
    def mostrar_puntajes(self):
        """Muestra el sistema completo de puntajes"""
        from puntajes import SistemaPuntajes 
        # Limpiar la ventana primero
        for widget in self.root.winfo_children():
            widget.destroy()
    
        # Crear el sistema de puntajes
        SistemaPuntajes(self.root, self.database, self.auth)
    
    def sopa_letras(self):
        """Abre el juego de Sopa de Letras"""
        from sopa_letras import SopaLetras
        SopaLetras(self.root)
    
    def cruzigrama(self):
        """Abre el juego del Crucigrama"""
        from crucigrama import Crucigrama
        Crucigrama(self.root)
    
    def buscaminas(self):
        """Abre el juego de Buscaminas"""
        from buscaminas import Buscaminas
        Buscaminas(self.root)
    
    def conecta_puntos(self):
        """Abre el juego de Conecta Puntos""" 
        from conecta_puntos import ConectaPuntos
        ConectaPuntos(self.root)
    
    def laberinto(self):
        """Abre el juego de Laberinto"""
        from laberinto import Laberinto
        Laberinto(self.root)
    
    def ahorcado(self):
        """Abre el juego de Ahorcado"""
        from ahorcado import Ahorcado
        Ahorcado(self.root)
    
    def torre_hanoi(self):
        """Abre el juego de Torre de Hanói"""
        from torre_hanoi import TorreHanoi
        TorreHanoi(self.root)
    
    def sudoku(self):
        """Abre el juego de Sudoku"""
        from sudoku import Sudoku
        Sudoku(self.root)
    
    def pong(self):
        """Abre el juego de Pong"""
        from pong import Pong
        Pong(self.root)