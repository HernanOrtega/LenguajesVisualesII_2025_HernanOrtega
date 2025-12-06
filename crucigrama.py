# crucigrama.py 
import tkinter as tk
from tkinter import messagebox
import datetime
import random
import sys
import os

# Añadir el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Crucigrama:
    def __init__(self, root, auth=None, database=None):
        self.root = root
        self.auth = auth  # Referencia al sistema de autenticación
        self.database = database  # Referencia a la base de datos
        
        self.tablero = []
        self.celdas = []
        self.definiciones = []
        self.palabras_info = []
        self.numeros_palabras = {}
        self.categoria_actual = None
        self.tiempo_inicio = None
        self.puntaje = 0
        self.juego_activo = True
        self.palabras_completadas = set()
        self.bindings_mousewheel = []  # Para trackear bindings y limpiarlos
        
        # Datos de crucigramas por categoría
        self.crucigramas_data = self.obtener_crucigramas_integrados()
        
        # Verificar conexión con la base de datos
        self.verificar_conexion_bd()
        
        self.mostrar_menu_principal()

    def verificar_conexion_bd(self):
        """Verifica la conexión con la base de datos"""
        print("=" * 50)
        print("Verificando conexión con base de datos...")
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
            try:
                conexion = self.database.get_conexion()
                cursor = conexion.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tablas = cursor.fetchall()
                print(f"✓ Tablas en la BD: {[t[0] for t in tablas]}")
                conexion.close()
            except Exception as e:
                print(f"❌ Error al verificar BD: {e}")
        else:
            print("⚠️ Database no configurado")
        print("=" * 50)

    def limpiar_bindings_mousewheel(self):
        """Limpia todos los bindings del mousewheel para prevenir errores"""
        for binding_id in self.bindings_mousewheel:
            try:
                self.root.unbind_all(binding_id)
            except:
                pass
        self.bindings_mousewheel = []

    def obtener_crucigramas_integrados(self):
        """Devuelve todos los crucigramas integrados"""
        return {
            1: {
                'nombre': 'Lenguajes de Programación',
                'descripcion': 'Lenguajes y términos de programación',
                'filas': 15,
                'columnas': 15,
                'palabras': [
                    {'palabra': 'PYTHON', 'definicion': 'Lenguaje interpretado de alto nivel', 'fila': 2, 'columna': 2, 'direccion': 'H', 'numero': 1},
                    {'palabra': 'JAVASCRIPT', 'definicion': 'Lenguaje para desarrollo web', 'fila': 1, 'columna': 12, 'direccion': 'V', 'numero': 2},
                    {'palabra': 'HTML', 'definicion': 'Lenguaje de marcado web', 'fila': 4, 'columna': 2, 'direccion': 'H', 'numero': 3},
                    {'palabra': 'CSS', 'definicion': 'Hojas de estilo en cascada', 'fila': 1, 'columna': 13, 'direccion': 'V', 'numero': 4},
                    {'palabra': 'JAVA', 'definicion': 'Lenguaje orientado a objetos', 'fila': 6, 'columna': 2, 'direccion': 'H', 'numero': 5},
                    {'palabra': 'RUBY', 'definicion': 'Lenguaje de programación dinámico', 'fila': 1, 'columna': 14, 'direccion': 'V', 'numero': 6},
                    {'palabra': 'SWIFT', 'definicion': 'Lenguaje para desarrollo iOS', 'fila': 8, 'columna': 2, 'direccion': 'H', 'numero': 7},
                    {'palabra': 'KOTLIN', 'definicion': 'Lenguaje para desarrollo Android', 'fila': 1, 'columna': 15, 'direccion': 'V', 'numero': 8},
                    {'palabra': 'PHP', 'definicion': 'Lenguaje para desarrollo web backend', 'fila': 10, 'columna': 2, 'direccion': 'H', 'numero': 9},
                    {'palabra': 'SQL', 'definicion': 'Lenguaje de consulta de bases de datos', 'fila': 1, 'columna': 11, 'direccion': 'V', 'numero': 10}
                ]
            },
            2: {
                'nombre': 'Ciencia',
                'descripcion': 'Términos científicos',
                'filas': 15,
                'columnas': 15,
                'palabras': [
                    {'palabra': 'ATOMO', 'definicion': 'Unidad básica de la materia', 'fila': 2, 'columna': 2, 'direccion': 'H', 'numero': 1},
                    {'palabra': 'MOLECULA', 'definicion': 'Conjunto de átomos enlazados', 'fila': 1, 'columna': 12, 'direccion': 'V', 'numero': 2},
                    {'palabra': 'ADN', 'definicion': 'Material genético de los seres vivos', 'fila': 4, 'columna': 2, 'direccion': 'H', 'numero': 3},
                    {'palabra': 'CELULA', 'definicion': 'Unidad básica de los organismos', 'fila': 1, 'columna': 13, 'direccion': 'V', 'numero': 4},
                    {'palabra': 'GRAVEDAD', 'definicion': 'Fuerza de atracción entre masas', 'fila': 6, 'columna': 2, 'direccion': 'H', 'numero': 5},
                    {'palabra': 'ENERGIA', 'definicion': 'Capacidad para realizar trabajo', 'fila': 1, 'columna': 14, 'direccion': 'V', 'numero': 6},
                    {'palabra': 'QUANTUM', 'definicion': 'Teoría física de partículas', 'fila': 8, 'columna': 2, 'direccion': 'H', 'numero': 7},
                    {'palabra': 'ECOSISTEMA', 'definicion': 'Comunidad de organismos vivos', 'fila': 1, 'columna': 15, 'direccion': 'V', 'numero': 8},
                    {'palabra': 'EVOLUCION', 'definicion': 'Desarrollo de especies en el tiempo', 'fila': 10, 'columna': 2, 'direccion': 'H', 'numero': 9},
                    {'palabra': 'GENOMA', 'definicion': 'Conjunto completo de genes', 'fila': 1, 'columna': 11, 'direccion': 'V', 'numero': 10}
                ]
            },
            3: {
                'nombre': 'Arte',
                'descripcion': 'Términos artísticos',
                'filas': 15,
                'columnas': 15,
                'palabras': [
                    {'palabra': 'PINTURA', 'definicion': 'Arte de aplicar colores sobre superficies', 'fila': 2, 'columna': 2, 'direccion': 'H', 'numero': 1},
                    {'palabra': 'ESCULTURA', 'definicion': 'Arte de crear formas tridimensionales', 'fila': 1, 'columna': 12, 'direccion': 'V', 'numero': 2},
                    {'palabra': 'MUSICA', 'definicion': 'Arte de combinar sonidos armónicamente', 'fila': 4, 'columna': 2, 'direccion': 'H', 'numero': 3},
                    {'palabra': 'DANZA', 'definicion': 'Arte del movimiento corporal rítmico', 'fila': 1, 'columna': 13, 'direccion': 'V', 'numero': 4},
                    {'palabra': 'TEATRO', 'definicion': 'Arte escénico de representación dramática', 'fila': 6, 'columna': 2, 'direccion': 'H', 'numero': 5},
                    {'palabra': 'LITERATURA', 'definicion': 'Arte de la expresión escrita', 'fila': 1, 'columna': 14, 'direccion': 'V', 'numero': 6},
                    {'palabra': 'CINE', 'definicion': 'Arte cinematográfico', 'fila': 8, 'columna': 2, 'direccion': 'H', 'numero': 7},
                    {'palabra': 'FOTOGRAFIA', 'definicion': 'Arte de capturar imágenes con luz', 'fila': 1, 'columna': 15, 'direccion': 'V', 'numero': 8},
                    {'palabra': 'ARQUITECTURA', 'definicion': 'Arte de diseñar edificios', 'fila': 10, 'columna': 2, 'direccion': 'H', 'numero': 9},
                    {'palabra': 'DIBUJO', 'definicion': 'Arte de representar gráficamente', 'fila': 1, 'columna': 11, 'direccion': 'V', 'numero': 10}
                ]
            },
            4: {
                'nombre': 'Deportes',
                'descripcion': 'Deportes y términos deportivos',
                'filas': 15,
                'columnas': 15,
                'palabras': [
                    {'palabra': 'FUTBOL', 'definicion': 'Deporte de equipo con balón', 'fila': 2, 'columna': 2, 'direccion': 'H', 'numero': 1},
                    {'palabra': 'BALONCESTO', 'definicion': 'Deporte con canasta y balón', 'fila': 1, 'columna': 12, 'direccion': 'V', 'numero': 2},
                    {'palabra': 'TENIS', 'definicion': 'Deporte con raqueta y pelota', 'fila': 4, 'columna': 2, 'direccion': 'H', 'numero': 3},
                    {'palabra': 'NATACION', 'definicion': 'Deporte acuático', 'fila': 1, 'columna': 13, 'direccion': 'V', 'numero': 4},
                    {'palabra': 'ATLETISMO', 'definicion': 'Conjunto de deportes de pista', 'fila': 6, 'columna': 2, 'direccion': 'H', 'numero': 5},
                    {'palabra': 'CICLISMO', 'definicion': 'Deporte con bicicleta', 'fila': 1, 'columna': 14, 'direccion': 'V', 'numero': 6},
                    {'palabra': 'VOLEIBOL', 'definicion': 'Deporte con red y pelota', 'fila': 8, 'columna': 2, 'direccion': 'H', 'numero': 7},
                    {'palabra': 'RUGBY', 'definicion': 'Deporte de contacto con balón oval', 'fila': 1, 'columna': 15, 'direccion': 'V', 'numero': 8},
                    {'palabra': 'GIMNASIA', 'definicion': 'Deporte de ejercicios físicos', 'fila': 10, 'columna': 2, 'direccion': 'H', 'numero': 9},
                    {'palabra': 'JUDO', 'definicion': 'Arte marcial japonés', 'fila': 1, 'columna': 11, 'direccion': 'V', 'numero': 10}
                ]
            },
            5: {
                'nombre': 'Geografía',
                'descripcion': 'Términos geográficos',
                'filas': 15,
                'columnas': 15,
                'palabras': [
                    {'palabra': 'CONTINENTE', 'definicion': 'Gran extensión de tierra', 'fila': 2, 'columna': 2, 'direccion': 'H', 'numero': 1},
                    {'palabra': 'OCEANO', 'definicion': 'Gran masa de agua salada', 'fila': 1, 'columna': 12, 'direccion': 'V', 'numero': 2},
                    {'palabra': 'MONTAÑA', 'definicion': 'Elevación natural del terreno', 'fila': 4, 'columna': 2, 'direccion': 'H', 'numero': 3},
                    {'palabra': 'RIO', 'definicion': 'Corriente natural de agua', 'fila': 1, 'columna': 13, 'direccion': 'V', 'numero': 4},
                    {'palabra': 'DESIERTO', 'definicion': 'Zona árida con poca vegetación', 'fila': 6, 'columna': 2, 'direccion': 'H', 'numero': 5},
                    {'palabra': 'VOLCAN', 'definicion': 'Abertura en la corteza terrestre', 'fila': 1, 'columna': 14, 'direccion': 'V', 'numero': 6},
                    {'palabra': 'ISLA', 'definicion': 'Porción de tierra rodeada de agua', 'fila': 8, 'columna': 2, 'direccion': 'H', 'numero': 7},
                    {'palabra': 'LAGO', 'definicion': 'Cuerpo de agua dulce', 'fila': 1, 'columna': 15, 'direccion': 'V', 'numero': 8},
                    {'palabra': 'SELVA', 'definicion': 'Bosque tropical denso', 'fila': 10, 'columna': 2, 'direccion': 'H', 'numero': 9},
                    {'palabra': 'GLACIAR', 'definicion': 'Masa de hielo en movimiento', 'fila': 1, 'columna': 11, 'direccion': 'V', 'numero': 10}
                ]
            }
        }

    def mostrar_menu_principal(self):
        """Muestra el menú principal"""
        print("Mostrando menú principal...")
        
        # Limpiar bindings del mousewheel
        self.limpiar_bindings_mousewheel()
        
        # Limpiar todo
        for w in self.root.winfo_children():
            w.destroy()
        
        self.root.title("Crucigrama - Menú Principal")
        self.root.geometry("900x650")
        self.root.configure(bg='#2C3E50')
        
        # Frame principal centrado
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(expand=True, fill='both', padx=80, pady=40)
        
        # Título centrado
        title_frame = tk.Frame(main_frame, bg='#2C3E50')
        title_frame.pack(pady=(0, 20))
        
        tk.Label(title_frame, text="🧩 CRUCIGRAMA 🧩", 
                font=("Arial", 28, "bold"), bg='#2C3E50', fg='white').pack()
        
        tk.Label(title_frame, text="Selecciona una categoría:", 
                font=("Arial", 16), bg='#2C3E50', fg='white').pack(pady=10)
        
        # Información del usuario
        if self.auth and self.auth.usuario_actual:
            tk.Label(title_frame, text=f"👤 Jugando como: {self.auth.usuario_actual}", 
                    font=("Arial", 12, "bold"), bg='#2C3E50', fg='#2ECC71').pack(pady=5)
        else:
            tk.Label(title_frame, text="⚠️ No autenticado - Los puntajes no se guardarán", 
                    font=("Arial", 10), bg='#2C3E50', fg='#E74C3C').pack(pady=5)
        
        # Contenedor principal para categorías con scrollbar
        categories_container = tk.Frame(main_frame, bg='#2C3E50')
        categories_container.pack(fill='both', expand=True)
        
        scroll_frame = tk.Frame(categories_container, bg='#2C3E50')
        scroll_frame.pack(expand=True, fill='both')
        
        # Canvas con scrollbar
        canvas = tk.Canvas(scroll_frame, bg='#2C3E50', highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", 
                               command=canvas.yview, 
                               bg='#34495E', 
                               troughcolor='#2C3E50',
                               activebackground='#2980B9',
                               width=12)
        
        scrollable_frame = tk.Frame(canvas, bg='#2C3E50')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((canvas.winfo_reqwidth()//2, 0), 
                           window=scrollable_frame, 
                           anchor="n", 
                           width=canvas.winfo_reqwidth())
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(0, 5))
        scrollbar.pack(side="right", fill="y", padx=(5, 0))
        
        # Guardar binding para limpiarlo después
        binding_id = "<MouseWheel>"
        self.bindings_mousewheel.append(binding_id)
        
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        inner_container = tk.Frame(scrollable_frame, bg='#2C3E50')
        inner_container.pack(expand=True, fill='both', padx=50)
        
        # Botones de categorías
        for cat_id, data in self.crucigramas_data.items():
            cat_frame = tk.Frame(inner_container, bg='#34495E', relief='raised', bd=2)
            cat_frame.pack(fill='x', pady=12, padx=80)
            
            content_frame = tk.Frame(cat_frame, bg='#34495E')
            content_frame.pack(fill='x', padx=20, pady=15)
            
            info_frame = tk.Frame(content_frame, bg='#34495E')
            info_frame.pack(side='left', fill='both', expand=True)
            
            tk.Label(info_frame, text=data['nombre'], 
                    font=("Arial", 16, "bold"), bg='#34495E', fg='white').pack(anchor='w')
            
            tk.Label(info_frame, text=data['descripcion'], 
                    font=("Arial", 11), bg='#34495E', fg='#BDC3C7',
                    anchor='w', wraplength=400).pack(anchor='w', pady=(5, 0))
            
            meta_frame = tk.Frame(info_frame, bg='#34495E')
            meta_frame.pack(anchor='w', pady=(8, 0))
            
            tk.Label(meta_frame, 
                    text=f"• Palabras: {len(data['palabras'])}", 
                    font=("Arial", 10), bg='#34495E', fg='#95A5A6').pack(side='left', padx=(0, 15))
            
            tk.Label(meta_frame, 
                    text=f"• Tamaño: {data['filas']}x{data['columnas']}", 
                    font=("Arial", 10), bg='#34495E', fg='#95A5A6').pack(side='left')
            
            btn_frame = tk.Frame(content_frame, bg='#34495E')
            btn_frame.pack(side='right', padx=(20, 0))
            
            btn = tk.Button(btn_frame, text="JUGAR", 
                           font=("Arial", 12, "bold"), bg='#27AE60', fg='white',
                           width=10, height=2, cursor='hand2',
                           relief='raised', bd=3,
                           command=lambda x=cat_id: self.iniciar_juego(x))
            btn.pack()
        
        def configure_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas.find_all()[0], width=event.width)
        
        canvas.bind('<Configure>', configure_canvas)
        
        # Botón salir
        bottom_frame = tk.Frame(main_frame, bg='#2C3E50')
        bottom_frame.pack(pady=30)
        
        tk.Button(bottom_frame, text="VOLVER AL MENÚ PRINCIPAL", 
                 font=("Arial", 12, "bold"), bg='#95A5A6', fg='white',
                 width=25, height=2, command=self.volver_menu_principal,
                 relief='raised', bd=2, cursor='hand2').pack()

    def iniciar_juego(self, cat_id):
        """Inicia el juego con la categoría seleccionada"""
        print(f"Iniciando juego categoría {cat_id}")
        
        if cat_id not in self.crucigramas_data:
            messagebox.showerror("Error", f"Categoría {cat_id} no existe")
            return
        
        self.categoria_actual = cat_id
        crucigrama = self.crucigramas_data[cat_id]
        self.crear_pantalla_juego(crucigrama)

    def crear_pantalla_juego(self, crucigrama):
        """Crea la pantalla de juego"""
        print(f"Creando juego: {crucigrama['nombre']}")
        
        # Limpiar bindings del mousewheel
        self.limpiar_bindings_mousewheel()
        
        # Limpiar
        for w in self.root.winfo_children():
            w.destroy()
        
        self.root.title(f"Crucigrama - {crucigrama['nombre']}")
        self.root.geometry("1400x800")
        self.root.configure(bg='#34495E')
        
        # Variables de juego
        self.crucigrama_actual = crucigrama
        self.palabras_ok = 0
        self.puntaje = 0
        self.tiempo_inicio = datetime.datetime.now()
        self.juego_activo = True
        self.palabras_completadas = set()
        
        # Header
        header = tk.Frame(self.root, bg='#34495E')
        header.pack(fill='x', padx=20, pady=10)
        
        tk.Label(header, text=crucigrama['nombre'], 
                font=("Arial", 18, "bold"), bg='#34495E', fg='white').pack(side='left')
        
        self.lbl_puntaje = tk.Label(header, text="Puntaje: 0", 
                                    font=("Arial", 14, "bold"), bg='#34495E', fg='#F1C40F')
        self.lbl_puntaje.pack(side='right', padx=15)
        
        self.lbl_completado = tk.Label(header, 
                                      text=f"Completado: 0/{len(crucigrama['palabras'])}", 
                                      font=("Arial", 14), bg='#34495E', fg='#2ECC71')
        self.lbl_completado.pack(side='right', padx=15)
        
        # Contenedor principal
        container = tk.Frame(self.root, bg='#34495E')
        container.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Panel izquierdo - Definiciones
        panel_def = tk.Frame(container, bg='#2C3E50', width=350, relief='ridge', bd=2)
        panel_def.pack(side='left', fill='both', padx=(0, 10))
        panel_def.pack_propagate(False)
        
        tk.Label(panel_def, text="DEFINICIONES", 
                font=("Arial", 14, "bold"), bg='#2C3E50', fg='white', pady=15).pack()
        
        # Frame scrollable para definiciones
        def_canvas = tk.Canvas(panel_def, bg='#2C3E50', highlightthickness=0)
        def_scrollbar = tk.Scrollbar(panel_def, orient="vertical", command=def_canvas.yview,
                                     bg='#34495E', troughcolor='#2C3E50',
                                     activebackground='#2980B9', width=12)
        def_content = tk.Frame(def_canvas, bg='#2C3E50')
        
        # Configurar el scroll correctamente
        def_canvas.create_window((0, 0), window=def_content, anchor="nw", width=330)
        
        # Crear las definiciones
        for palabra_info in crucigrama['palabras']:
            f = tk.Frame(def_content, bg='#34495E', relief='solid', bd=1)
            f.pack(fill='x', padx=10, pady=6)
            
            dir_txt = "→" if palabra_info['direccion'] == 'H' else "↓"
            tk.Label(f, text=f"{palabra_info['numero']}. {dir_txt} ({len(palabra_info['palabra'])} letras)", 
                    font=("Arial", 11, "bold"), bg='#34495E', fg='#F39C12',
                    anchor='w', padx=10, pady=4).pack(fill='x')
            
            tk.Label(f, text=palabra_info['definicion'], 
                    font=("Arial", 10), bg='#34495E', fg='white',
                    anchor='w', justify='left', wraplength=290, padx=10, pady=4).pack(fill='x')
        
        # Actualizar la región scrollable después de crear todo el contenido
        def_content.update_idletasks()
        def_canvas.configure(scrollregion=def_canvas.bbox("all"), yscrollcommand=def_scrollbar.set)
        
        # Habilitar scroll con la rueda del mouse (con corrección de error)
        def on_mousewheel(event):
            try:
                def_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except Exception as e:
                print(f"Error en scroll: {e}")
        
        # Guardar binding para limpiarlo después
        binding_id = "<MouseWheel>"
        self.bindings_mousewheel.append(binding_id)
        def_canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Pack canvas y scrollbar
        def_scrollbar.pack(side="right", fill="y", padx=(0, 5))
        def_canvas.pack(side="left", fill="both", expand=True, padx=(8, 3), pady=8)
        
        # Panel central - Tablero con scroll
        panel_tablero = tk.Frame(container, bg='#34495E')
        panel_tablero.pack(side='left', fill='both', expand=True)
        
        self.crear_tablero(panel_tablero, crucigrama)
        
        # Panel derecho - Controles (sin botón de pista)
        panel_ctrl = tk.Frame(container, bg='#34495E', width=180)
        panel_ctrl.pack(side='right', fill='y', padx=(10, 0))
        panel_ctrl.pack_propagate(False)
        
        tk.Label(panel_ctrl, text="CONTROLES", 
                font=("Arial", 13, "bold"), bg='#34495E', fg='white', pady=15).pack()
        
        tk.Button(panel_ctrl, text="✓ VERIFICAR", bg='#2ECC71', fg='white',
                 font=("Arial", 11, "bold"), width=14, height=2,
                 command=self.verificar).pack(pady=8)
        
        tk.Button(panel_ctrl, text="🗑 LIMPIAR", bg='#3498DB', fg='white',
                 font=("Arial", 11, "bold"), width=14, height=2,
                 command=self.limpiar).pack(pady=8)
        
        tk.Button(panel_ctrl, text="🏠 MENÚ", bg='#7F8C8D', fg='white',
                 font=("Arial", 11, "bold"), width=14, height=2,
                 command=self.volver_al_menu).pack(pady=8)

    def crear_tablero(self, parent, crucigrama):
        """Crea el tablero optimizado con números indicadores de palabras"""
        print("Creando tablero optimizado...")
        
        filas = crucigrama['filas']
        cols = crucigrama['columnas']
        
        # Identificar celdas activas
        celdas_activas = set()
        self.numeros = {}
        self.palabras_posiciones = {}  # Guardar info de cada palabra
        
        for p in crucigrama['palabras']:
            fila = p['fila'] - 1
            col = p['columna'] - 1
            self.numeros[(fila, col)] = p['numero']
            self.palabras_posiciones[p['numero']] = {
                'fila': fila,
                'col': col,
                'direccion': p['direccion'],
                'longitud': len(p['palabra'])
            }
            
            if p['direccion'] == 'H':
                for i in range(len(p['palabra'])):
                    if col + i < cols:
                        celdas_activas.add((fila, col + i))
            else:
                for i in range(len(p['palabra'])):
                    if fila + i < filas:
                        celdas_activas.add((fila + i, col))
        
        # Frame simple para el tablero centrado
        frame_tablero = tk.Frame(parent, bg='#34495E')
        frame_tablero.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Frame interno para centrar el grid (con offset para los números)
        inner_frame = tk.Frame(frame_tablero, bg='#34495E')
        inner_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Crear celdas y etiquetas de números
        self.celdas = []
        tam = 32  # Tamaño de celda reducido para mejor visualización
        
        # Offset más grande para garantizar espacio para TODOS los números
        offset_fila = 2
        offset_col = 2
        
        # Primero crear las etiquetas de números para cada palabra (SIEMPRE)
        for numero, info in self.palabras_posiciones.items():
            fila = info['fila'] + offset_fila
            col = info['col'] + offset_col
            direccion = info['direccion']
            
            if direccion == 'H':
                # Número a la izquierda para palabras horizontales
                label_frame = tk.Frame(inner_frame, bg='#34495E')
                label_frame.grid(row=fila, column=col-1, padx=2, pady=0, sticky='e')
                tk.Label(label_frame, text=f"{numero}→", 
                        font=("Arial", 11, "bold"), 
                        bg='#34495E', fg='#F39C12').pack()
            else:
                # Número arriba para palabras verticales
                label_frame = tk.Frame(inner_frame, bg='#34495E')
                label_frame.grid(row=fila-1, column=col, padx=0, pady=2, sticky='s')
                tk.Label(label_frame, text=f"{numero}↓", 
                        font=("Arial", 11, "bold"), 
                        bg='#34495E', fg='#3498DB').pack()
        
        # Ahora crear las celdas del crucigrama (con offset)
        for i in range(filas):
            fila_celdas = []
            for j in range(cols):
                if (i, j) in celdas_activas:
                    # Frame de celda (aplicar offset en la posición del grid)
                    f = tk.Frame(inner_frame, bg='#000000', width=tam, height=tam, 
                                relief='solid', bd=1, highlightbackground='#666666')
                    f.grid(row=i+offset_fila, column=j+offset_col, padx=0, pady=0)
                    f.grid_propagate(False)
                    
                    # Frame interno
                    inner_cell = tk.Frame(f, bg='#FFFFFF', width=tam, height=tam)
                    inner_cell.pack(fill='both', expand=True, padx=1, pady=1)
                    inner_cell.pack_propagate(False)
                    
                    # Número pequeño en esquina (para intersecciones)
                    if (i, j) in self.numeros:
                        numero_label = tk.Label(inner_cell, 
                                              text=str(self.numeros[(i, j)]), 
                                              font=("Arial", 8, "bold"),
                                              bg='#FFFFFF', fg='#E74C3C')
                        numero_label.place(x=2, y=1, anchor='nw')
                    
                    # Entry para letra
                    entry = tk.Entry(inner_cell, 
                                    font=("Arial", 14, "bold"), 
                                    bg='#FFFFFF', fg='#000000',
                                    width=1, 
                                    justify='center', 
                                    relief='flat', 
                                    bd=0,
                                    insertwidth=2,
                                    selectbackground='#3498DB')
                    entry.place(relx=0.5, rely=0.55, anchor='center', width=tam-8, height=tam-8)
                    
                    # Guardar posición para navegación
                    entry.posicion = (i, j)
                    
                    # Encontrar letra correcta
                    letra_correcta = self.encontrar_letra_correcta(i, j, crucigrama)
                    entry.letra_correcta = letra_correcta
                    
                    # Vincular eventos
                    entry.bind('<KeyRelease>', lambda e, entry=entry: self.on_letra(e, entry))
                    entry.bind('<Right>', lambda e, entry=entry: self.mover_derecha(entry))
                    entry.bind('<Left>', lambda e, entry=entry: self.mover_izquierda(entry))
                    entry.bind('<Up>', lambda e, entry=entry: self.mover_arriba(entry))
                    entry.bind('<Down>', lambda e, entry=entry: self.mover_abajo(entry))
                    
                    fila_celdas.append(entry)
                else:
                    fila_celdas.append(None)
            
            self.celdas.append(fila_celdas)
        
        print(f"Tablero creado con {len(celdas_activas)} celdas activas!")
        
        # Enfocar la primera celda
        if self.celdas and self.celdas[0]:
            for fila in self.celdas:
                for celda in fila:
                    if celda:
                        celda.focus_set()
                        return

    def encontrar_letra_correcta(self, fila, col, crucigrama):
        """Encuentra la letra correcta para una celda específica"""
        for p in crucigrama['palabras']:
            f = p['fila'] - 1
            c = p['columna'] - 1
            
            if p['direccion'] == 'H':
                if fila == f and c <= col < c + len(p['palabra']):
                    return p['palabra'][col - c]
            else:
                if col == c and f <= fila < f + len(p['palabra']):
                    return p['palabra'][fila - f]
        return ''

    def encontrar_siguiente_celda(self, fila, col):
        """Encuentra la siguiente celda activa en la dirección de la palabra"""
        # Primero, encontrar a qué palabra pertenece esta celda
        for p in self.crucigrama_actual['palabras']:
            f = p['fila'] - 1
            c = p['columna'] - 1
            
            if p['direccion'] == 'H':
                # Palabra horizontal
                if fila == f and c <= col < c + len(p['palabra']):
                    # Verificar si hay siguiente celda en esta palabra
                    next_col = col + 1
                    if next_col < c + len(p['palabra']) and next_col < len(self.celdas[0]):
                        if self.celdas[fila][next_col]:
                            return self.celdas[fila][next_col]
            else:
                # Palabra vertical
                if col == c and f <= fila < f + len(p['palabra']):
                    # Verificar si hay siguiente celda en esta palabra
                    next_fila = fila + 1
                    if next_fila < f + len(p['palabra']) and next_fila < len(self.celdas):
                        if self.celdas[next_fila][col]:
                            return self.celdas[next_fila][col]
        
        # Si no hay siguiente celda en la misma palabra, buscar cualquier celda vacía
        for i in range(len(self.celdas)):
            for j in range(len(self.celdas[0])):
                if self.celdas[i][j] and not self.celdas[i][j].get():
                    return self.celdas[i][j]
        
        return None

    def mover_derecha(self, entry):
        """Mueve el foco a la derecha"""
        fila, col = entry.posicion
        if col + 1 < len(self.celdas[0]) and self.celdas[fila][col + 1]:
            self.celdas[fila][col + 1].focus_set()
        return "break"

    def mover_izquierda(self, entry):
        """Mueve el foco a la izquierda"""
        fila, col = entry.posicion
        if col - 1 >= 0 and self.celdas[fila][col - 1]:
            self.celdas[fila][col - 1].focus_set()
        return "break"

    def mover_arriba(self, entry):
        """Mueve el foco hacia arriba"""
        fila, col = entry.posicion
        if fila - 1 >= 0 and self.celdas[fila - 1][col]:
            self.celdas[fila - 1][col].focus_set()
        return "break"

    def mover_abajo(self, entry):
        """Mueve el foco hacia abajo"""
        fila, col = entry.posicion
        if fila + 1 < len(self.celdas) and self.celdas[fila + 1][col]:
            self.celdas[fila + 1][col].focus_set()
        return "break"

    def on_letra(self, event, entry):
        """Al escribir una letra - con avance automático"""
        texto = entry.get().upper()
        
        # Solo 1 letra
        if len(texto) > 1:
            entry.delete(0, tk.END)
            entry.insert(0, texto[0] if texto else '')
            texto = entry.get()
        
        # Solo letras
        if texto and not texto.isalpha():
            entry.delete(0, tk.END)
            return "break"
        
        # Mayúscula
        if texto:
            entry.delete(0, tk.END)
            entry.insert(0, texto.upper())
            
            # Verificar
            if entry.get() == entry.letra_correcta:
                entry.config(bg='#D5F4E6', fg='#27AE60')  # Verde suave
                
                # AVANZAR A LA SIGUIENTE CELDA AUTOMÁTICAMENTE
                fila, col = entry.posicion
                siguiente_celda = self.encontrar_siguiente_celda(fila, col)
                if siguiente_celda:
                    siguiente_celda.focus_set()
                
                # Verificar palabras completadas
                self.verificar_palabras()
            else:
                entry.config(bg='#FADBD8', fg='#C0392B')  # Rojo suave
                self.root.after(300, lambda: entry.config(bg='#FFFFFF', fg='#000000'))
        
        return "break"

    def verificar_palabras(self):
        """Verifica si hay palabras completas"""
        completas = 0
        
        for p in self.crucigrama_actual['palabras']:
            fila = p['fila'] - 1
            col = p['columna'] - 1
            palabra = p['palabra']
            ok = True
            
            if p['direccion'] == 'H':
                for i in range(len(palabra)):
                    if col + i >= len(self.celdas[0]):
                        ok = False
                        break
                    celda = self.celdas[fila][col + i]
                    if not celda or celda.get() != palabra[i]:
                        ok = False
                        break
            else:
                for i in range(len(palabra)):
                    if fila + i >= len(self.celdas):
                        ok = False
                        break
                    celda = self.celdas[fila + i][col]
                    if not celda or celda.get() != palabra[i]:
                        ok = False
                        break
            
            if ok:
                completas += 1
                if p['numero'] not in self.palabras_completadas:
                    self.palabras_completadas.add(p['numero'])
                    # Marcar palabra completada en verde
                    self.marcar_palabra_completada(fila, col, palabra, p['direccion'])
        
        self.palabras_ok = completas
        self.puntaje = completas * 10
        self.lbl_puntaje.config(text=f"Puntaje: {self.puntaje}")
        self.lbl_completado.config(text=f"Completado: {completas}/{len(self.crucigrama_actual['palabras'])}")
        
        if completas == len(self.crucigrama_actual['palabras']):
            self.juego_completado()

    def marcar_palabra_completada(self, fila, col, palabra, direccion):
        """Marca una palabra completada en verde"""
        if direccion == 'H':
            for i in range(len(palabra)):
                if col + i < len(self.celdas[0]):
                    celda = self.celdas[fila][col + i]
                    if celda:
                        celda.config(bg='#2ECC71', fg='white')
        else:
            for i in range(len(palabra)):
                if fila + i < len(self.celdas):
                    celda = self.celdas[fila + i][col]
                    if celda:
                        celda.config(bg='#2ECC71', fg='white')

    def juego_completado(self):
        """Maneja el juego completado y guarda el puntaje"""
        self.juego_activo = False
        tiempo_transcurrido = (datetime.datetime.now() - self.tiempo_inicio).seconds
        
        # Calcular puntaje final (base + bonificación por tiempo)
        bonus_tiempo = max(0, 300 - tiempo_transcurrido)  # Bonificación por terminar rápido
        puntaje_final = self.puntaje + bonus_tiempo
        
        # GUARDAR EL PUNTAJE EN LA BASE DE DATOS
        puntaje_guardado = False
        mensaje_usuario = ""
        
        if self.auth and self.auth.usuario_actual and self.database:
            try:
                usuario_id = self.database.obtener_id_usuario(self.auth.usuario_actual)
                if usuario_id:
                    # CORRECCIÓN: Usar guardar_puntaje (no registrar_puntaje)
                    exito = self.database.guardar_puntaje(
                        usuario_id=usuario_id,
                        juego="Crucigrama",
                        puntaje=puntaje_final,
                        dificultad=None,  # No hay dificultad en crucigramas
                        categoria=self.crucigrama_actual['nombre']
                    )
                    
                    if exito:
                        print(f"✅ Puntaje guardado: {puntaje_final} para usuario {self.auth.usuario_actual}")
                        puntaje_guardado = True
                        mensaje_usuario = f"¡Puntaje guardado en tu perfil!"
                        
                        # Verificar que se guardó realmente
                        self.verificar_puntaje_guardado(usuario_id, puntaje_final)
                    else:
                        print("❌ No se pudo guardar el puntaje")
                        mensaje_usuario = f"Error al guardar puntaje"
                else:
                    print("⚠️ No se pudo obtener el ID del usuario")
                    mensaje_usuario = f"Usuario no encontrado"
            except Exception as e:
                print(f"❌ Error al guardar puntaje: {e}")
                mensaje_usuario = f"Error técnico al guardar"
        else:
            print("⚠️ Usuario no autenticado o sin BD, no se guarda puntaje")
            if not self.auth or not self.auth.usuario_actual:
                mensaje_usuario = f"⚠️ Inicia sesión para guardar tus puntajes"
            else:
                mensaje_usuario = f"⚠️ No se pudo conectar con la base de datos"
        
        # Mensaje final al usuario
        mensaje = f"¡Completaste todo el crucigrama!\n\n"
        mensaje += f"🏆 Puntaje: {puntaje_final}\n"
        mensaje += f"⏱️ Tiempo: {tiempo_transcurrido}s\n"
        mensaje += f"📈 Bonus tiempo: +{bonus_tiempo}\n\n"
        
        if puntaje_guardado:
            mensaje += f"✅ {mensaje_usuario}"
        else:
            mensaje += f"{mensaje_usuario}"
        
        messagebox.showinfo("¡GANASTE!", mensaje)
        
        self.mostrar_menu_principal()

    def verificar_puntaje_guardado(self, usuario_id, puntaje):
        """Verifica que el puntaje se guardó correctamente"""
        try:
            conexion = self.database.get_conexion()
            cursor = conexion.cursor()
            
            # Buscar el puntaje recién guardado
            cursor.execute('''
                SELECT COUNT(*) FROM puntajes 
                WHERE usuario_id = ? AND juego = ? AND puntaje = ? AND categoria = ?
            ''', (usuario_id, "Crucigrama", puntaje, self.crucigrama_actual['nombre']))
            
            count = cursor.fetchone()[0]
            
            # Mostrar todos los puntajes del usuario para debug
            cursor.execute('''
                SELECT * FROM puntajes 
                WHERE usuario_id = ? AND juego = ?
                ORDER BY fecha DESC
                LIMIT 5
            ''', (usuario_id, "Crucigrama"))
            
            puntajes = cursor.fetchall()
            print(f"📊 Últimos 5 puntajes del usuario: {puntajes}")
            
            conexion.close()
            
            if count > 0:
                print(f"✅ Verificación: Puntaje {puntaje} encontrado {count} veces en la BD")
            else:
                print("❌ Verificación: Puntaje NO encontrado en la BD")
                
        except Exception as e:
            print(f"❌ Error en verificación: {e}")

    def verificar(self):
        """Verifica todas las celdas"""
        for fila in self.celdas:
            for celda in fila:
                if celda:
                    if celda.get() == celda.letra_correcta:
                        celda.config(bg='#2ECC71', fg='white')
                    elif celda.get():
                        celda.config(bg='#E74C3C', fg='white')
        
        self.verificar_palabras()

    def limpiar(self):
        """Limpia el tablero"""
        for fila in self.celdas:
            for celda in fila:
                if celda:
                    celda.delete(0, tk.END)
                    celda.config(bg='#FFFFFF', fg='#000000')
        
        self.palabras_ok = 0
        self.puntaje = 0
        self.palabras_completadas.clear()
        self.lbl_puntaje.config(text="Puntaje: 0")
        self.lbl_completado.config(text=f"Completado: 0/{len(self.crucigrama_actual['palabras'])}")

    def volver_al_menu(self):
        """Vuelve al menú"""
        if messagebox.askyesno("Volver", "¿Volver al menú principal?"):
            self.mostrar_menu_principal()

    def volver_menu_principal(self):
        """Vuelve al menú principal de la aplicación"""
        try:
            # Limpiar bindings del mousewheel primero
            self.limpiar_bindings_mousewheel()
            
            from menu_principal import MenuPrincipal
            for w in self.root.winfo_children():
                w.destroy()
            
            # Volver al menú principal pasando auth y database
            MenuPrincipal(self.root, self.auth, self.database)
            
        except Exception as e:
            print(f"Error volviendo al menú: {e}")
            # Si hay error, intentar cerrar limpiamente
            try:
                self.root.quit()
            except:
                pass


# Función principal para iniciar el juego desde el menú principal
def iniciar_crucigrama(root, auth=None, database=None):
    """Función para iniciar el crucigrama desde el menú principal"""
    for widget in root.winfo_children():
        widget.destroy()
    
    # Crear instancia pasando auth y database
    app = Crucigrama(root, auth, database)


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
        
        app = Crucigrama(root, auth, db)
    except ImportError:
        print("⚠️ No se encontraron módulos de auth/database, ejecutando en modo prueba")
        app = Crucigrama(root)
    
    root.mainloop()