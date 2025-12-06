# sudoku.py
import tkinter as tk
from tkinter import messagebox
import random
import copy
from app_manager import app_manager

class Sudoku:
    def __init__(self, root):
        self.root = root
        self.tablero_inicial = []
        self.tablero_actual = []
        self.tablero_solucion = []
        self.celdas = []
        self.celda_seleccionada = None
        self.juego_activo = False
        self.dificultad_actual = None
        self.errores = 0
        self.max_errores = 3
        
        self.mostrar_menu_dificultad()
    
    def mostrar_menu_dificultad(self):
        """Muestra el menú de selección de dificultad"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Sudoku - Selección de Dificultad")
        self.root.geometry("700x700")
        self.root.configure(bg='#2C3E50')
        
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # BOTÓN VOLVER - ESQUINA SUPERIOR IZQUIERDA
        volver_frame = tk.Frame(main_frame, bg='#2C3E50')
        volver_frame.pack(anchor='nw', pady=(0, 20))
        
        tk.Button(volver_frame, text="← Volver",
                 font=("Arial", 10, "bold"), bg='#95A5A6', fg='white',
                 padx=15, pady=5, cursor='hand2',
                 command=self.volver_menu_principal).pack(side='left')
        
        # Título
        tk.Label(main_frame, text="🔢 SUDOKU 🔢",
                 font=("Arial", 32, "bold"), bg='#2C3E50', fg='white', pady=15).pack()
        
        tk.Label(main_frame, text="Completa el tablero del 1 al 9",
                 font=("Arial", 13), bg='#2C3E50', fg='#BDC3C7', pady=3).pack()
        
        tk.Label(main_frame, text="Sin repetir números en filas, columnas o regiones 3x3",
                 font=("Arial", 11), bg='#2C3E50', fg='#95A5A6', pady=5).pack()
        
        # Frame para dificultades
        frame_dificultades = tk.Frame(main_frame, bg='#2C3E50')
        frame_dificultades.pack(fill='both', expand=True, pady=20)
        
        dificultades_info = [
            ('Fácil', '5-6 números por región 3x3', 6, '#2ECC71'),
            ('Medio', '4 números por región 3x3', 4, '#3498DB'),
            ('Difícil', '3 números por región 3x3', 3, '#F39C12'),
            ('Experto', '2 números por región 3x3\n(¡Muy difícil!)', 2, '#E74C3C')
        ]
        
        for nombre, desc, pistas_region, color in dificultades_info:
            frame_dif = tk.Frame(frame_dificultades, bg='#34495E', relief='raised', bd=2)
            frame_dif.pack(fill='x', pady=8, padx=50)
            
            content = tk.Frame(frame_dif, bg='#34495E')
            content.pack(fill='x', padx=15, pady=12)
            
            info_frame = tk.Frame(content, bg='#34495E')
            info_frame.pack(side='left', fill='both', expand=True)
            
            tk.Label(info_frame, text=nombre,
                    font=("Arial", 16, "bold"), bg='#34495E', fg='white').pack(anchor='w')
            
            tk.Label(info_frame, text=desc,
                    font=("Arial", 10), bg='#34495E', fg='#BDC3C7', justify='left').pack(anchor='w', pady=(2, 0))
            
            btn = tk.Button(content, text="JUGAR",
                           font=("Arial", 11, "bold"), bg=color, fg='white',
                           width=10, height=1, cursor='hand2',
                           command=lambda n=nombre, p=pistas_region: self.iniciar_juego(n, p))
            btn.pack(side='right')
    
    def generar_sudoku_completo(self):
        """Genera un tablero de Sudoku completo y válido"""
        tablero = [[0 for _ in range(9)] for _ in range(9)]
        
        def es_valido(tablero, fila, col, num):
            # Verificar fila
            if num in tablero[fila]:
                return False
            
            # Verificar columna
            if num in [tablero[i][col] for i in range(9)]:
                return False
            
            # Verificar región 3x3
            region_fila = (fila // 3) * 3
            region_col = (col // 3) * 3
            for i in range(region_fila, region_fila + 3):
                for j in range(region_col, region_col + 3):
                    if tablero[i][j] == num:
                        return False
            
            return True
        
        def resolver(tablero):
            for fila in range(9):
                for col in range(9):
                    if tablero[fila][col] == 0:
                        numeros = list(range(1, 10))
                        random.shuffle(numeros)
                        for num in numeros:
                            if es_valido(tablero, fila, col, num):
                                tablero[fila][col] = num
                                if resolver(tablero):
                                    return True
                                tablero[fila][col] = 0
                        return False
            return True
        
        resolver(tablero)
        return tablero
    
    def crear_puzzle(self, tablero_completo, pistas_por_region):
        """Crea un puzzle con distribución equilibrada de pistas en cada región 3x3"""
        puzzle = [[0 for _ in range(9)] for _ in range(9)]
        
        print(f"Creando puzzle con {pistas_por_region} pistas por región...")
        
        # Colocar pistas en cada región 3x3 (9 regiones en total)
        for region_fila in range(3):
            for region_col in range(3):
                # Obtener todas las posiciones en esta región
                posiciones_region = []
                for i in range(3):
                    for j in range(3):
                        fila = region_fila * 3 + i
                        col = region_col * 3 + j
                        posiciones_region.append((fila, col))
                
                # Seleccionar aleatoriamente las pistas para esta región
                random.shuffle(posiciones_region)
                
                # Variar un poco el número de pistas (+/- 1)
                variacion = random.randint(-1, 1)
                pistas_a_colocar = max(2, min(9, pistas_por_region + variacion))
                
                print(f"Región [{region_fila},{region_col}]: colocando {pistas_a_colocar} pistas")
                
                # Colocar las pistas
                for idx in range(pistas_a_colocar):
                    fila, col = posiciones_region[idx]
                    valor = tablero_completo[fila][col]
                    puzzle[fila][col] = valor
                    print(f"  Colocando {valor} en [{fila},{col}]")
        
        # Verificar cuántas pistas se colocaron en total
        total_pistas = sum(1 for i in range(9) for j in range(9) if puzzle[i][j] != 0)
        print(f"Total de pistas colocadas: {total_pistas}")
        
        return puzzle
    
    def iniciar_juego(self, dificultad, pistas_por_region):
        """Inicia el juego con la dificultad seleccionada"""
        self.dificultad_actual = dificultad
        self.pistas_por_region = pistas_por_region
        self.errores = 0
        self.juego_activo = True
        
        # Generar tablero completo y crear puzzle
        tablero_completo = self.generar_sudoku_completo()
        self.tablero_solucion = [fila[:] for fila in tablero_completo]
        self.tablero_inicial = self.crear_puzzle(tablero_completo, pistas_por_region)
        self.tablero_actual = [fila[:] for fila in self.tablero_inicial]
        
        self.mostrar_pantalla_juego()
    
    def mostrar_pantalla_juego(self):
        """Muestra la pantalla principal del juego"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title(f"Sudoku - {self.dificultad_actual}")
        self.root.geometry("950x750")
        self.root.configure(bg='#34495E')
        
        # Debug: imprimir tablero inicial
        print("\n=== TABLERO INICIAL ===")
        for fila in self.tablero_inicial:
            print(fila)
        print("=======================\n")
        
        main_frame = tk.Frame(self.root, bg='#34495E')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header SOLO con título y contador de errores (sin botón duplicado)
        header = tk.Frame(main_frame, bg='#34495E')
        header.pack(fill='x', pady=(0, 10))
        
        # Título a la izquierda
        tk.Label(header, text=f"🔢 Sudoku - {self.dificultad_actual}",
                 font=("Arial", 18, "bold"), bg='#34495E', fg='white').pack(side='left')
        
        # Contador de errores a la derecha
        self.label_errores = tk.Label(header, text=f"❌ Errores: {self.errores}/{self.max_errores}",
                                      font=("Arial", 14, "bold"), bg='#34495E', fg='#E74C3C')
        self.label_errores.pack(side='right', padx=20)
        
        # Contenedor principal
        contenedor = tk.Frame(main_frame, bg='#34495E')
        contenedor.pack(fill='both', expand=True)
        
        # Panel izquierdo - Tablero
        panel_izq = tk.Frame(contenedor, bg='#34495E')
        panel_izq.pack(side='left', fill='both', expand=True)
        
        # Frame para el tablero
        frame_tablero = tk.Frame(panel_izq, bg='#2C3E50', relief='ridge', bd=5)
        frame_tablero.pack(padx=20, pady=20)
        
        self.celdas = []
        for i in range(9):
            fila_celdas = []
            for j in range(9):
                # Determinar borde para regiones 3x3
                if i % 3 == 0 and i != 0:
                    pady_top = 3
                else:
                    pady_top = 1
                
                if j % 3 == 0 and j != 0:
                    padx_left = 3
                else:
                    padx_left = 1
                
                # Frame para la celda
                celda_frame = tk.Frame(frame_tablero, bg='#2C3E50')
                celda_frame.grid(row=i, column=j, padx=(padx_left, 1), pady=(pady_top, 1))
                
                # Entry para la celda
                if self.tablero_inicial[i][j] != 0:
                    # Número fijo (del puzzle inicial)
                    entry = tk.Entry(celda_frame, width=2, font=("Arial", 20, "bold"),
                                    justify='center', bg='#BDC3C7', fg='#2C3E50',
                                    relief='flat', disabledforeground='#2C3E50')
                    entry.insert(0, str(self.tablero_inicial[i][j]))
                    entry.config(state='disabled')  # Deshabilitar después de insertar
                    entry.es_fija = True
                    print(f"Creando celda FIJA en [{i},{j}] con valor {self.tablero_inicial[i][j]}")
                else:
                    # Celda editable
                    entry = tk.Entry(celda_frame, width=2, font=("Arial", 20, "bold"),
                                    justify='center', bg='#ECF0F1', fg='#3498DB',
                                    relief='flat', insertwidth=0)
                    entry.es_fija = False
                    entry.bind('<FocusIn>', lambda e, r=i, c=j: self.seleccionar_celda(r, c))
                    entry.bind('<KeyRelease>', lambda e, r=i, c=j: self.on_numero_ingresado(e, r, c))
                    print(f"Creando celda EDITABLE en [{i},{j}]")
                
                entry.grid(row=0, column=0, ipadx=10, ipady=10)
                entry.fila = i
                entry.columna = j
                fila_celdas.append(entry)
            
            self.celdas.append(fila_celdas)
        
        # Panel derecho - Controles
        panel_der = tk.Frame(contenedor, bg='#34495E', width=300)
        panel_der.pack(side='right', fill='y', padx=(20, 0))
        panel_der.pack_propagate(False)
        
        tk.Label(panel_der, text="CONTROLES",
                 font=("Arial", 14, "bold"), bg='#34495E', fg='white', pady=15).pack()
        
        # Teclado numérico
        tk.Label(panel_der, text="Números:",
                 font=("Arial", 12, "bold"), bg='#34495E', fg='#BDC3C7', pady=10).pack()
        
        frame_numeros = tk.Frame(panel_der, bg='#34495E')
        frame_numeros.pack(pady=10)
        
        for i in range(1, 10):
            row = (i - 1) // 3
            col = (i - 1) % 3
            btn = tk.Button(frame_numeros, text=str(i),
                           font=("Arial", 16, "bold"), bg='#3498DB', fg='white',
                           width=3, height=1, cursor='hand2',
                           command=lambda n=i: self.insertar_numero(n))
            btn.grid(row=row, column=col, padx=3, pady=3)
        
        # Botón borrar
        tk.Button(frame_numeros, text="⌫",
                 font=("Arial", 16, "bold"), bg='#E67E22', fg='white',
                 width=10, height=1, cursor='hand2',
                 command=self.borrar_numero).grid(row=3, column=0, columnspan=3, pady=10)
        
        # Instrucciones
        tk.Label(panel_der, text="💡 Haz clic en una celda\ny escribe un número",
                 font=("Arial", 10), bg='#34495E', fg='#95A5A6', pady=10).pack()
        
        # Frame para botones de control - ORGANIZADOS EN 2 FILAS
        frame_botones = tk.Frame(panel_der, bg='#34495E')
        frame_botones.pack(pady=20)
        
        # Fila 1: VERIFICAR y REINICIAR
        frame_fila1 = tk.Frame(frame_botones, bg='#34495E')
        frame_fila1.pack(pady=5)
        
        tk.Button(frame_fila1, text="✓ VERIFICAR",
                 font=("Arial", 10, "bold"), bg='#2ECC71', fg='white',
                 width=14, height=2, cursor='hand2',
                 command=self.verificar_solucion).pack(side='left', padx=5)
        
        tk.Button(frame_fila1, text="🔄 REINICIAR",
                 font=("Arial", 10, "bold"), bg='#3498DB', fg='white',
                 width=14, height=2, cursor='hand2',
                 command=self.reiniciar_juego).pack(side='left', padx=5)
        
        # Fila 2: DIFICULTADES y RENDIRSE
        frame_fila2 = tk.Frame(frame_botones, bg='#34495E')
        frame_fila2.pack(pady=5)
        
        tk.Button(frame_fila2, text="📋 DIFICULTADES",
                 font=("Arial", 10, "bold"), bg='#9B59B6', fg='white',
                 width=14, height=2, cursor='hand2',
                 command=self.mostrar_menu_dificultad).pack(side='left', padx=5)
        
        tk.Button(frame_fila2, text="🏳️ RENDIRSE",
                 font=("Arial", 10, "bold"), bg='#E74C3C', fg='white',
                 width=14, height=2, cursor='hand2',
                 command=self.rendirse).pack(side='left', padx=5)
    
    def reiniciar_juego(self):
        """Reinicia el juego generando un nuevo puzzle con la misma dificultad"""
        self.iniciar_juego(self.dificultad_actual, self.pistas_por_region)
    
    def seleccionar_celda(self, fila, col):
        """Selecciona una celda"""
        if self.celdas[fila][col].es_fija:
            return
        
        # Deseleccionar todas
        for i in range(9):
            for j in range(9):
                if not self.celdas[i][j].es_fija:
                    self.celdas[i][j].config(bg='#ECF0F1')
        
        # Seleccionar actual
        self.celdas[fila][col].config(bg='#AED6F1')
        self.celda_seleccionada = (fila, col)
    
    def insertar_numero(self, numero):
        """Inserta un número en la celda seleccionada"""
        if not self.celda_seleccionada or not self.juego_activo:
            return
        
        fila, col = self.celda_seleccionada
        entry = self.celdas[fila][col]
        
        if entry.es_fija:
            return
        
        # Insertar número
        entry.delete(0, tk.END)
        entry.insert(0, str(numero))
        self.tablero_actual[fila][col] = numero
        
        # Verificar si es correcto
        if numero != self.tablero_solucion[fila][col]:
            # Error
            entry.config(bg='#FADBD8', fg='#E74C3C')
            self.errores += 1
            self.label_errores.config(text=f"❌ Errores: {self.errores}/{self.max_errores}")
            
            if self.errores >= self.max_errores:
                self.game_over()
        else:
            # Correcto
            entry.config(bg='#D5F4E6', fg='#27AE60')
            
            # Verificar si ganó
            if self.verificar_completado():
                self.root.after(500, self.victoria)
    
    def borrar_numero(self):
        """Borra el número de la celda seleccionada"""
        if not self.celda_seleccionada:
            return
        
        fila, col = self.celda_seleccionada
        entry = self.celdas[fila][col]
        
        if entry.es_fija:
            return
        
        entry.delete(0, tk.END)
        entry.config(bg='#ECF0F1', fg='#3498DB')
        self.tablero_actual[fila][col] = 0
    
    def on_numero_ingresado(self, event, fila, col):
        """Maneja el ingreso de números por teclado"""
        entry = self.celdas[fila][col]
        texto = entry.get()
        
        if not texto:
            self.tablero_actual[fila][col] = 0
            entry.config(bg='#ECF0F1', fg='#3498DB')
            return
        
        # Validar que sea un número del 1 al 9
        if not texto.isdigit() or int(texto) < 1 or int(texto) > 9:
            entry.delete(0, tk.END)
            return
        
        # Tomar solo el primer dígito
        numero = int(texto[0])
        entry.delete(0, tk.END)
        entry.insert(0, str(numero))
        
        self.insertar_numero(numero)
    
    def verificar_completado(self):
        """Verifica si el sudoku está completado correctamente"""
        for i in range(9):
            for j in range(9):
                if self.tablero_actual[i][j] != self.tablero_solucion[i][j]:
                    return False
        return True
    
    def verificar_solucion(self):
        """Verifica la solución actual"""
        if self.verificar_completado():
            self.victoria()
        else:
            # Contar aciertos
            aciertos = sum(1 for i in range(9) for j in range(9) 
                          if self.tablero_actual[i][j] == self.tablero_solucion[i][j])
            messagebox.showinfo("Verificación", 
                               f"Aún no está completo.\n\nCeldas correctas: {aciertos}/81")
    
    def victoria(self):
        """Maneja la victoria del jugador"""
        self.juego_activo = False
        
        # Calcular puntaje
        puntaje_base = {'Fácil': 100, 'Medio': 200, 'Difícil': 300, 'Experto': 500}
        puntaje = puntaje_base.get(self.dificultad_actual, 100)
        bonus = max(0, (self.max_errores - self.errores) * 100)
        puntaje_total = puntaje + bonus
        
        # Guardar puntaje
        if hasattr(app_manager, 'auth') and app_manager.auth and \
           getattr(app_manager.auth, 'usuario_actual', None) and \
           getattr(app_manager, 'database', None):
            try:
                usuario_id = app_manager.database.obtener_id_usuario(app_manager.auth.usuario_actual)
                if usuario_id:
                    app_manager.database.guardar_puntaje(
                        usuario_id,
                        "Sudoku",
                        puntaje_total,
                        dificultad=self.dificultad_actual,
                        categoria=self.dificultad_actual
                    )
            except Exception as e:
                print(f"Error guardando puntaje: {e}")
        
        mensaje = f"🎉 ¡FELICITACIONES! 🎉\n\n"
        mensaje += f"¡Completaste el Sudoku!\n\n"
        mensaje += f"🎯 Dificultad: {self.dificultad_actual}\n"
        mensaje += f"❌ Errores: {self.errores}/{self.max_errores}\n"
        mensaje += f"━━━━━━━━━━━━━━━━━\n"
        mensaje += f"💰 Puntaje: {puntaje_total}"
        
        messagebox.showinfo("¡Victoria!", mensaje)
        self.mostrar_menu_dificultad()
    
    def game_over(self):
        """Maneja la derrota del jugador"""
        self.juego_activo = False
        
        messagebox.showinfo("Game Over", 
                           f"❌ ¡Has cometido {self.max_errores} errores!\n\n"
                           f"El juego ha terminado.")
        self.mostrar_menu_dificultad()
    
    def rendirse(self):
        """Maneja la rendición del jugador"""
        if not self.juego_activo:
            return
        
        respuesta = messagebox.askyesno(
            "¿Rendirse?",
            "¿Estás seguro de que quieres rendirte?\n\n⚠️ Se revelará la solución completa."
        )
        
        if respuesta:
            self.juego_activo = False
            
            # Mostrar solución
            for i in range(9):
                for j in range(9):
                    if not self.celdas[i][j].es_fija:
                        entry = self.celdas[i][j]
                        entry.delete(0, tk.END)
                        entry.insert(0, str(self.tablero_solucion[i][j]))
                        entry.config(bg='#FADBD8', fg='#E74C3C')
            
            messagebox.showinfo("Rendido", 
                               "🏳️ TE HAS RENDIDO 🏳️\n\n"
                               "Se ha revelado la solución completa.")
            
            self.root.after(2000, self.mostrar_menu_dificultad)
    
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
    app = Sudoku(root)
    root.mainloop()