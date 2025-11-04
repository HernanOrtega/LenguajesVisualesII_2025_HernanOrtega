import tkinter as tk
from tkinter import messagebox, ttk
import random
import datetime
from app_manager import app_manager

class SopaLetras:
    def __init__(self, root):
        self.root = root
        self.tablero = []
        self.palabras_encontradas = []
        self.seleccion_actual = []
        self.botones_tablero = []
        self.tiempo_inicio = None
        self.puntaje = 0
        self.categoria_actual = None
        self.juego_activo = True  # Nuevo: controlar si el juego está activo
        
        # Rastrear qué celdas pertenecen a qué palabras
        self.celdas_palabras = {}  # {(fila, col): [lista de palabras]}
        
        # Datos integrados - SIN BASE DE DATOS
        self.categorias_data = self.obtener_categorias_integradas()
        self.palabras_data = self.obtener_palabras_integradas()
        
        self.mostrar_configuracion()
    
    def obtener_categorias_integradas(self):
        """Devuelve las categorías integradas en el código"""
        return [
            (1, 'Música'),
            (2, 'Cine'), 
            (3, 'Videojuegos'),
            (4, 'Ciencia'),
            (5, 'Geografía'),
            (6, 'Comida')
        ]
    
    def obtener_palabras_integradas(self):
        """Devuelve todas las palabras integradas en el código"""
        return {
            # MÚSICA - 10 palabras
            1: [
                ('GUITARRA', 'Instrumento de cuerdas'),
                ('PIANO', 'Instrumento de teclas'),
                ('BAILE', 'Moverse al ritmo'),
                ('CANTO', 'Arte de la voz'),
                ('NOTA', 'Sonido musical'),
                ('RITMO', 'Patrón musical'),
                ('MELODIA', 'Sucesión de notas'),
                ('ARMONIA', 'Combinación de sonidos'),
                ('ORQUESTA', 'Conjunto de músicos'),
                ('CONCIERTO', 'Presentación musical')
            ],
            # CINE - 10 palabras
            2: [
                ('ACTOR', 'Intérprete de papeles'),
                ('PELICULA', 'Obra cinematográfica'),
                ('ESCENA', 'Parte de una película'),
                ('CAMARA', 'Equipo de filmación'),
                ('DIRECTOR', 'Líder del rodaje'),
                ('GUION', 'Texto de la película'),
                ('ESTRENO', 'Primera presentación'),
                ('TAQUILLA', 'Venta de entradas'),
                ('PRODUCCION', 'Proceso de filmación'),
                ('FOTOGRAFIA', 'Arte visual del cine')
            ],
            # VIDEOJUEGOS - 10 palabras
            3: [
                ('JUEGO', 'Entretenimiento digital'),
                ('NIVEL', 'Etapa del juego'),
                ('PUNTOS', 'Unidad de puntuación'),
                ('VIDA', 'Oportunidades del jugador'),
                ('MANDO', 'Dispositivo de control'),
                ('PANTALLA', 'Interfaz visual'),
                ('JUGADOR', 'Persona que juega'),
                ('CONSOLA', 'Sistema de videojuegos'),
                ('PERSONAJE', 'Avatar del juego'),
                ('ESTRATEGIA', 'Género de juego')
            ],
            # CIENCIA - 10 palabras
            4: [
                ('ATOMO', 'Partícula fundamental'),
                ('CELULA', 'Unidad básica de vida'),
                ('ENERGIA', 'Capacidad de trabajo'),
                ('MATERIA', 'Sustancia física'),
                ('QUIMICA', 'Ciencia de la materia'),
                ('FISICA', 'Ciencia de la energía'),
                ('BIOLOGIA', 'Ciencia de la vida'),
                ('MOLECULA', 'Conjunto de átomos'),
                ('EXPERIMENTO', 'Prueba científica'),
                ('LABORATORIO', 'Lugar de investigación')
            ],
            # GEOGRAFÍA - 10 palabras
            5: [
                ('PARAGUAY', 'País sudamericano'),
                ('ASUNCION', 'Capital paraguaya'),
                ('RIO', 'Corriente de agua'),
                ('MONTE', 'Elevación terrestre'),
                ('MAPA', 'Representación geográfica'),
                ('PAIS', 'Territorio nacional'),
                ('CIUDAD', 'Área urbana'),
                ('CONTINENTE', 'Gran masa terrestre'),
                ('OCEANO', 'Gran masa de agua'),
                ('CORDILLERA', 'Sistema montañoso')
            ],
            # COMIDA - 10 palabras
            6: [
                ('ASADO', 'Carne a la parrilla'),
                ('SOPA', 'Alimento líquido'),
                ('PAN', 'Alimento horneado'),
                ('QUESO', 'Producto lácteo'),
                ('FRUTA', 'Alimento natural'),
                ('ARROZ', 'Cereal alimenticio'),
                ('PASTA', 'Comida italiana'),
                ('VERDURA', 'Vegetal comestible'),
                ('EMPANADA', 'Masa rellena típica'),
                ('CHOCOLATE', 'Dulce de cacao')
            ]
        }

    # ... (Los métodos de configuración se mantienen igual)
    
    def mostrar_configuracion(self):
        """Muestra la pantalla de configuración de la sopa de letras"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Sopa de Letras - Configuración")
        self.root.geometry("500x400")
        self.root.configure(bg='#2C3E50')
        
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        tk.Label(main_frame, text="🔤 SOPA DE LETRAS", 
                font=("Arial", 20, "bold"), bg='#2C3E50', fg='white',
                pady=15).pack()
        
        frame_config = tk.Frame(main_frame, bg='#2C3E50')
        frame_config.pack(fill='both', expand=True, pady=10)
        
        tk.Label(frame_config, text="🎯 SELECCIONA UNA CATEGORÍA:", 
                font=("Arial", 12, "bold"), bg='#2C3E50', fg='#BDC3C7',
                pady=5).pack(anchor='w')
        
        nombres_categorias = [cat[1] for cat in self.categorias_data]
        
        self.combo_categoria = ttk.Combobox(frame_config, 
                                          values=nombres_categorias,
                                          font=("Arial", 11),
                                          state="readonly")
        self.combo_categoria.set(nombres_categorias[0])
        self.combo_categoria.pack(fill='x', pady=(5, 15))
        
        # Información del juego
        info_frame = tk.Frame(frame_config, bg='#2C3E50')
        info_frame.pack(fill='x', pady=10)
        
        tk.Label(info_frame, text="🎮 CONFIGURACIÓN ACTUAL:", 
                font=("Arial", 12, "bold"), bg='#2C3E50', fg='#BDC3C7',
                pady=5).pack(anchor='w')
        
        tk.Label(info_frame, text="• Tablero: 20x20 casillas", 
                font=("Arial", 10), bg='#2C3E50', fg='#ECF0F1',
                pady=2).pack(anchor='w')
        
        tk.Label(info_frame, text="• Palabras a encontrar: 10", 
                font=("Arial", 10), bg='#2C3E50', fg='#ECF0F1',
                pady=2).pack(anchor='w')
        
        tk.Label(info_frame, text="• Todas las categorías disponibles ✓", 
                font=("Arial", 10), bg='#2C3E50', fg='#2ECC71',
                pady=2).pack(anchor='w')
        
        frame_botones = tk.Frame(main_frame, bg='#2C3E50')
        frame_botones.pack(fill='x', pady=20)
        
        btn_iniciar = tk.Button(frame_botones, text="🎮 INICIAR JUEGO", 
                 font=("Arial", 14, "bold"), bg='#2ECC71', fg='white',
                 padx=30, pady=12, cursor='hand2',
                 command=self.iniciar_juego)
        btn_iniciar.pack(side='left', padx=10)
        
        btn_volver = tk.Button(frame_botones, text="← VOLVER AL MENÚ", 
                 font=("Arial", 11), bg='#95A5A6', fg='white',
                 padx=20, pady=10, cursor='hand2',
                 command=self.volver_menu_principal)
        btn_volver.pack(side='left', padx=10)
    
    def iniciar_juego(self):
        """Inicia el juego"""
        categoria = self.combo_categoria.get()
        
        if not categoria:
            messagebox.showwarning("Advertencia", "Por favor selecciona una categoría.")
            return
        
        # Buscar ID de categoría
        categoria_id = None
        for cat_id, cat_nombre in self.categorias_data:
            if cat_nombre == categoria:
                categoria_id = cat_id
                break
        
        if not categoria_id:
            messagebox.showerror("Error", "Categoría no válida")
            return
        
        # Obtener palabras INTEGRADAS (sin BD)
        palabras_integradas = self.obtener_palabras_desde_bd(categoria_id)
        
        if not palabras_integradas:
            messagebox.showwarning("Sin palabras", 
                                  f"No hay palabras disponibles para:\nCategoría: {categoria}")
            return
        
        # Usar todas las palabras (10 palabras por categoría)
        palabras_data = palabras_integradas
        
        # Tablero fijo de 20x20
        filas, columnas = 20, 20
        
        self.categoria_actual = categoria
        self.juego_activo = True  # Reiniciar estado del juego
        
        # Reiniciar el rastreo de celdas
        self.celdas_palabras = {}
        
        self.jugar_sopa_letras(categoria, palabras_data, filas, columnas)

    def obtener_palabras_desde_bd(self, categoria_id):
        """Obtiene palabras integradas (sin BD)"""
        try:
            if categoria_id in self.palabras_data:
                return self.palabras_data[categoria_id]
            return []
        except Exception as e:
            print(f"ERROR obteniendo palabras integradas: {e}")
            return []

    # ... (Los métodos crear_tablero, registrar_celdas_palabra, puede_colocar_palabra, colocar_palabra se mantienen igual)

    def crear_tablero(self, filas, columnas, palabras):
        """Crea el tablero de sopa de letras"""
        tablero = [['' for _ in range(columnas)] for _ in range(filas)]
        palabras_colocadas = []
        
        # Inicializar el rastreo de celdas
        self.celdas_palabras = {}
        
        # Intentar colocar cada palabra
        for palabra, pista in palabras:
            palabra = palabra.upper().replace(' ', '')
            if len(palabra) == 0:
                continue
                
            colocada = False
            intentos = 0
            
            while not colocada and intentos < 200:
                intentos += 1
                direccion = random.choice(['H', 'V', 'D'])
                
                if direccion == 'H':
                    fila = random.randint(0, filas - 1)
                    col = random.randint(0, columnas - len(palabra))
                    if col >= 0 and self.puede_colocar_palabra(tablero, palabra, fila, col, 0, 1):
                        self.colocar_palabra(tablero, palabra, fila, col, 0, 1)
                        palabras_colocadas.append((palabra, pista, fila, col, 0, 1))
                        self.registrar_celdas_palabra(palabra, fila, col, 0, 1)
                        colocada = True
                
                elif direccion == 'V':
                    fila = random.randint(0, filas - len(palabra))
                    col = random.randint(0, columnas - 1)
                    if fila >= 0 and self.puede_colocar_palabra(tablero, palabra, fila, col, 1, 0):
                        self.colocar_palabra(tablero, palabra, fila, col, 1, 0)
                        palabras_colocadas.append((palabra, pista, fila, col, 1, 0))
                        self.registrar_celdas_palabra(palabra, fila, col, 1, 0)
                        colocada = True
                
                else:  # Diagonal
                    fila = random.randint(0, filas - len(palabra))
                    col = random.randint(0, columnas - len(palabra))
                    if fila >= 0 and col >= 0 and self.puede_colocar_palabra(tablero, palabra, fila, col, 1, 1):
                        self.colocar_palabra(tablero, palabra, fila, col, 1, 1)
                        palabras_colocadas.append((palabra, pista, fila, col, 1, 1))
                        self.registrar_celdas_palabra(palabra, fila, col, 1, 1)
                        colocada = True
        
        # Llenar espacios vacíos con letras aleatorias
        letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in range(filas):
            for j in range(columnas):
                if tablero[i][j] == '':
                    tablero[i][j] = random.choice(letras)
        
        return tablero, palabras_colocadas
    
    def registrar_celdas_palabra(self, palabra, fila, col, df, dc):
        """Registra qué celdas pertenecen a cada palabra"""
        for i in range(len(palabra)):
            f = fila + i * df
            c = col + i * dc
            celda = (f, c)
            
            if celda not in self.celdas_palabras:
                self.celdas_palabras[celda] = []
            
            if palabra not in self.celdas_palabras[celda]:
                self.celdas_palabras[celda].append(palabra)
    
    def puede_colocar_palabra(self, tablero, palabra, fila, col, df, dc):
        """Verifica si se puede colocar una palabra en la posición dada"""
        for i, letra in enumerate(palabra):
            f = fila + i * df
            c = col + i * dc
            if f < 0 or f >= len(tablero) or c < 0 or c >= len(tablero[0]):
                return False
            if tablero[f][c] != '' and tablero[f][c] != letra:
                return False
        return True
    
    def colocar_palabra(self, tablero, palabra, fila, col, df, dc):
        """Coloca una palabra en el tablero"""
        for i, letra in enumerate(palabra):
            f = fila + i * df
            c = col + i * dc
            tablero[f][c] = letra
    
    def jugar_sopa_letras(self, categoria, palabras_data, filas, columnas):
        """Pantalla principal del juego"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Sopa de Letras - Jugando")
        self.root.geometry("1100x750")  # Un poco más ancho para los botones
        self.root.configure(bg='#34495E')
        
        # Crear tablero
        self.tablero, self.palabras_info = self.crear_tablero(filas, columnas, palabras_data)
        self.palabras_encontradas = []
        self.seleccion_actual = []
        self.puntaje = 0
        self.tiempo_inicio = datetime.datetime.now()
        self.juego_activo = True
        
        # Frame principal
        main = tk.Frame(self.root, bg='#34495E', padx=20, pady=15)
        main.pack(fill='both', expand=True)
        
        # Header con información
        header = tk.Frame(main, bg='#34495E')
        header.pack(fill='x', pady=10)
        
        tk.Label(header, text=f"🔤 {categoria.upper()}", 
                font=("Arial", 16, "bold"), bg='#34495E', fg='white').pack(side='left')
        
        self.label_puntaje = tk.Label(header, text=f"⭐ Puntaje: {self.puntaje}", 
                font=("Arial", 12, "bold"), bg='#34495E', fg='#F1C40F')
        self.label_puntaje.pack(side='right', padx=10)
        
        self.label_encontradas = tk.Label(header, 
                text=f"✓ Encontradas: {len(self.palabras_encontradas)}/{len(self.palabras_info)}", 
                font=("Arial", 12), bg='#34495E', fg='#2ECC71')
        self.label_encontradas.pack(side='right')
        
        # Frame contenedor horizontal PRINCIPAL
        contenedor_principal = tk.Frame(main, bg='#34495E')
        contenedor_principal.pack(fill='both', expand=True, pady=10)
        
        # Panel izquierdo - Lista de palabras
        frame_palabras = tk.Frame(contenedor_principal, bg='#2C3E50', relief='ridge', bd=2)
        frame_palabras.pack(side='left', fill='both', padx=(0, 10), pady=5)
        
        tk.Label(frame_palabras, text="📋 PALABRAS A BUSCAR", 
                font=("Arial", 12, "bold"), bg='#2C3E50', fg='white', pady=10).pack()
        
        # Canvas para scroll de palabras
        canvas_palabras = tk.Canvas(frame_palabras, bg='#2C3E50', width=250, height=500, highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_palabras, orient="vertical", command=canvas_palabras.yview)
        frame_lista = tk.Frame(canvas_palabras, bg='#2C3E50')
        
        frame_lista.bind("<Configure>", lambda e: canvas_palabras.configure(scrollregion=canvas_palabras.bbox("all")))
        canvas_palabras.create_window((0, 0), window=frame_lista, anchor="nw")
        canvas_palabras.configure(yscrollcommand=scrollbar.set)
        
        canvas_palabras.pack(side="left", fill="both", expand=True, padx=5)
        scrollbar.pack(side="right", fill="y")
        
        self.labels_palabras = {}
        for palabra, pista, _, _, _, _ in self.palabras_info:
            frame_palabra = tk.Frame(frame_lista, bg='#34495E', relief='solid', bd=1)
            frame_palabra.pack(fill='x', padx=10, pady=5)
            
            label = tk.Label(frame_palabra, text=f"• {palabra}", 
                           font=("Arial", 11, "bold"), bg='#34495E', fg='white', 
                           anchor='w', padx=10, pady=5)
            label.pack(fill='x')
            
            tk.Label(frame_palabra, text=f"  {pista}", 
                    font=("Arial", 9), bg='#34495E', fg='#BDC3C7',
                    anchor='w', padx=10, pady=2).pack(fill='x')
            
            self.labels_palabras[palabra] = label
        
        # Panel CENTRAL - Tablero
        frame_central = tk.Frame(contenedor_principal, bg='#34495E')
        frame_central.pack(side='left', fill='both', expand=True)
        
        # Frame para el tablero
        frame_tablero = tk.Frame(frame_central, bg='#34495E')
        frame_tablero.pack(fill='both', expand=True)
        
        # Crear botones del tablero
        self.botones_tablero = []
        tamano_celda = 2
        
        for i in range(filas):
            fila_botones = []
            for j in range(columnas):
                btn = tk.Button(frame_tablero, text=self.tablero[i][j],
                              font=("Arial", 8, "bold"), bg='#ECF0F1', fg='#2C3E50',
                              width=tamano_celda, height=1,
                              relief='raised', bd=1,
                              command=lambda f=i, c=j: self.seleccionar_celda(f, c))
                btn.grid(row=i, column=j, padx=1, pady=1)
                fila_botones.append(btn)
            self.botones_tablero.append(fila_botones)
        
        # Panel DERECHO - Botones de control VERTICALES
        frame_botones_derecha = tk.Frame(contenedor_principal, bg='#34495E', width=200)
        frame_botones_derecha.pack(side='left', fill='y', padx=(20, 0))
        frame_botones_derecha.pack_propagate(False)  # Mantener el ancho fijo
        
        # Título para los botones
        tk.Label(frame_botones_derecha, text="CONTROLES", 
                font=("Arial", 14, "bold"), bg='#34495E', fg='white',
                pady=15).pack()
        
        # Botones VERTICALES - GRANDES y bien espaciados
        btn_reintentar = tk.Button(frame_botones_derecha, text="🔄 REINTENTAR", 
                 font=("Arial", 12, "bold"), bg='#E67E22', fg='white',
                 width=18, height=3,  # Tamaño fijo grande
                 cursor='hand2',
                 command=lambda: self.jugar_sopa_letras(categoria, palabras_data, filas, columnas))
        btn_reintentar.pack(pady=15)  # Espacio generoso entre botones
        
        btn_rendirse = tk.Button(frame_botones_derecha, text="🏳️  RENDIRSE", 
                 font=("Arial", 12, "bold"), bg='#E74C3C', fg='white',
                 width=18, height=3,  # Tamaño fijo grande
                 cursor='hand2',
                 command=self.rendirse)
        btn_rendirse.pack(pady=15)  # Espacio generoso entre botones
        
        btn_menu = tk.Button(frame_botones_derecha, text="🏠 MENÚ PRINCIPAL", 
                 font=("Arial", 12, "bold"), bg='#95A5A6', fg='white',
                 width=18, height=3,  # Tamaño fijo grande
                 cursor='hand2',
                 command=self.salir_al_menu)
        btn_menu.pack(pady=15)  # Espacio generoso entre botones
        
        # Espacio vacío para equilibrar
        tk.Frame(frame_botones_derecha, bg='#34495E', height=20).pack()
    
    def seleccionar_celda(self, fila, col):
        """Maneja la selección de celdas en el tablero"""
        if not self.juego_activo:
            return  # No permitir selección si el juego terminó
            
        celda = (fila, col)
        
        # Si la celda ya está seleccionada, deseleccionar
        if celda in self.seleccion_actual:
            self.seleccion_actual.remove(celda)
            self.actualizar_color_celda(fila, col)
        else:
            # Siempre permitir seleccionar (las casillas compartidas son válidas)
            self.seleccion_actual.append(celda)
            self.botones_tablero[fila][col].config(bg='#3498DB', relief='sunken')
        
        # Verificar si forma una palabra
        if len(self.seleccion_actual) >= 3:
            self.verificar_palabra()
    
    def actualizar_color_celda(self, fila, col):
        """Actualiza el color de una celda basado en su estado"""
        celda = (fila, col)
        
        # Verificar si esta celda pertenece a palabras encontradas
        palabras_en_celda = self.celdas_palabras.get(celda, [])
        palabras_encontradas_en_celda = [p for p in palabras_en_celda if p in self.palabras_encontradas]
        
        if palabras_encontradas_en_celda:
            # Celda pertenece a al menos una palabra encontrada - color verde
            self.botones_tablero[fila][col].config(bg='#2ECC71', fg='white', relief='raised')
        else:
            # Celda normal
            self.botones_tablero[fila][col].config(bg='#ECF0F1', fg='#2C3E50', relief='raised')
    
    def verificar_palabra(self):
        """Verifica si la selección actual forma una palabra válida"""
        if len(self.seleccion_actual) < 3:
            return
        
        # Obtener palabra de la selección
        palabra_seleccionada = ''.join([self.tablero[f][c] for f, c in self.seleccion_actual])
        
        # Verificar si es una palabra válida y en la dirección correcta
        for palabra, pista, fila, col, df, dc in self.palabras_info:
            if palabra in self.palabras_encontradas:
                continue
            
            # Generar coordenadas de la palabra
            coords_palabra = [(fila + i*df, col + i*dc) for i in range(len(palabra))]
            
            # Verificar si coincide (en cualquier dirección)
            if (sorted(self.seleccion_actual) == sorted(coords_palabra) or
                sorted(self.seleccion_actual) == sorted(coords_palabra[::-1])):
                
                # ¡Palabra encontrada!
                self.palabras_encontradas.append(palabra)
                self.puntaje += len(palabra) * 10
                
                # Actualizar interfaz
                self.marcar_palabra_encontrada(palabra)
                self.limpiar_seleccion()
                self.actualizar_estadisticas()
                
                # Verificar si ganó
                if len(self.palabras_encontradas) == len(self.palabras_info):
                    self.juego_completado()
                return
    
    def marcar_palabra_encontrada(self, palabra):
        """Marca visualmente una palabra encontrada"""
        # Actualizar colores de todas las celdas del tablero
        for i in range(len(self.botones_tablero)):
            for j in range(len(self.botones_tablero[0])):
                self.actualizar_color_celda(i, j)
        
        # Tachar palabra en la lista
        if palabra in self.labels_palabras:
            self.labels_palabras[palabra].config(fg='#95A5A6', 
                                                font=("Arial", 11, "bold", "overstrike"))
    
    def limpiar_seleccion(self):
        """Limpia la selección actual"""
        for fila, col in self.seleccion_actual:
            self.actualizar_color_celda(fila, col)
        self.seleccion_actual = []
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas del juego"""
        self.label_puntaje.config(text=f"⭐ Puntaje: {self.puntaje}")
        self.label_encontradas.config(
            text=f"✓ Encontradas: {len(self.palabras_encontradas)}/{len(self.palabras_info)}"
        )
    
    def rendirse(self):
        """Maneja la acción de rendirse"""
        if not self.juego_activo:
            return
            
        respuesta = messagebox.askyesno(
            "¿Rendirse?",
            "¿Estás seguro de que quieres rendirte?\n\nSe revelarán todas las palabras y perderás el juego."
        )
        
        if respuesta:
            self.juego_activo = False
            
            # GUARDAR el número real de palabras encontradas ANTES de revelar todo
            palabras_encontradas_reales = len(self.palabras_encontradas)
            
            # Mostrar todas las palabras en rojo
            self.mostrar_todas_las_palabras()
            
            # Mostrar mensaje con el número REAL de palabras encontradas
            messagebox.showinfo(
                "Te has rendido",
                f"Juego terminado.\nPalabras encontradas: {palabras_encontradas_reales}/{len(self.palabras_info)}\nPuntaje final: {self.puntaje}"
            )
            self.mostrar_configuracion()
    
    def mostrar_todas_las_palabras(self):
        """Muestra todas las palabras en color rojo cuando el jugador se rinde"""
        for palabra, pista, fila, col, df, dc in self.palabras_info:
            if palabra not in self.palabras_encontradas:
                # NO agregar a palabras_encontradas, solo mostrar visualmente
                # self.palabras_encontradas.append(palabra)  # ← ESTA LÍNEA ES EL PROBLEMA
                
                # Marcar todas las celdas de esta palabra en ROJO
                for i in range(len(palabra)):
                    f = fila + i * df
                    c = col + i * dc
                    self.botones_tablero[f][c].config(bg='#E74C3C', fg='white')  # Rojo
                
                # Tachar palabra en la lista en ROJO (pero sin contarla como encontrada)
                if palabra in self.labels_palabras:
                    self.labels_palabras[palabra].config(fg='#E74C3C', 
                                                        font=("Arial", 11, "bold", "overstrike"))
    
    def salir_al_menu(self):
        """Maneja la acción de salir al menú principal"""
        if not self.juego_activo:
            self.volver_menu_principal()
            return
            
        respuesta = messagebox.askyesno(
            "Salir al Menú Principal",
            "¿Estás seguro de que quieres salir al menú principal?\n\n⚠️ PERDERÁS TODO TU PROGRESO ACTUAL DE ESTA PARTIDA."
        )
        
        if respuesta:
            self.volver_menu_principal()
    
    def mostrar_todas_las_palabras(self):
        """Muestra todas las palabras en color rojo cuando el jugador se rinde"""
        for palabra, pista, fila, col, df, dc in self.palabras_info:
            if palabra not in self.palabras_encontradas:
                # Marcar esta palabra como encontrada (pero por rendición)
                self.palabras_encontradas.append(palabra)
                
                # Marcar todas las celdas de esta palabra en ROJO
                for i in range(len(palabra)):
                    f = fila + i * df
                    c = col + i * dc
                    self.botones_tablero[f][c].config(bg='#E74C3C', fg='white')  # Rojo
                
                # Tachar palabra en la lista
                if palabra in self.labels_palabras:
                    self.labels_palabras[palabra].config(fg='#E74C3C', 
                                                        font=("Arial", 11, "bold", "overstrike"))
    
    def juego_completado(self):
        """Maneja el final del juego por victoria"""
        self.juego_activo = False
        tiempo_final = datetime.datetime.now()
        tiempo_transcurrido = (tiempo_final - self.tiempo_inicio).seconds
        
        # Bonus por tiempo
        bonus_tiempo = max(0, 600 - tiempo_transcurrido) * 2
        puntaje_final = self.puntaje + bonus_tiempo
        
        # Guardar puntaje (si la BD está disponible)
        if app_manager.auth and app_manager.auth.usuario_actual and app_manager.database:
            try:
                usuario_id = app_manager.database.obtener_id_usuario(app_manager.auth.usuario_actual)
                if usuario_id:
                    app_manager.database.guardar_puntaje(
                        usuario_id, 
                        "Sopa de Letras", 
                        puntaje_final,
                        dificultad="20x20",
                        categoria=self.categoria_actual
                    )
            except Exception as e:
                print(f"Error guardando puntaje: {e}")
        
        # Mostrar mensaje de victoria
        mensaje = f"🎉 ¡FELICITACIONES! 🎉\n\n"
        mensaje += f"Completaste el juego en {tiempo_transcurrido} segundos\n\n"
        mensaje += f"Puntaje base: {self.puntaje}\n"
        mensaje += f"Bonus por tiempo: +{bonus_tiempo}\n"
        mensaje += f"━━━━━━━━━━━━━━━━━━━\n"
        mensaje += f"PUNTAJE FINAL: {puntaje_final} ⭐"
        
        messagebox.showinfo("¡Victoria!", mensaje)
        self.mostrar_configuracion()

    def volver_menu_principal(self):
        """Vuelve al menú principal"""
        try:
            from menu_principal import MenuPrincipal
            for widget in self.root.winfo_children():
                widget.destroy()
            MenuPrincipal(self.root, app_manager.auth, app_manager.database)
        except Exception as e:
            print(f"Error volviendo al menú: {e}")
            for widget in self.root.winfo_children():
                widget.destroy()
            tk.Label(self.root, text="Error al volver al menú", 
                    font=("Arial", 14), bg='#2C3E50', fg='white').pack(expand=True)