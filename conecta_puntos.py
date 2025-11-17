# conecta_puntos.py
# Versión con soluciones reales al rendirse

import tkinter as tk
from tkinter import messagebox
import copy
from app_manager import app_manager

class ConectaPuntos:
    def __init__(self, root):
        self.root = root
        self.grid_size = 6
        self.cell_size = 80
        self.nivel_actual = 1
        self.juego_completado = False

        # Niveles extremadamente simples
        self.niveles = self._definir_niveles_corregidos()
        self.mostrar_menu_niveles()

    def _definir_niveles_corregidos(self):
        """Niveles que son imposibles de fallar"""
        niveles = {}

        # Nivel 1 - Solo 3 pares muy separados
        niveles[1] = {
            'pairs': [
                ('red', (0,0), (0,5)),
                ('blue', (2,0), (2,5)),
                ('green', (4,0), (4,5))
            ]
        }

        # Nivel 2 - 3 pares verticales
        niveles[2] = {
            'pairs': [
                ('red', (0,0), (5,0)),
                ('blue', (0,2), (5,2)),
                ('green', (0,4), (5,4))
            ]
        }

        # Nivel 3 - 4 pares en esquinas
        niveles[3] = {
            'pairs': [
                ('red', (0,0), (1,1)),
                ('blue', (0,5), (1,4)),
                ('green', (5,0), (4,1)),
                ('orange', (5,5), (4,4))
            ]
        }

        # Nivel 4 - 4 pares horizontales
        niveles[4] = {
            'pairs': [
                ('red', (0,0), (0,5)),
                ('blue', (1,0), (1,5)),
                ('green', (3,0), (3,5)),
                ('orange', (4,0), (4,5))
            ]
        }

        # Nivel 5 - 4 pares verticales
        niveles[5] = {
            'pairs': [
                ('red', (0,0), (5,0)),
                ('blue', (0,1), (5,1)),
                ('green', (0,3), (5,3)),
                ('orange', (0,4), (5,4))
            ]
        }

        # Nivel 6 - 5 pares simples
        niveles[6] = {
            'pairs': [
                ('red', (0,0), (0,5)),
                ('blue', (2,0), (2,5)),
                ('green', (4,0), (4,5)),
                ('orange', (1,1), (1,4)),
                ('purple', (3,1), (3,4))
            ]
        }

        # Nivel 7 - 5 pares en zonas separadas
        niveles[7] = {
            'pairs': [
                ('red', (0,0), (2,0)),
                ('blue', (0,5), (2,5)),
                ('green', (5,0), (3,0)),
                ('orange', (5,5), (3,5)),
                ('purple', (2,2), (3,3))
            ]
        }

        # Nivel 8 - 6 pares separados
        niveles[8] = {
            'pairs': [
                ('red', (0,0), (0,2)),
                ('blue', (0,3), (0,5)),
                ('green', (2,0), (2,2)),
                ('orange', (2,3), (2,5)),
                ('purple', (4,0), (4,2)),
                ('yellow', (4,3), (4,5))
            ]
        }

        # Nivel 9 - 6 pares en zonas bien separadas
        niveles[9] = {
            'pairs': [
                ('red', (0,0), (1,0)),      # Superior izquierda
                ('blue', (0,5), (1,5)),     # Superior derecha
                ('green', (5,0), (4,0)),    # Inferior izquierda
                ('orange', (5,5), (4,5)),   # Inferior derecha
                ('purple', (1,2), (1,3)),   # Centro superior
                ('yellow', (4,2), (4,3))    # Centro inferior
            ]
        }
        
        # Nivel 10 - 6 pares final
        niveles[10] = {
            'pairs': [
                ('red', (0,0), (0,5)),
                ('blue', (1,0), (1,5)),
                ('green', (3,0), (3,5)),
                ('orange', (4,0), (4,5)),
                ('purple', (2,1), (2,4)),
                ('yellow', (5,2), (5,3))
            ]
        }

        return niveles

    def _obtener_solucion_nivel(self, nivel):
        """Devuelve soluciones reales y lógicas para cada nivel"""
        soluciones = {
            1: {
                'red': [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5)],
                'blue': [(2,0), (2,1), (2,2), (2,3), (2,4), (2,5)],
                'green': [(4,0), (4,1), (4,2), (4,3), (4,4), (4,5)]
            },
            2: {
                'red': [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0)],
                'blue': [(0,2), (1,2), (2,2), (3,2), (4,2), (5,2)],
                'green': [(0,4), (1,4), (2,4), (3,4), (4,4), (5,4)]
            },
            3: {
                'red': [(0,0), (0,1), (1,1)],
                'blue': [(0,5), (0,4), (1,4)],
                'green': [(5,0), (5,1), (4,1)],
                'orange': [(5,5), (5,4), (4,4)]
            },
            4: {
                'red': [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5)],
                'blue': [(1,0), (1,1), (1,2), (1,3), (1,4), (1,5)],
                'green': [(3,0), (3,1), (3,2), (3,3), (3,4), (3,5)],
                'orange': [(4,0), (4,1), (4,2), (4,3), (4,4), (4,5)]
            },
            5: {
                'red': [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0)],
                'blue': [(0,1), (1,1), (2,1), (3,1), (4,1), (5,1)],
                'green': [(0,3), (1,3), (2,3), (3,3), (4,3), (5,3)],
                'orange': [(0,4), (1,4), (2,4), (3,4), (4,4), (5,4)]
            },
            6: {
                'red': [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5)],
                'blue': [(2,0), (2,1), (2,2), (2,3), (2,4), (2,5)],
                'green': [(4,0), (4,1), (4,2), (4,3), (4,4), (4,5)],
                'orange': [(1,1), (1,2), (1,3), (1,4)],
                'purple': [(3,1), (3,2), (3,3), (3,4)]
            },
            7: {
                'red': [(0,0), (1,0), (2,0)],
                'blue': [(0,5), (1,5), (2,5)],
                'green': [(5,0), (4,0), (3,0)],
                'orange': [(5,5), (4,5), (3,5)],
                'purple': [(2,2), (2,3), (3,3)]
            },
            8: {
                'red': [(0,0), (0,1), (0,2)],
                'blue': [(0,3), (0,4), (0,5)],
                'green': [(2,0), (2,1), (2,2)],
                'orange': [(2,3), (2,4), (2,5)],
                'purple': [(4,0), (4,1), (4,2)],
                'yellow': [(4,3), (4,4), (4,5)]
            },
            9: {
                'red': [(0,0), (1,0)],
                'blue': [(0,5), (1,5)],
                'green': [(5,0), (4,0)],
                'orange': [(5,5), (4,5)],
                'purple': [(1,2), (1,3)],
                'yellow': [(4,2), (4,3)]
            },
            10: {
                'red': [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5)],
                'blue': [(1,0), (1,1), (1,2), (1,3), (1,4), (1,5)],
                'green': [(3,0), (3,1), (3,2), (3,3), (3,4), (3,5)],
                'orange': [(4,0), (4,1), (4,2), (4,3), (4,4), (4,5)],
                'purple': [(2,1), (2,2), (2,3), (2,4)],
                'yellow': [(5,2), (5,3)]
            }
        }
        return soluciones.get(nivel, {})

    def mostrar_menu_niveles(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Conecta Puntos - Selección de Nivel")
        self.root.geometry("600x500")
        self.root.configure(bg='#2C3E50')

        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=40, pady=30)

        tk.Label(main_frame, text="🔴 CONECTA PUNTOS 🔵",
                 font=("Arial", 22, "bold"), bg='#2C3E50', fg='white', pady=20).pack()

        tk.Label(main_frame, text="Selecciona un nivel:",
                 font=("Arial", 14), bg='#2C3E50', fg='#BDC3C7', pady=10).pack()

        frame_niveles = tk.Frame(main_frame, bg='#2C3E50')
        frame_niveles.pack(fill='both', expand=True, pady=20)

        for nivel in range(1, 11):
            row = (nivel - 1) // 5
            col = (nivel - 1) % 5
            btn = tk.Button(frame_niveles, text=f"Nivel {nivel}",
                            font=("Arial", 12, "bold"), bg='#3498DB', fg='white',
                            width=10, height=2, cursor='hand2',
                            command=lambda n=nivel: self.iniciar_nivel(n))
            btn.grid(row=row, column=col, padx=8, pady=8)

        frame_botones = tk.Frame(main_frame, bg='#2C3E50')
        frame_botones.pack(fill='x', pady=20)

        tk.Button(frame_botones, text="← Volver al Menú Principal",
                  font=("Arial", 11), bg='#95A5A6', fg='white', padx=20, pady=8, cursor='hand2',
                  command=self.volver_menu_principal).pack()

    def iniciar_nivel(self, nivel):
        self.nivel_actual = nivel
        self.juego_completado = False

        nivel_info = self.niveles[nivel]
        self.pares = copy.deepcopy(nivel_info['pairs'])

        # Solo trackear caminos, no ocupación completa
        self.occupied = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.endpoints = {}
        
        # Marcar puntos finales
        for color, a, b in self.pares:
            self.endpoints[color] = (a, b)
            self.occupied[a[0]][a[1]] = f"dot:{color}"
            self.occupied[b[0]][b[1]] = f"dot:{color}"

        self.paths = {color: [] for color,_,_ in self.pares}
        self.current_color = None
        self.current_path = []

        self.mostrar_juego()

    def mostrar_juego(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title(f"Conecta Puntos - Nivel {self.nivel_actual}")
        canvas_w = self.grid_size * self.cell_size
        canvas_h = self.grid_size * self.cell_size
        win_w = canvas_w + 200
        win_h = canvas_h + 160
        self.root.geometry(f"{win_w}x{win_h}")
        self.root.configure(bg='#34495E')

        main_frame = tk.Frame(self.root, bg='#34495E')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        header = tk.Frame(main_frame, bg='#34495E')
        header.pack(fill='x')
        tk.Label(header, text=f"🎯 Nivel {self.nivel_actual}", font=("Arial", 16, "bold"),
                 bg='#34495E', fg='white').pack(side='left')

        canvas_frame = tk.Frame(main_frame, bg='#2C3E50', relief='ridge', bd=2)
        canvas_frame.pack(side='left', padx=10, pady=10)

        self.canvas = tk.Canvas(canvas_frame, bg='#ECF0F1', width=canvas_w, height=canvas_h,
                                highlightthickness=0)
        self.canvas.pack()

        self.canvas.bind('<Button-1>', self.on_button_press)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_button_release)

        frame_controles = tk.Frame(main_frame, bg='#34495E')
        frame_controles.pack(side='right', fill='y', padx=10)

        tk.Button(frame_controles, text='🔄 Reiniciar', font=("Arial",11), bg='#E67E22', fg='white',
                  width=15, pady=8, cursor='hand2', 
                  command=lambda: self.iniciar_nivel(self.nivel_actual)).pack(pady=6)

        tk.Button(frame_controles, text='🏳️ Rendirse', font=("Arial",11), bg='#E74C3C', fg='white',
                  width=15, pady=8, cursor='hand2', 
                  command=self.rendirse).pack(pady=6)

        tk.Button(frame_controles, text='📋 Niveles', font=("Arial",11), bg='#3498DB', fg='white',
                  width=15, pady=8, cursor='hand2', 
                  command=self.mostrar_menu_niveles).pack(pady=6)

        tk.Button(frame_controles, text='🏠 Menú Principal', font=("Arial",11), bg='#95A5A6', fg='white',
                  width=15, pady=8, cursor='hand2', 
                  command=self.volver_menu_principal).pack(pady=6)

        info_text = f'Nivel {self.nivel_actual}\n\nConecta {len(self.pares)} pares\nde puntos\n\nPueden quedar\nespacios libres'
        tk.Label(frame_controles, text=info_text,
                 bg='#34495E', fg='white', font=("Arial",10), justify='left').pack(pady=10)

        self.dibujar_estado()

    def dibujar_estado(self):
        self.canvas.delete('all')
        
        # Dibujar cuadrícula
        for r in range(self.grid_size + 1):
            y = r * self.cell_size
            self.canvas.create_line(0, y, self.grid_size*self.cell_size, y, fill='#BDC3C7')
        for c in range(self.grid_size + 1):
            x = c * self.cell_size
            self.canvas.create_line(x, 0, x, self.grid_size*self.cell_size, fill='#BDC3C7')

        # Dibujar caminos existentes
        for color, path in self.paths.items():
            if len(path) < 2:
                continue
                
            for i in range(1, len(path)):
                r1, c1 = path[i-1]
                r2, c2 = path[i]
                x1, y1 = self._cell_center(r1, c1)
                x2, y2 = self._cell_center(r2, c2)
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=6, capstyle='round')

        # Dibujar TODOS los puntos (siempre visibles)
        for color, (a,b) in self.endpoints.items():
            for (r,c) in (a,b):
                cx, cy = self._cell_center(r,c)
                # Punto con borde negro
                self.canvas.create_oval(cx-14, cy-14, cx+14, cy+14, outline='black', width=2)
                self.canvas.create_oval(cx-10, cy-10, cx+10, cy+10, fill=color, outline='')

        # Dibujar camino temporal
        if self.current_path and len(self.current_path) > 1:
            for i in range(1, len(self.current_path)):
                r1, c1 = self.current_path[i-1]
                r2, c2 = self.current_path[i]
                x1, y1 = self._cell_center(r1, c1)
                x2, y2 = self._cell_center(r2, c2)
                self.canvas.create_line(x1, y1, x2, y2, fill=self.current_color, 
                                      width=6, capstyle='round', dash=(4, 2))

    def _cell_center(self, r, c):
        x = c * self.cell_size + self.cell_size//2
        y = r * self.cell_size + self.cell_size//2
        return x, y

    def _pixel_to_cell(self, x, y):
        c = x // self.cell_size
        r = y // self.cell_size
        if 0 <= r < self.grid_size and 0 <= c < self.grid_size:
            return int(r), int(c)
        return None

    def on_button_press(self, event):
        if self.juego_completado:
            return
            
        cell = self._pixel_to_cell(event.x, event.y)
        if not cell:
            return
            
        r, c = cell
        val = self.occupied[r][c]
        
        # Empezar en cualquier punto no conectado
        if isinstance(val, str) and val.startswith('dot:'):
            color = val.split(':',1)[1]
            # Verificar que este punto no esté ya conectado
            path = self.paths.get(color, [])
            if (r, c) not in path or len(path) < 2:
                self.current_color = color
                self.current_path = [(r, c)]
                self.dibujar_estado()

    def on_mouse_drag(self, event):
        if not self.current_color or self.juego_completado:
            return
            
        cell = self._pixel_to_cell(event.x, event.y)
        if not cell:
            return
            
        r, c = cell
        last_r, last_c = self.current_path[-1]

        # Solo mover a celdas adyacentes
        if abs(last_r - r) + abs(last_c - c) != 1:
            return

        # Permitir retroceso
        if (r, c) in self.current_path:
            idx = self.current_path.index((r, c))
            self.current_path = self.current_path[:idx+1]
            self.dibujar_estado()
            return

        val = self.occupied[r][c]
        
        # Si llegamos al punto final del mismo color
        if isinstance(val, str) and val.startswith('dot:') and val == f'dot:{self.current_color}':
            start_point = self.current_path[0]
            end_point = (r, c)
            
            # Verificar que sea el punto opuesto
            endpoints = self.endpoints[self.current_color]
            if (start_point == endpoints[0] and end_point == endpoints[1]) or \
               (start_point == endpoints[1] and end_point == endpoints[0]):
                
                # Conectar directamente
                self.paths[self.current_color] = self.current_path + [end_point]
                self.current_path = []
                self.current_color = None
                self.dibujar_estado()
                
                if self.verificar_victoria():
                    self.juego_completado = True
                    self.mostrar_victoria()
                return

        # Agregar celda si no está en otro camino
        if not self.esta_en_otro_camino(r, c):
            self.current_path.append((r, c))
            self.dibujar_estado()

    def esta_en_otro_camino(self, r, c):
        """Verifica si la celda está en otro camino completado"""
        for color, path in self.paths.items():
            if color != self.current_color and (r, c) in path:
                return True
        return False

    def on_button_release(self, event):
        if self.current_color and self.current_path:
            # Solo mantener el camino si conecta dos puntos
            if len(self.current_path) < 2:
                self.current_path = []
                self.current_color = None
                self.dibujar_estado()

    def verificar_victoria(self):
        """Verifica si todos los pares están conectados"""
        for color, (start, end) in self.endpoints.items():
            path = self.paths.get(color, [])
            if len(path) < 2:
                return False
            if not ((path[0] == start and path[-1] == end) or 
                   (path[0] == end and path[-1] == start)):
                return False
        return True

    def rendirse(self):
        """Muestra soluciones reales y lógicas para cada nivel"""
        if self.juego_completado:
            return
            
        # Obtener solución real para este nivel
        solucion = self._obtener_solucion_nivel(self.nivel_actual)
        
        if solucion:
            # Aplicar la solución real
            self.paths = copy.deepcopy(solucion)
            self.dibujar_estado()
            messagebox.showinfo("Te has rendido", 
                               "❌ ¡Te has rendido! ❌\n\nSe ha mostrado una solución real.\n\n¡Inténtalo de nuevo!")
        else:
            # Si no hay solución predefinida, conectar directamente
            for color, (start, end) in self.endpoints.items():
                self.paths[color] = [start, end]
            self.dibujar_estado()
            messagebox.showinfo("Te has rendido", 
                               "❌ ¡Te has rendido! ❌\n\nTodos los puntos se han conectado.\n\n¡Inténtalo de nuevo!")
        
        self.root.after(2000, self.mostrar_menu_niveles)

    def mostrar_victoria(self):
        """Muestra mensaje de victoria"""
        if hasattr(app_manager, 'auth') and app_manager.auth and getattr(app_manager.auth, 'usuario_actual', None) and getattr(app_manager, 'database', None):
            try:
                usuario_id = app_manager.database.obtener_id_usuario(app_manager.auth.usuario_actual)
                if usuario_id:
                    app_manager.database.guardar_puntaje(
                        usuario_id,
                        "Conecta Puntos",
                        self.nivel_actual * 100,
                        dificultad="Media",
                        categoria=f"Nivel {self.nivel_actual}"
                    )
            except Exception as e:
                print(f"Error guardando puntaje: {e}")

        mensaje = f"🎉 ¡FELICIDADES! 🎉\n\nHas completado el Nivel {self.nivel_actual}"
        messagebox.showinfo("¡Victoria!", mensaje)
        self.root.after(100, self.mostrar_menu_niveles)

    def volver_menu_principal(self):
        try:
            from menu_principal import MenuPrincipal
            for widget in self.root.winfo_children():
                widget.destroy()
            MenuPrincipal(self.root, app_manager.auth, app_manager.database)
        except Exception as e:
            print(f"Error volviendo al menú: {e}")
            self.root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    app = ConectaPuntos(root)
    root.mainloop()