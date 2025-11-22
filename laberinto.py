# laberinto.py
import tkinter as tk
from tkinter import messagebox
import datetime
from app_manager import app_manager

class Laberinto:
    def __init__(self, root):
        self.root = root
        self.nivel_actual = 1
        self.canvas = None
        self.posicion_jugador = None
        self.tiempo_inicio = None
        self.puntaje = 0
        self.juego_activo = True
        self.movimientos = 0
        
        # Definir los 10 niveles
        self.niveles = self._definir_niveles_correctos()
        
        self.mostrar_menu_niveles()

    def _texto_a_paredes(self, laberinto_texto):
        paredes = []
        entrada = None
        salida = None
        for fila, linea in enumerate(laberinto_texto):
            for col, char in enumerate(linea):
                if char == "#":
                    paredes.append((fila, col))
                elif char == "E":
                    entrada = (fila, col)
                elif char == "S":
                    salida = (fila, col)
        return paredes, entrada, salida
    
    def _definir_niveles_correctos(self):
        """Define 10 niveles de laberintos funcionales y desafiantes"""
        niveles = {}
        
        # NIVEL 1 - Laberinto basado en la imagen (salida arriba-izquierda, entrada abajo-derecha)
        laberinto_texto = [
            "###...####.#",
            "#####...##.#",
            "S.##.#.#.#..",
            "#.#....#...#",
            "#...##.#.#.#",
            "#####..#.#..",
            "..#.#.##.#.#",
            "#.#.#....#.#",
            "..#.######.#",
            "#..........#",
            "#.###.###..E",
            "####..######"
        ]
        paredes, entrada, salida = self._texto_a_paredes(laberinto_texto)
        niveles[1] = {
            'nombre': 'Muy Fácil',
            'grid_size': 12,
            'cell_size': 42,
            'entrada': entrada,  # esquina inferior derecha
            'salida': salida,    # esquina superior izquierda
            'paredes': paredes
        }

        # NIVEL 2 - Laberinto (más grande para mejor detalle)
        laberinto_texto_2 = [
            "##########S###.#",
            "#.....####.#...#",
            "#.###.####.#.#.#",
            "#.##..####...#.#",
            "#.#.#####.###..#",
            "E.#.......#.#.#.",
            "#.#####.###.#.#.",
            "#...........#...",
            "####.#######.#.#",
            "#....#.#.....#.#",
            "#.##.#.#.###.#.#",
            "#.#..#...#.....#",
            "#.#.###.#.####..",
            "#.#.....#.......",
            "#.#####.#####.##",
            "#.###...########"
        ]

        paredes2, entrada2, salida2 = self._texto_a_paredes(laberinto_texto_2)

        niveles[2] = {
        'nombre': 'Fácil ',
        'grid_size': 16,
        'cell_size': 36,       
        'entrada': entrada2,   # debería quedar en (0,0) por 'E' en la matriz
        'salida': salida2,     # debería quedar en (15,15) por 'S' en la matriz
        'paredes': paredes2
        }
        
        laberinto_texto_3 = [
            "#################E##",
            "#......#.#........##",
            "######.#.#.###.##.##",
            "#.#.........#####.##",
            "#.#.###.###.##.##...",
            "#.#..#...#.....#####",
            "#...#..####.###.....",
            "#####.......###.###.",
            "#####.#.#.#####...#.",
            "......#.#.####.##.#.",
            "####.#####.###.####.",
            "###.....#.#.........",
            "###.###.#####.#.####",
            "###.#.........#.###.",
            "##..#.#######.#..###",
            "##.#.#.#.......#.###",
            "#..#.#.#.###.#.#..##",
            "#####....#.#.#.#####",
            "#.....#....#...#...#",
            "S.##.#.###.#######.#",
            "#######...........#",
            "####################"
        ]

        paredes3, entrada3, salida3 = self._texto_a_paredes(laberinto_texto_3)

        niveles[3] = {
            'nombre': 'Nivel 3 Grande',
            'grid_size': 20,
            'cell_size': 30,       
            'entrada': entrada3,   # 'E' en la matriz (arriba centro)
            'salida': salida3,     # 'S' en la matriz (abajo centro)
            'paredes': paredes3
        }

        # NIVEL 4 - Laberinto en espiral
        laberinto_texto_4 = [
            "##########S#########",
            "##.............#...#",
            "#.##########.#.###.#",
            "#.#..........#...#.#",
            "#.####.###########.#",
            "#.#....#.......#.#.#",
            "#.#.####.#####.#.#.#",
            "#.#....#.#.....#.#.#",
            "#.#.####.#.###.#.#.#",
            "#.#.#....#.....#.#.#",
            "#.#.######.###.#.#.#",
            "#.#........#...#.#.#",
            "#.##########.#.#.#.#",
            "#.############.#...#",
            "#.#............#.#.#",
            "#.##.###########.#.#",
            "#.#..............#.#",
            "##################.#",
            "#..................#",
            "#########E##########"
        ]

        paredes4, entrada4, salida4 = self._texto_a_paredes(laberinto_texto_4)

        niveles[4] = {
            'nombre': 'Espiral',
            'grid_size': 20,
            'cell_size': 30,       
            'entrada': entrada4,   # 'E' (abajo centro en esta matriz)
            'salida': salida4,     # 'S' (arriba centro en esta matriz)
            'paredes': paredes4
        }

        # NIVEL 5 - Laberinto de cuadrado
        laberinto_texto_5 = [
            "E.##################",
            "#..#.##.....##.....#",
            "#.##.##.###.##.###.#",
            "#....##.#.#.#..#...#",
            "###.###.#.#.##.###.#",
            "#.#.....#.#....#.#.#",
            "#.#######.######.#.#",
            "#......#...........#",
            "####.#.#####.##.#.#.",
            "#....#.#####.#..#.#.",
            "#.##.#.#####.##.#.#.",
            "#.#....#####.#..#..#",
            "#.#.##.#####.####.##",
            "#.#..#.......#......",
            "#.##################",
            "#......#.....#.....#",
            "#.####.#.###.#.###.#",
            "#.....#....#....#...",
            "#.###.###.####.##.#.",
            "#####.....####.##S##"
        ]

        paredes5, entrada5, salida5 = self._texto_a_paredes(laberinto_texto_5)

        niveles[5] = {
            'nombre': 'Cuadrado',
            'grid_size': 20,
            'cell_size': 30,       # zoom pedido
            'entrada': entrada5,   # 'E' arriba-izquierda
            'salida': salida5,     # 'S' abajo-derecha
            'paredes': paredes5
        }
        
        # NIVEL 6 - Laberinto cruz
        laberinto_texto_6 = [
            "S.#......##......",
            "#...#..#.#.......",
            "########.######.#",
            "#.....#......#..#",
            "#.######..####..#",
            "#.#.....#.......#",
            "#.####....#######",
            "......##...#.....",
            "......###.#......",
            "......#...#......",
            "......#.###......",
            "......#...#......",
            "......###.#......",
            "......#.#.#......",
            "......#...#......",
            "......##.##......",
            ".......E..#......"
        ]

        paredes6, entrada6, salida6 = self._texto_a_paredes(laberinto_texto_6)

        niveles[6] = {
            'nombre': 'Cruz Visual',
            'grid_size': 17,
            'cell_size': 30,
            'entrada': entrada6,   # 'E' abajo centro en la matriz
            'salida': salida6,     # 'S' arriba centro en la matriz
            'paredes': paredes6
        }
        
        # NIVEL 7 - Laberinto denso complejo
        laberinto_texto_7 = [
            "E.###...####..##..",
            "#...#.#....#..#..#",
            "###.#.####.#.##.##",
            "#.........#.....#",
            "#.#####.######.#.#",
            "#.#.....#......#.#",
            "#.#.###.####.#.#.#",
            "#.#.#.#......#...#",
            "#.#.#.#########...",
            "#.#.#.........#.#.",
            "#.#.#########...##",
            "#.#....#......#..#",
            "#.######.#######.#",
            "#.....#..##.#..###",
            "###.###.#.#.##...#",
            "#...#...#......#.#",
            "#.###.#.#.######.#",
            ".##...#......###S#"
        ]

        paredes7, entrada7, salida7 = self._texto_a_paredes(laberinto_texto_7)

        niveles[7] = {
            'nombre': 'Denso',
            'grid_size': 18,
            'cell_size': 28,
            'entrada': entrada7,
            'salida': salida7,
            'paredes': paredes7
        }
        
        # NIVEL 8 - Laberinto de habitaciones
        laberinto_texto_8 = [
            "E.#.###########.##.",
            "#......#.....#..#.#",
            "##.#.#...#.###.#.##",
            "#..#.#...#.#...#..#",
            "#.##.#.#####.#.##.#",
            "#............#..#.#",
            "###.#########.#...#",
            "#.#..#....#.....#.#",
            "#.#############.#.#",
            "#........#......#.#",
            "####.###...###.#.#.",
            "#....#.......#.#..#",
            "#.##.#.#####.#.##.#",
            "#.#..#.#.....#...#.",
            "#.#.##.#.###.#####.",
            "#.#....#.#.#.......",
            "#.######.#.######.#",
            "#.......#.........#",
            "########S.#########"
        ]

        paredes8, entrada8, salida8 = self._texto_a_paredes(laberinto_texto_8)

        niveles[8] = {
            'nombre': 'Habitaciones',
            'grid_size': 19,
            'cell_size': 27,
            'entrada': entrada8,   # 'E' abajo centro en la matriz
            'salida': salida8,     # 'S' arriba-izquierda en la matriz
            'paredes': paredes8
        }
        
        # NIVEL 9 - Laberinto zigzag complejo
        laberinto_texto_9 = [
            "E.#####.#####.#####.",
            "#.................#.",
            "#############.#####.",
            "#.#.#.#.#.#.#.#.#.#.",
            "#.#.#.#.......#.#.#.",
            "#.#.#.#.#######.#.#.",
            "#.#...........#...#.",
            "#.#####.#####.###.#.",
            "#.#.........#...#.#.",
            "#.#.#.#.###.#####.#.",
            "#...#.#...#........#",
            "###.#.###.#.########",
            "#...#.....#........#",
            "#.#####.###.#.###.##",
            "#.#.....#...#...#..#",
            "#.#.###.#.#####.##.#",
            "#.#.#...#...........",
            "#.#.###############.",
            "##............#..#..",
            "#############....S#."
        ]

        paredes9, entrada9, salida9 = self._texto_a_paredes(laberinto_texto_9)

        niveles[9] = {      
            'nombre': 'Difícil',
            'grid_size': 20,
            'cell_size': 26,
            'entrada': entrada9,
            'salida': salida9,
            'paredes': paredes9
        }
        
        # NIVEL 10 - Laberinto final épico
        laberinto_texto_10 = [
            "##########E##########",
            "#....##.....##......#",
            "#.##...###.#.##.#.#.#",
            "#.#..#.#...#....#.#.#",
            "#.#.##.#.###.#.#.#..#",
            "#.#.#..#......##.##.#",
            "#.#.#.#######.#.#...#",
            "#.#.#.......#.#.###.#",
            "#.#.#######.#.#.#.#.#",
            "#.#.......#.#...#.#.#",
            "#.#######.#.#####.#.#",
            "#......#..#.........#",
            "####.#.#.#.#####.#.#.",
            "#....#.#.#.#.....#..#",
            "#.##..##.#.#.###.##.#",
            "#.#.....#.####.....#.",
            "###.#####.....#######",
            "#.........#.#.......#",
            "#.#################.#",
            "#........#....#...#.#",
            "###########S#...#...#"
        ]

        paredes10, entrada10, salida10 = self._texto_a_paredes(laberinto_texto_10)

        niveles[10] = {
            'nombre': 'Desafío Final',
            'grid_size': 21,
            'cell_size': 24,
            'entrada': entrada10,
            'salida': salida10,
            'paredes': paredes10
        }
        
        return niveles
    
    def mostrar_menu_niveles(self):
        """Muestra el menú de selección de niveles"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Laberinto - Selección de Nivel")
        self.root.geometry("700x650")
        self.root.configure(bg='#2C3E50')
        
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Título
        tk.Label(main_frame, text="🧭 LABERINTO 🧭",
                 font=("Arial", 24, "bold"), bg='#2C3E50', fg='white', pady=20).pack()
        
        tk.Label(main_frame, text="Usa las flechas del teclado para moverte",
                 font=("Arial", 12), bg='#2C3E50', fg='#BDC3C7', pady=5).pack()
        
        tk.Label(main_frame, text="↑ ↓ ← → para navegar por el laberinto",
                 font=("Arial", 11), bg='#2C3E50', fg='#95A5A6', pady=10).pack()
        
        # Grid de niveles
        frame_niveles = tk.Frame(main_frame, bg='#2C3E50')
        frame_niveles.pack(fill='both', expand=True, pady=20)
        
        # Crear botones de niveles en grid 2x5
        for nivel in range(1, 11):
            row = (nivel - 1) // 5
            col = (nivel - 1) % 5
            
            # Color según dificultad
            if nivel <= 3:
                color = '#2ECC71'
            elif nivel <= 6:
                color = '#F39C12'
            else:
                color = '#E74C3C'
            
            nivel_data = self.niveles[nivel]
            btn = tk.Button(frame_niveles, 
                            text=f"Nivel {nivel}\n{nivel_data['nombre']}",
                            font=("Arial", 10, "bold"), bg=color, fg='white',
                            width=14, height=3, cursor='hand2',
                            command=lambda n=nivel: self.iniciar_nivel(n))
            btn.grid(row=row, column=col, padx=8, pady=8)
        
        # Botón volver
        tk.Button(main_frame, text="← VOLVER AL MENÚ PRINCIPAL",
                  font=("Arial", 11, "bold"), bg='#95A5A6', fg='white',
                  padx=20, pady=10, cursor='hand2',
                  command=self.volver_menu_principal).pack(pady=20)
    
    def iniciar_nivel(self, nivel):
        """Inicia un nivel específico"""
        self.nivel_actual = nivel
        self.juego_activo = True
        self.movimientos = 0
        self.tiempo_inicio = datetime.datetime.now()
        
        nivel_data = self.niveles[nivel]
        self.posicion_jugador = nivel_data['entrada']
        
        self.mostrar_juego(nivel_data)
    
    def mostrar_juego(self, nivel_data):
        """Muestra la pantalla del juego"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        grid_size = nivel_data['grid_size']
        cell_size = nivel_data['cell_size']
        
        canvas_width = grid_size * cell_size
        canvas_height = grid_size * cell_size
        
        self.root.title(f"Laberinto - Nivel {self.nivel_actual}: {nivel_data['nombre']}")
        self.root.geometry(f"{canvas_width + 300}x{canvas_height + 120}")
        self.root.configure(bg='#34495E')
        
        main_frame = tk.Frame(self.root, bg='#34495E')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Frame(main_frame, bg='#34495E')
        header.pack(fill='x', pady=10)
        
        tk.Label(header, text=f"🧭 Nivel {self.nivel_actual}: {nivel_data['nombre']}",
                 font=("Arial", 16, "bold"), bg='#34495E', fg='white').pack(side='left')
        
        self.label_movimientos = tk.Label(header, text=f"Movimientos: {self.movimientos}",
                 font=("Arial", 12), bg='#34495E', fg='#3498DB')
        self.label_movimientos.pack(side='right', padx=10)
        
        # Contenedor principal
        contenedor = tk.Frame(main_frame, bg='#34495E')
        contenedor.pack(fill='both', expand=True)
        
        # Canvas para el laberinto
        canvas_frame = tk.Frame(contenedor, bg='#2C3E50', relief='ridge', bd=3)
        canvas_frame.pack(side='left', padx=10, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg='#FFFFFF', 
                                width=canvas_width, height=canvas_height,
                                highlightthickness=0)
        self.canvas.pack()
        
        # Panel de controles
        controles_frame = tk.Frame(contenedor, bg='#34495E')
        controles_frame.pack(side='right', fill='y', padx=10)
        
        tk.Label(controles_frame, text="CONTROLES",
                 font=("Arial", 14, "bold"), bg='#34495E', fg='white', pady=15).pack()
        
        tk.Label(controles_frame, text="⌨️ TECLAS",
                 font=("Arial", 12, "bold"), bg='#34495E', fg='#3498DB', pady=10).pack()
        
        teclas_frame = tk.Frame(controles_frame, bg='#34495E')
        teclas_frame.pack(pady=5)
        
        tk.Label(teclas_frame, text="↑ Arriba\n↓ Abajo\n← Izquierda\n→ Derecha",
                 font=("Arial", 11), bg='#34495E', fg='#BDC3C7',
                 justify='left', pady=5).pack()
        
        tk.Frame(controles_frame, bg='#34495E', height=20).pack()
        
        tk.Button(controles_frame, text="🔄 REINICIAR",
                  font=("Arial", 11, "bold"), bg='#3498DB', fg='white',
                  width=18, height=2, cursor='hand2',
                  command=lambda: self.iniciar_nivel(self.nivel_actual)).pack(pady=10)
        
        tk.Button(controles_frame, text="📋 NIVELES",
                  font=("Arial", 11, "bold"), bg='#9B59B6', fg='white',
                  width=18, height=2, cursor='hand2',
                  command=self.mostrar_menu_niveles).pack(pady=10)
        
        tk.Button(controles_frame, text="🏠 MENÚ PRINCIPAL",
                  font=("Arial", 11, "bold"), bg='#95A5A6', fg='white',
                  width=18, height=2, cursor='hand2',
                  command=self.volver_menu_principal).pack(pady=10)
        
        # Guardar datos del nivel
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.entrada = nivel_data['entrada']
        self.salida = nivel_data['salida']
        self.paredes = set(nivel_data['paredes'])
        
        # Dibujar el laberinto
        self.dibujar_laberinto()
        
        # Bind teclas de dirección
        self.root.bind('<Up>', lambda e: self.mover('arriba'))
        self.root.bind('<Down>', lambda e: self.mover('abajo'))
        self.root.bind('<Left>', lambda e: self.mover('izquierda'))
        self.root.bind('<Right>', lambda e: self.mover('derecha'))
        
        # Focus en el root para capturar teclas
        self.root.focus_set()
    
    def dibujar_laberinto(self):
        """Dibuja el laberinto completo"""
        self.canvas.delete('all')
        
        # Dibujar grid de fondo
        for i in range(self.grid_size + 1):
            y = i * self.cell_size
            self.canvas.create_line(0, y, self.grid_size * self.cell_size, y, 
                                   fill='#D5DBDB', width=1)
        
        for i in range(self.grid_size + 1):
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, self.grid_size * self.cell_size, 
                                   fill='#D5DBDB', width=1)
        
        # Dibujar paredes (negro sólido)
        for fila, col in self.paredes:
            x1 = col * self.cell_size
            y1 = fila * self.cell_size
            self.canvas.create_rectangle(x1, y1, x1 + self.cell_size, y1 + self.cell_size,
                                         fill='#2C3E50', outline='#1C2833', width=2)
        
        # Dibujar salida (rojo brillante con estrella)
        salida_fila, salida_col = self.salida
        x1 = salida_col * self.cell_size
        y1 = salida_fila * self.cell_size
        self.canvas.create_rectangle(x1, y1, x1 + self.cell_size, y1 + self.cell_size,
                                     fill='#E74C3C', outline='#C0392B', width=3)
        self.canvas.create_text(x1 + self.cell_size // 2, y1 + self.cell_size // 2,
                               text="⭐", font=("Arial", int(self.cell_size * 0.6)))
        
        # Dibujar jugador (círculo azul)
        self.dibujar_jugador()
    
    def dibujar_jugador(self):
        """Dibuja al jugador en su posición actual"""
        # Borrar jugador anterior
        self.canvas.delete('jugador')
        
        fila, col = self.posicion_jugador
        x = col * self.cell_size + self.cell_size // 2
        y = fila * self.cell_size + self.cell_size // 2
        radio = self.cell_size // 3
        
        # Círculo azul brillante para el jugador
        self.canvas.create_oval(x - radio, y - radio, x + radio, y + radio,
                               fill='#3498DB', outline='#2980B9', width=3,
                               tags='jugador')
        
        # Punto blanco en el centro
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3,
                               fill='white', outline='', tags='jugador')
    
    def mover(self, direccion):
        """Mueve al jugador en la dirección indicada"""
        if not self.juego_activo:
            return
        
        fila, col = self.posicion_jugador
        nueva_fila, nueva_col = fila, col
        
        # Calcular nueva posición
        if direccion == 'arriba':
            nueva_fila = fila - 1
        elif direccion == 'abajo':
            nueva_fila = fila + 1
        elif direccion == 'izquierda':
            nueva_col = col - 1
        elif direccion == 'derecha':
            nueva_col = col + 1
        
        # Verificar límites del grid
        if nueva_fila < 0 or nueva_fila >= self.grid_size:
            return
        if nueva_col < 0 or nueva_col >= self.grid_size:
            return
        
        # Verificar si hay pared
        if (nueva_fila, nueva_col) in self.paredes:
            # Sonido de choque (visual)
            self.canvas.config(bg='#FADBD8')
            self.root.after(100, lambda: self.canvas.config(bg='#FFFFFF'))
            return
        
        # Mover al jugador
        self.posicion_jugador = (nueva_fila, nueva_col)
        self.movimientos += 1
        self.label_movimientos.config(text=f"Movimientos: {self.movimientos}")
        
        # Redibujar jugador
        self.dibujar_jugador()
        
        # Verificar si llegó a la salida
        if self.posicion_jugador == self.salida:
            self.nivel_completado()
    
    def nivel_completado(self):
        """Maneja la finalización exitosa del nivel"""
        self.juego_activo = False
        tiempo_final = datetime.datetime.now()
        tiempo_transcurrido = (tiempo_final - self.tiempo_inicio).seconds
        
        # Calcular puntaje
        puntaje_base = self.nivel_actual * 100
        
        # Bonus por movimientos eficientes
        movimientos_optimos = {1: 30, 2: 40, 3: 45, 4: 60, 5: 50, 
                              6: 55, 7: 70, 8: 80, 9: 90, 10: 100}
        movimientos_esperados = movimientos_optimos.get(self.nivel_actual, 50)
        
        if self.movimientos <= movimientos_esperados:
            bonus_movimientos = 200
        elif self.movimientos <= movimientos_esperados * 1.5:
            bonus_movimientos = 100
        else:
            bonus_movimientos = 50
        
        # Bonus por tiempo
        bonus_tiempo = max(0, 180 - tiempo_transcurrido) * 2
        
        puntaje_total = puntaje_base + bonus_movimientos + bonus_tiempo
        
        # Guardar puntaje si hay usuario logueado
        if hasattr(app_manager, 'auth') and app_manager.auth and \
           getattr(app_manager.auth, 'usuario_actual', None) and \
           getattr(app_manager, 'database', None):
            try:
                usuario_id = app_manager.database.obtener_id_usuario(app_manager.auth.usuario_actual)
                if usuario_id:
                    app_manager.database.guardar_puntaje(
                        usuario_id,
                        "Laberinto",
                        puntaje_total,
                        dificultad="Variable",
                        categoria=f"Nivel {self.nivel_actual}"
                    )
            except Exception as e:
                print(f"Error guardando puntaje: {e}")
        
        # Animación de victoria
        self.canvas.config(bg='#D5F4E6')
        
        # Mensaje de victoria
        mensaje = f"🎉 ¡NIVEL COMPLETADO! 🎉\n\n"
        mensaje += f"Nivel {self.nivel_actual}: {self.niveles[self.nivel_actual]['nombre']}\n\n"
        mensaje += f"⏱️ Tiempo: {tiempo_transcurrido}s\n"
        mensaje += f"👣 Movimientos: {self.movimientos}\n"
        mensaje += f"━━━━━━━━━━━━━━━\n"
        mensaje += f"💰 Puntaje base: {puntaje_base}\n"
        mensaje += f"⚡ Bonus movimientos: +{bonus_movimientos}\n"
        mensaje += f"⏰ Bonus tiempo: +{bonus_tiempo}\n"
        mensaje += f"━━━━━━━━━━━━━━━\n"
        mensaje += f"⭐ PUNTAJE TOTAL: {puntaje_total}"
        
        messagebox.showinfo("¡Victoria!", mensaje)
        
        # Ofrecer siguiente nivel o volver al menú
        if self.nivel_actual < 10:
            respuesta = messagebox.askyesno(
                "Siguiente Nivel",
                f"¿Quieres jugar el Nivel {self.nivel_actual + 1}?"
            )
            if respuesta:
                self.iniciar_nivel(self.nivel_actual + 1)
            else:
                self.mostrar_menu_niveles()
        else:
            messagebox.showinfo(
                "¡FELICITACIONES!",
                "¡Has completado todos los niveles del laberinto!\n\n🏆🎉\n\n¡Eres un maestro del laberinto!"
            )
            self.mostrar_menu_niveles()
    
    def volver_menu_principal(self):
        """Vuelve al menú principal de la aplicación"""
        try:
            from menu_principal import MenuPrincipal
            for widget in self.root.winfo_children():
                widget.destroy()
            
            try:
                from app_manager import app_manager
                MenuPrincipal(self.root, app_manager.auth, app_manager.database)
            except:
                MenuPrincipal(self.root, None, None)
        except Exception as e:
            print(f"Error volviendo al menú: {e}")
            self.root.quit()


# Test
if __name__ == "__main__":
    root = tk.Tk()
    app = Laberinto(root)
    root.mainloop()
