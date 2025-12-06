# pong.py
import tkinter as tk
from tkinter import messagebox
import random
import math
import sys
import os

# Añadir el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Pong:
    def __init__(self, root, auth=None, database=None):
        self.root = root
        self.auth = auth  # Referencia al sistema de autenticación
        self.database = database  # Referencia a la base de datos
        
        self.canvas = None
        self.juego_activo = False
        self.modo_juego = None  # 'solitario' o 'multijugador'
        
        # Dimensiones del juego
        self.ancho = 800
        self.alto = 600
        
        # Pelota - VELOCIDAD MUY RÁPIDA
        self.pelota_x = self.ancho // 2
        self.pelota_y = self.alto // 2
        self.pelota_dx = 0
        self.pelota_dy = 0
        self.pelota_radio = 10
        self.velocidad_total = 14  # ¡MUY RÁPIDA!
        self.velocidad_inicial = 14
        
        # Paletas - MÁS RÁPIDAS (igual que la pelota)
        self.paleta_ancho = 15
        self.paleta_alto = 100
        self.paleta_velocidad = 12  # ¡MUY RÁPIDAS!
        
        # Jugador 1 (izquierda)
        self.paleta1_x = 30
        self.paleta1_y = self.alto // 2 - self.paleta_alto // 2
        
        # Jugador 2 (derecha)
        self.paleta2_x = self.ancho - 30 - self.paleta_ancho
        self.paleta2_y = self.alto // 2 - self.paleta_alto // 2
        
        # Puntajes
        self.puntaje1 = 0
        self.puntaje2 = 0
        self.puntos_ganar = 10
        
        # Controles
        self.teclas_presionadas = set()
        
        # IA - MÁS RÁPIDA
        self.velocidad_ia = 10
        
        # Elementos gráficos
        self.pelota_obj = None
        self.paleta1_obj = None
        self.paleta2_obj = None
        self.texto_puntaje1 = None
        self.texto_puntaje2 = None
        
        # ID del loop del juego
        self.loop_id = None
        
        # Verificar conexión con la base de datos
        self.verificar_conexion_bd()
        
        self.mostrar_menu_principal()
    
    def verificar_conexion_bd(self):
        """Verifica la conexión con la base de datos"""
        print("=" * 50)
        print("Pong: Verificando conexión con base de datos...")
        if self.auth:
            print(f"✓ Auth configurado: {self.auth}")
            if self.auth.usuario_actual:
                print(f"✓ Usuario actual: {self.auth.usuario_actual}")
            else:
                print("⚠️ Usuario no autenticado")
        else:
            print("⚠️ Auth no configurado")
            
        if self.database:
            print("✓ Database configurado")
        else:
            print("⚠️ Database no configurado")
        print("=" * 50)
    
    def mostrar_menu_principal(self):
        """Muestra el menú de selección de modo"""
        # Cancelar loop del juego si está activo
        if self.loop_id:
            self.root.after_cancel(self.loop_id)
            self.loop_id = None
        
        self.juego_activo = False
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Pong - Menú Principal")
        self.root.geometry("700x650")
        self.root.configure(bg='#000000')
        
        main_frame = tk.Frame(self.root, bg='#000000')
        main_frame.pack(fill='both', expand=True, padx=30, pady=10)  # Reducido pady de 20 a 10
        
        # BOTÓN VOLVER - ESQUINA SUPERIOR IZQUIERDA
        volver_frame = tk.Frame(main_frame, bg='#000000')
        volver_frame.pack(anchor='nw', pady=(0, 10))  # Reducido pady de 20 a 10
        
        tk.Button(volver_frame, text="← VOLVER AL MENÚ",
                 font=("Courier", 11, "bold"), bg='#FF0000', fg='#FFFFFF',  # Reducido tamaño fuente
                 padx=15, pady=5, cursor='hand2', relief='flat',  # Reducido padding
                 command=self.volver_menu_principal).pack(side='left')
        
        # Información del usuario (más compacta)
        if self.auth and self.auth.usuario_actual:
            tk.Label(main_frame, text=f"👤 Jugando como: {self.auth.usuario_actual}",
                    font=("Courier", 9, "bold"), bg='#000000', fg='#00FF00').pack(pady=(0, 5))  # Reducido tamaño
        else:
            tk.Label(main_frame, text="⚠️ No autenticado - Los puntajes no se guardarán",
                    font=("Courier", 8), bg='#000000', fg='#FF0000').pack(pady=(0, 5))  # Reducido tamaño
        
        # Título (más arriba y más compacto)
        title_frame = tk.Frame(main_frame, bg='#000000')
        title_frame.pack(pady=(0, 5))  # Reducido pady de 20 a 5
        
        tk.Label(title_frame, text="🏓 PONG 🏓",
                 font=("Courier", 40, "bold"), bg='#000000', fg='#00FF00').pack()  # Reducido tamaño de 48 a 40
        
        tk.Label(title_frame, text="El clásico juego de arcade",
                 font=("Courier", 12), bg='#000000', fg='#FFFFFF').pack()  # Reducido tamaño
        
        # Frame para botones de modo (más compacto)
        frame_modos = tk.Frame(main_frame, bg='#000000')
        frame_modos.pack(fill='both', expand=True, pady=15)  # Reducido pady de 30 a 15
        
        # Botón Un Jugador (más compacto)
        frame_solitario = tk.Frame(frame_modos, bg='#1a1a1a', relief='solid', bd=2)  # Reducido borde
        frame_solitario.pack(pady=8, padx=40, fill='x')  # Reducido padding
        
        content1 = tk.Frame(frame_solitario, bg='#1a1a1a')
        content1.pack(fill='x', padx=15, pady=10)  # Reducido padding
        
        tk.Label(content1, text="🤖 UN JUGADOR",
                font=("Courier", 14, "bold"), bg='#1a1a1a', fg='#00FF00').pack()  # Reducido tamaño
        
        tk.Label(content1, text="Juega contra la IA",
                font=("Courier", 10), bg='#1a1a1a', fg='#888888').pack(pady=(2, 4))  # Reducido padding
        
        tk.Label(content1, text="Controles: ↑ ↓",
                font=("Courier", 9), bg='#1a1a1a', fg='#FFFF00').pack()  # Reducido tamaño
        
        tk.Label(content1, text="¡Los puntajes se guardan si ganas!",
                font=("Courier", 8, "italic"), bg='#1a1a1a', fg='#00FF00').pack(pady=(3, 0))  # Reducido tamaño
        
        btn_solitario = tk.Button(frame_solitario, text="JUGAR",
                                 font=("Courier", 11, "bold"), bg='#00FF00', fg='#000000',  # Reducido tamaño
                                 width=10, height=1, cursor='hand2', relief='flat',  # Reducido width
                                 command=self.iniciar_solitario)
        btn_solitario.pack(pady=(0, 10))  # Reducido padding
        
        # Botón Dos Jugadores (más compacto)
        frame_multi = tk.Frame(frame_modos, bg='#1a1a1a', relief='solid', bd=2)  # Reducido borde
        frame_multi.pack(pady=8, padx=40, fill='x')  # Reducido padding
        
        content2 = tk.Frame(frame_multi, bg='#1a1a1a')
        content2.pack(fill='x', padx=15, pady=10)  # Reducido padding
        
        tk.Label(content2, text="👥 DOS JUGADORES",
                font=("Courier", 14, "bold"), bg='#1a1a1a', fg='#00FFFF').pack()  # Reducido tamaño
        
        tk.Label(content2, text="Juega con un amigo",
                font=("Courier", 10), bg='#1a1a1a', fg='#888888').pack(pady=(2, 4))  # Reducido padding
        
        tk.Label(content2, text="J1: W S  |  J2: ↑ ↓",
                font=("Courier", 9), bg='#1a1a1a', fg='#FFFF00').pack()  # Reducido tamaño
        
        tk.Label(content2, text="Los puntajes no se guardan en este modo",
                font=("Courier", 8, "italic"), bg='#1a1a1a', fg='#888888').pack(pady=(3, 0))  # Reducido tamaño
        
        btn_multi = tk.Button(frame_multi, text="JUGAR",
                             font=("Courier", 11, "bold"), bg='#00FFFF', fg='#000000',  # Reducido tamaño
                             width=10, height=1, cursor='hand2', relief='flat',  # Reducido width
                             command=self.iniciar_multijugador)
        btn_multi.pack(pady=(0, 10))  # Reducido padding
        
        # Espacio adicional en la parte inferior si es necesario
        bottom_space = tk.Frame(main_frame, bg='#000000', height=20)
        bottom_space.pack(fill='x')
    
    def iniciar_solitario(self):
        """Inicia el modo un jugador"""
        self.modo_juego = 'solitario'
        self.iniciar_juego()
    
    def iniciar_multijugador(self):
        """Inicia el modo dos jugadores"""
        self.modo_juego = 'multijugador'
        self.iniciar_juego()
    
    def iniciar_juego(self):
        """Inicializa el juego"""
        # Cancelar loop anterior si existe
        if self.loop_id:
            self.root.after_cancel(self.loop_id)
            self.loop_id = None
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title(f"Pong - {'Un Jugador' if self.modo_juego == 'solitario' else 'Dos Jugadores'}")
        self.root.geometry(f"{self.ancho}x{self.alto + 100}")
        self.root.configure(bg='#000000')
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#000000')
        main_frame.pack(fill='both', expand=True)
        
        # Header con botón volver
        header = tk.Frame(main_frame, bg='#000000')
        header.pack(fill='x', pady=(0, 10))
        
        tk.Button(header, text="← MENÚ PONG",
                 font=("Courier", 11, "bold"), bg='#FF0000', fg='#FFFFFF',
                 padx=15, pady=5, cursor='hand2', relief='flat',
                 command=self.volver_menu_pong).pack(side='left')
        
        # Información de usuario
        if self.auth and self.auth.usuario_actual:
            tk.Label(header, text=f"👤 {self.auth.usuario_actual}",
                    font=("Courier", 9, "bold"), bg='#000000', fg='#00FF00').pack(side='right', padx=15)
        
        # Canvas para el juego
        self.canvas = tk.Canvas(main_frame, bg='#000000', width=self.ancho, height=self.alto,
                               highlightthickness=0)
        self.canvas.pack(pady=5)  # Reducido padding
        
        # Resetear valores
        self.puntaje1 = 0
        self.puntaje2 = 0
        self.juego_activo = True
        self.teclas_presionadas = set()
        
        # Resetear posiciones
        self.paleta1_y = self.alto // 2 - self.paleta_alto // 2
        self.paleta2_y = self.alto // 2 - self.paleta_alto // 2
        
        # Crear elementos gráficos
        self.crear_elementos()
        
        # Binds de teclado
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)
        
        # Información de controles
        info_frame = tk.Frame(main_frame, bg='#000000')
        info_frame.pack(pady=5)  # Reducido padding
        
        if self.modo_juego == 'solitario':
            tk.Label(info_frame, text="Controles: ↑ ↓  |  ESC: Salir",
                    font=("Courier", 10, "bold"), bg='#000000', fg='#00FF00').pack()  # Reducido tamaño
        else:
            tk.Label(info_frame, text="Jugador 1: W S  |  Jugador 2: ↑ ↓  |  ESC: Salir",
                    font=("Courier", 10, "bold"), bg='#000000', fg='#00FFFF').pack()  # Reducido tamaño
        
        # Iniciar pelota
        self.servir_pelota()
        
        # Iniciar loop del juego
        self.actualizar_juego()
    
    def volver_menu_pong(self):
        """Vuelve al menú de Pong desde la partida"""
        self.juego_activo = False
        if self.loop_id:
            self.root.after_cancel(self.loop_id)
            self.loop_id = None
        
        # Quitar binds de teclado
        self.root.unbind('<KeyPress>')
        self.root.unbind('<KeyRelease>')
        
        self.mostrar_menu_principal()
    
    def crear_elementos(self):
        """Crea los elementos gráficos del juego"""
        # Línea central
        for i in range(0, self.alto, 20):
            self.canvas.create_line(self.ancho // 2, i, self.ancho // 2, i + 10,
                                   fill='#444444', width=3)
        
        # Paleta 1 (izquierda)
        self.paleta1_obj = self.canvas.create_rectangle(
            self.paleta1_x, self.paleta1_y,
            self.paleta1_x + self.paleta_ancho, self.paleta1_y + self.paleta_alto,
            fill='#00FF00', outline='#00FF00'
        )
        
        # Paleta 2 (derecha)
        color_paleta2 = '#00FFFF' if self.modo_juego == 'multijugador' else '#FF0000'
        self.paleta2_obj = self.canvas.create_rectangle(
            self.paleta2_x, self.paleta2_y,
            self.paleta2_x + self.paleta_ancho, self.paleta2_y + self.paleta_alto,
            fill=color_paleta2, outline=color_paleta2
        )
        
        # Pelota
        self.pelota_obj = self.canvas.create_oval(
            self.pelota_x - self.pelota_radio, self.pelota_y - self.pelota_radio,
            self.pelota_x + self.pelota_radio, self.pelota_y + self.pelota_radio,
            fill='#FFFFFF', outline='#FFFFFF'
        )
        
        # Puntajes
        self.texto_puntaje1 = self.canvas.create_text(
            self.ancho // 4, 50,
            text=str(self.puntaje1), font=("Courier", 48, "bold"),
            fill='#00FF00'
        )
        
        color_puntaje2 = '#00FFFF' if self.modo_juego == 'multijugador' else '#FF0000'
        self.texto_puntaje2 = self.canvas.create_text(
            3 * self.ancho // 4, 50,
            text=str(self.puntaje2), font=("Courier", 48, "bold"),
            fill=color_puntaje2
        )
    
    def servir_pelota(self):
        """Sirve la pelota desde el centro con velocidad constante"""
        self.pelota_x = self.ancho // 2
        self.pelota_y = self.alto // 2
        
        # Restablecer velocidad total constante
        self.velocidad_total = self.velocidad_inicial
        
        # Ángulo aleatorio para variedad
        angulo = random.uniform(30, 60)
        
        # Dirección aleatoria (izquierda o derecha)
        direccion_x = random.choice([-1, 1])
        direccion_y = random.choice([-1, 1])
        
        # Calcular componentes con velocidad CONSTANTE Y MUY RÁPIDA
        self.pelota_dx = self.velocidad_total * math.cos(math.radians(angulo)) * direccion_x
        self.pelota_dy = self.velocidad_total * math.sin(math.radians(angulo)) * direccion_y
        
        # Asegurar velocidad mínima en ambos ejes
        min_velocidad = 4.0
        if abs(self.pelota_dx) < min_velocidad:
            self.pelota_dx = min_velocidad if self.pelota_dx >= 0 else -min_velocidad
        if abs(self.pelota_dy) < min_velocidad:
            self.pelota_dy = min_velocidad if self.pelota_dy >= 0 else -min_velocidad
    
    def on_key_press(self, event):
        """Maneja las teclas presionadas"""
        self.teclas_presionadas.add(event.keysym.lower())
        
        # ESC para salir al menú de Pong
        if event.keysym == 'Escape':
            self.volver_menu_pong()
    
    def on_key_release(self, event):
        """Maneja las teclas liberadas"""
        self.teclas_presionadas.discard(event.keysym.lower())
    
    def actualizar_juego(self):
        """Loop principal del juego"""
        if not self.juego_activo:
            return
        
        try:
            # Mover paletas según controles - MÁS RÁPIDAS
            if self.modo_juego == 'multijugador':
                # Jugador 1 (W/S) - MUY RÁPIDAS
                if 'w' in self.teclas_presionadas:
                    self.paleta1_y = max(0, self.paleta1_y - self.paleta_velocidad)
                if 's' in self.teclas_presionadas:
                    self.paleta1_y = min(self.alto - self.paleta_alto, self.paleta1_y + self.paleta_velocidad)
                
                # Jugador 2 (↑/↓) - MUY RÁPIDAS
                if 'up' in self.teclas_presionadas:
                    self.paleta2_y = max(0, self.paleta2_y - self.paleta_velocidad)
                if 'down' in self.teclas_presionadas:
                    self.paleta2_y = min(self.alto - self.paleta_alto, self.paleta2_y + self.paleta_velocidad)
            else:
                # Modo solitario - Jugador controla paleta derecha
                if 'up' in self.teclas_presionadas:
                    self.paleta2_y = max(0, self.paleta2_y - self.paleta_velocidad)
                if 'down' in self.teclas_presionadas:
                    self.paleta2_y = min(self.alto - self.paleta_alto, self.paleta2_y + self.paleta_velocidad)
                
                # IA controla paleta izquierda - MÁS RÁPIDA
                self.mover_ia()
            
            # Mover pelota - MUY RÁPIDA
            self.pelota_x += self.pelota_dx
            self.pelota_y += self.pelota_dy
            
            # Colisión con bordes superior/inferior - REBOTE RÁPIDO
            if self.pelota_y - self.pelota_radio <= 0:
                self.pelota_y = self.pelota_radio
                self.pelota_dy = abs(self.pelota_dy)  # Rebote simple
            
            if self.pelota_y + self.pelota_radio >= self.alto:
                self.pelota_y = self.alto - self.pelota_radio
                self.pelota_dy = -abs(self.pelota_dy)  # Rebote simple
            
            # Colisión con paleta 1 - REBOTE MUY RÁPIDO
            if (self.paleta1_x <= self.pelota_x - self.pelota_radio <= self.paleta1_x + self.paleta_ancho and
                self.paleta1_y <= self.pelota_y <= self.paleta1_y + self.paleta_alto):
                
                # Corregir posición
                self.pelota_x = self.paleta1_x + self.paleta_ancho + self.pelota_radio
                
                # Calcular ángulo basado en dónde golpea
                impacto = (self.pelota_y - (self.paleta1_y + self.paleta_alto // 2)) / (self.paleta_alto // 2)
                
                # Rebote con velocidad CONSTANTE Y RÁPIDA
                self.pelota_dx = abs(self.velocidad_total * 0.85)  # Mantener velocidad
                self.pelota_dy = self.velocidad_total * impacto * 0.7  # Ángulo controlado
            
            # Colisión con paleta 2 - REBOTE MUY RÁPIDO
            if (self.paleta2_x <= self.pelota_x + self.pelota_radio <= self.paleta2_x + self.paleta_ancho and
                self.paleta2_y <= self.pelota_y <= self.paleta2_y + self.paleta_alto):
                
                # Corregir posición
                self.pelota_x = self.paleta2_x - self.pelota_radio
                
                # Calcular ángulo basado en dónde golpea
                impacto = (self.pelota_y - (self.paleta2_y + self.paleta_alto // 2)) / (self.paleta_alto // 2)
                
                # Rebote con velocidad CONSTANTE Y RÁPIDA
                self.pelota_dx = -abs(self.velocidad_total * 0.85)  # Mantener velocidad
                self.pelota_dy = self.velocidad_total * impacto * 0.7  # Ángulo controlado
            
            # Normalizar velocidad para mantenerla constante y MUY RÁPIDA
            velocidad_actual = math.sqrt(self.pelota_dx**2 + self.pelota_dy**2)
            if velocidad_actual > 0:
                factor = self.velocidad_total / velocidad_actual
                self.pelota_dx *= factor
                self.pelota_dy *= factor
            
            # Puntos
            if self.pelota_x < 0:
                self.puntaje2 += 1
                self.actualizar_puntajes()
                if self.puntaje2 >= self.puntos_ganar:
                    self.fin_juego(2)
                    return
                self.servir_pelota()
            
            if self.pelota_x > self.ancho:
                self.puntaje1 += 1
                self.actualizar_puntajes()
                if self.puntaje1 >= self.puntos_ganar:
                    self.fin_juego(1)
                    return
                self.servir_pelota()
            
            # Actualizar posiciones en canvas
            self.canvas.coords(self.pelota_obj,
                              self.pelota_x - self.pelota_radio, self.pelota_y - self.pelota_radio,
                              self.pelota_x + self.pelota_radio, self.pelota_y + self.pelota_radio)
            
            self.canvas.coords(self.paleta1_obj,
                              self.paleta1_x, self.paleta1_y,
                              self.paleta1_x + self.paleta_ancho, self.paleta1_y + self.paleta_alto)
            
            self.canvas.coords(self.paleta2_obj,
                              self.paleta2_x, self.paleta2_y,
                              self.paleta2_x + self.paleta_ancho, self.paleta2_y + self.paleta_alto)
            
            # Siguiente frame - Mantener 60 FPS
            self.loop_id = self.root.after(16, self.actualizar_juego)
            
        except tk.TclError:
            # Si el canvas fue destruido, detener el juego
            self.juego_activo = False
            return
    
    def mover_ia(self):
        """Mueve la paleta de la IA - MÁS RÁPIDA Y EFICIENTE"""
        centro_paleta = self.paleta1_y + self.paleta_alto // 2
        
        # Seguir pelota con predicción mejorada
        if self.pelota_dx < 0:  # Pelota va hacia la IA
            # Predecir posición futura
            tiempo_estimado = abs((self.pelota_x - self.paleta1_x) / self.pelota_dx)
            prediccion_y = self.pelota_y + (self.pelota_dy * tiempo_estimado)
            
            # Asegurar predicción dentro de límites
            if prediccion_y < 0:
                prediccion_y = abs(prediccion_y)
            elif prediccion_y > self.alto:
                prediccion_y = self.alto - (prediccion_y % self.alto)
            
            objetivo = prediccion_y
        else:
            objetivo = self.pelota_y
        
        # Mover hacia el objetivo - MÁS RÁPIDO
        if centro_paleta < objetivo - 5:
            self.paleta1_y = min(self.alto - self.paleta_alto, self.paleta1_y + self.velocidad_ia)
        elif centro_paleta > objetivo + 5:
            self.paleta1_y = max(0, self.paleta1_y - self.velocidad_ia)
    
    def actualizar_puntajes(self):
        """Actualiza los textos de puntaje"""
        self.canvas.itemconfig(self.texto_puntaje1, text=str(self.puntaje1))
        self.canvas.itemconfig(self.texto_puntaje2, text=str(self.puntaje2))
    
    def fin_juego(self, ganador):
        """Maneja el fin del juego"""
        self.juego_activo = False
        if self.loop_id:
            self.root.after_cancel(self.loop_id)
            self.loop_id = None
        
        # Quitar binds de teclado
        self.root.unbind('<KeyPress>')
        self.root.unbind('<KeyRelease>')
        
        # Calcular puntaje basado en el juego
        puntaje_guardado = False
        mensaje_guardado = ""
        
        if self.modo_juego == 'solitario' and ganador == 2:
            # Solo guardar si el jugador gana en solitario (jugador 2 es el humano)
            puntaje = self.calcular_puntaje()
            
            if self.auth and self.auth.usuario_actual and self.database:
                try:
                    usuario_id = self.database.obtener_id_usuario(self.auth.usuario_actual)
                    if usuario_id:
                        # Guardar el puntaje usando el método correcto
                        exito = self.database.guardar_puntaje(
                            usuario_id=usuario_id,
                            juego="Pong",
                            puntaje=puntaje,
                            dificultad="Solitario Rápido",
                            categoria="Modo Rápido"
                        )
                        
                        if exito:
                            print(f"✅ Pong - Puntaje guardado: {puntaje} para usuario {self.auth.usuario_actual}")
                            puntaje_guardado = True
                            mensaje_guardado = f"✅ Puntaje guardado: {puntaje} puntos"
                            
                            # Verificar que se guardó realmente
                            self.verificar_puntaje_guardado(usuario_id, puntaje)
                        else:
                            print("❌ Pong - No se pudo guardar el puntaje")
                            mensaje_guardado = "❌ Error al guardar puntaje"
                    else:
                        print("⚠️ Pong - No se pudo obtener el ID del usuario")
                        mensaje_guardado = "⚠️ Usuario no encontrado en BD"
                except Exception as e:
                    print(f"❌ Pong - Error al guardar puntaje: {e}")
                    mensaje_guardado = f"❌ Error técnico: {str(e)[:50]}..."
            else:
                print("⚠️ Pong - Usuario no autenticado o sin BD")
                mensaje_guardado = "⚠️ Inicia sesión para guardar puntajes"
        
        # Crear mensaje de fin de juego
        if self.modo_juego == 'solitario':
            if ganador == 2:
                mensaje = "⚡ ¡VICTORIA RÁPIDA! ⚡\n\n¡Derrotaste a la IA!\n\n"
            else:
                mensaje = "😢 DERROTA 😢\n\nLa IA te ha derrotado.\n\n"
        else:
            mensaje = f"⚡ ¡VICTORIA RÁPIDA! ⚡\n\nJugador {ganador} gana!\n\n"
        
        mensaje += f"Puntaje Final:\nJugador 1: {self.puntaje1}\nJugador 2: {self.puntaje2}\n\n"
        
        if puntaje_guardado:
            mensaje += mensaje_guardado
        elif self.modo_juego == 'solitario' and ganador == 2:
            mensaje += "⚠️ Los puntajes no se guardaron (sin autenticación)"
        
        messagebox.showinfo("Fin del Juego", mensaje)
        self.mostrar_menu_principal()
    
    def calcular_puntaje(self):
        """Calcula el puntaje basado en el rendimiento"""
        # Base por ganar
        puntaje_base = 1000
        
        # Bonus por diferencia de puntos
        diferencia = abs(self.puntaje1 - self.puntaje2)
        bonus_diferencia = diferencia * 50
        
        # Bonus por velocidad (si terminó rápido)
        # En este caso, como es rápido por defecto, siempre damos bonus
        bonus_velocidad = 500
        
        # Bonus extra si fue una victoria contundente (10-0, 10-1, etc.)
        if self.puntaje2 >= 10 and self.puntaje1 <= 3:
            bonus_contundente = 300
        elif self.puntaje2 >= 10 and self.puntaje1 <= 5:
            bonus_contundente = 150
        else:
            bonus_contundente = 0
        
        total = puntaje_base + bonus_diferencia + bonus_velocidad + bonus_contundente
        return total
    
    def verificar_puntaje_guardado(self, usuario_id, puntaje):
        """Verifica que el puntaje se guardó correctamente"""
        try:
            conexion = self.database.get_conexion()
            cursor = conexion.cursor()
            
            # Buscar el puntaje recién guardado
            cursor.execute('''
                SELECT COUNT(*) FROM puntajes 
                WHERE usuario_id = ? AND juego = ? AND puntaje >= ? AND categoria LIKE ?
            ''', (usuario_id, "Pong", puntaje * 0.9, "%Modo Rápido%"))
            
            count = cursor.fetchone()[0]
            
            # Mostrar todos los puntajes del usuario para debug
            cursor.execute('''
                SELECT * FROM puntajes 
                WHERE usuario_id = ? AND juego = ?
                ORDER BY fecha DESC
                LIMIT 5
            ''', (usuario_id, "Pong"))
            
            puntajes = cursor.fetchall()
            print(f"📊 Pong - Últimos 5 puntajes del usuario: {puntajes}")
            
            conexion.close()
            
            if count > 0:
                print(f"✅ Pong - Verificación: Puntaje encontrado en la BD")
            else:
                print("❌ Pong - Verificación: Puntaje NO encontrado en la BD")
                
        except Exception as e:
            print(f"❌ Pong - Error en verificación: {e}")
    
    def volver_menu_principal(self):
        """Vuelve al menú principal de la aplicación"""
        # Cancelar loop del juego si está activo
        if self.loop_id:
            self.root.after_cancel(self.loop_id)
            self.loop_id = None
        
        self.juego_activo = False
        try:
            from menu_principal import MenuPrincipal
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Volver al menú principal pasando auth y database
            MenuPrincipal(self.root, self.auth, self.database)
            
        except Exception as e:
            print(f"Pong - Error volviendo al menú: {e}")
            # Si hay error, intentar cerrar limpiamente
            try:
                self.root.quit()
            except:
                pass


# Función principal para iniciar el juego desde el menú principal
def iniciar_pong(root, auth=None, database=None):
    """Función para iniciar Pong desde el menú principal"""
    for widget in root.winfo_children():
        widget.destroy()
    
    # Crear instancia pasando auth y database
    app = Pong(root, auth, database)


# Test
if __name__ == "__main__":
    root = tk.Tk()
    
    # Para testing, crear auth y database mock si no existen
    try:
        from database import Database
        from auth import AuthManager
        
        db = Database()
        auth = AuthManager(db)
        
        # Configurar usuario de prueba (opcional)
        # auth.usuario_actual = "test_user"
        
        app = Pong(root, auth, db)
    except ImportError:
        print("⚠️ Pong - No se encontraron módulos de auth/database, ejecutando en modo prueba")
        app = Pong(root)
    
    root.mainloop()