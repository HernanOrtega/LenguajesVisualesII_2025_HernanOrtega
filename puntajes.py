# puntajes.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class SistemaPuntajes:
    def __init__(self, root, database, auth):
        self.root = root
        self.database = database
        self.auth = auth
        self.juego_actual = None
        
        self.mostrar_menu_principal()
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal del sistema de puntajes"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Sistema de Puntajes")
        self.root.geometry("900x700")
        self.root.configure(bg='#2C3E50')
        
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=30, pady=15)  # Reducido de 20 a 15
        
        # Botón volver
        tk.Button(main_frame, text="← VOLVER AL MENÚ",
                 font=("Arial", 10, "bold"), bg='#95A5A6', fg='white',
                 padx=12, pady=4, cursor='hand2',  # Reducido padding
                 command=self.volver_menu_principal).pack(anchor='nw', pady=(0, 10))  # Reducido pady
        
        # Título
        tk.Label(main_frame, text="🏆 SISTEMA DE PUNTAJES 🏆",
                 font=("Arial", 26, "bold"), bg='#2C3E50', fg='white',  # Reducido de 28 a 26
                 pady=15).pack()  # Reducido de 20 a 15
        
        # Información del usuario
        if self.auth and self.auth.usuario_actual:
            tk.Label(main_frame, text=f"👤 Usuario: {self.auth.usuario_actual}",
                    font=("Arial", 12, "bold"), bg='#2C3E50', fg='#2ECC71',  # Reducido de 14 a 12
                    pady=5).pack()  # Reducido de 10 a 5
        else:
            tk.Label(main_frame, text="⚠️ Debes iniciar sesión para ver tus puntajes",
                    font=("Arial", 11, "bold"), bg='#2C3E50', fg='#E74C3C',  # Reducido de 12 a 11
                    pady=5).pack()  # Reducido de 10 a 5
        
        # Frame para botones de opciones
        frame_opciones = tk.Frame(main_frame, bg='#2C3E50')
        frame_opciones.pack(fill='both', expand=True, pady=20)  # Reducido de 30 a 20
        
        # Opciones disponibles
        opciones = [
            ("🌟 RANKING GENERAL", "Ver top 10 de todos los juegos", self.mostrar_ranking_general, '#3498DB'),
            ("🎮 RANKING POR JUEGO", "Ver ranking de un juego específico", self.mostrar_menu_juegos, '#9B59B6'),
            ("📊 MIS PUNTAJES", "Ver todos tus puntajes personales", self.mostrar_mis_puntajes, '#2ECC71'),
            ("📈 ESTADÍSTICAS", "Ver estadísticas detalladas", self.mostrar_estadisticas, '#F39C12')
        ]
        
        for titulo, descripcion, comando, color in opciones:
            frame_opcion = tk.Frame(frame_opciones, bg='#34495E', relief='raised', bd=2)
            frame_opcion.pack(fill='x', pady=8, padx=50)  # Reducido pady de 10 a 8
            
            content = tk.Frame(frame_opcion, bg='#34495E')
            content.pack(fill='x', padx=15, pady=12)  # Reducido pady de 15 a 12
            
            info_frame = tk.Frame(content, bg='#34495E')
            info_frame.pack(side='left', fill='both', expand=True)
            
            tk.Label(info_frame, text=titulo,
                    font=("Arial", 13, "bold"), bg='#34495E', fg='white').pack(anchor='w')  # Reducido de 14 a 13
            
            tk.Label(info_frame, text=descripcion,
                    font=("Arial", 9), bg='#34495E', fg='#BDC3C7').pack(anchor='w', pady=(2, 0))  # Reducido fuente y padding
            
            btn = tk.Button(content, text="VER",
                           font=("Arial", 10, "bold"), bg=color, fg='white',  # Reducido de 11 a 10
                           width=10, height=1, cursor='hand2',  # Reducido width de 12 a 10
                           command=comando)
            btn.pack(side='right')
    
    def mostrar_ranking_general(self):
        """Muestra el ranking general de todos los juegos"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Ranking General - Top 10")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2C3E50')
        
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=30, pady=15)  # Reducido de 20 a 15
        
        # Header
        header = tk.Frame(main_frame, bg='#2C3E50')
        header.pack(fill='x', pady=(0, 15))  # Reducido de 20 a 15
        
        tk.Button(header, text="← VOLVER",
                 font=("Arial", 10, "bold"), bg='#95A5A6', fg='white',
                 padx=12, pady=4, cursor='hand2',  # Reducido padding
                 command=self.mostrar_menu_principal).pack(side='left')
        
        tk.Label(header, text="🏆 RANKING GENERAL - TOP 10",
                 font=("Arial", 18, "bold"), bg='#2C3E50', fg='white').pack()  # Reducido de 20 a 18
        
        # Frame para la tabla
        frame_tabla = tk.Frame(main_frame, bg='#34495E', relief='ridge', bd=2)
        frame_tabla.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear Treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", 
                       background="#ECF0F1",
                       foreground="#2C3E50",
                       rowheight=35,
                       fieldbackground="#ECF0F1",
                       font=('Arial', 11))
        style.configure("Treeview.Heading",
                       background="#34495E",
                       foreground="white",
                       font=('Arial', 12, 'bold'))
        style.map('Treeview', background=[('selected', '#3498DB')])
        
        columns = ("Pos", "Usuario", "Juego", "Puntaje", "Dificultad", "Fecha")
        tree = ttk.Treeview(frame_tabla, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        tree.heading("Pos", text="🏅 Pos")
        tree.heading("Usuario", text="👤 Usuario")
        tree.heading("Juego", text="🎮 Juego")
        tree.heading("Puntaje", text="⭐ Puntaje")
        tree.heading("Dificultad", text="📊 Dificultad")
        tree.heading("Fecha", text="📅 Fecha")
        
        tree.column("Pos", width=60, anchor='center')
        tree.column("Usuario", width=150, anchor='w')
        tree.column("Juego", width=180, anchor='w')
        tree.column("Puntaje", width=100, anchor='center')
        tree.column("Dificultad", width=120, anchor='center')
        tree.column("Fecha", width=150, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Obtener datos
        try:
            puntajes = self.database.obtener_ranking(limite=10)
            
            if not puntajes:
                tk.Label(frame_tabla, text="📭 No hay puntajes registrados aún",
                        font=("Arial", 14, "bold"), bg='#34495E', fg='#95A5A6',
                        pady=50).pack(fill='both', expand=True)
            else:
                for idx, registro in enumerate(puntajes, 1):
                    username, puntaje, juego, dificultad, categoria, fecha = registro
                    
                    # Formatear fecha
                    try:
                        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
                        fecha_formato = fecha_obj.strftime('%d/%m/%Y %H:%M')
                    except:
                        fecha_formato = fecha
                    
                    # Emoji de medalla para top 3
                    if idx == 1:
                        pos = "🥇"
                    elif idx == 2:
                        pos = "🥈"
                    elif idx == 3:
                        pos = "🥉"
                    else:
                        pos = str(idx)
                    
                    dif_texto = dificultad if dificultad else "-"
                    
                    tree.insert("", "end", values=(
                        pos, username, juego, f"{puntaje:,}", dif_texto, fecha_formato
                    ))
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar ranking: {e}")
    
    def mostrar_menu_juegos(self):
        """Muestra menú para seleccionar juego CON SCROLL"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Seleccionar Juego")
        self.root.geometry("700x650")
        self.root.configure(bg='#2C3E50')
        
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=30, pady=15)  # Reducido de 20 a 15
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#2C3E50')
        header_frame.pack(fill='x', pady=(0, 15))  # Reducido pady
        
        tk.Button(header_frame, text="← VOLVER",
                 font=("Arial", 10, "bold"), bg='#95A5A6', fg='white',
                 padx=12, pady=4, cursor='hand2',  # Reducido padding
                 command=self.mostrar_menu_principal).pack(anchor='nw')
        
        tk.Label(header_frame, text="🎮 SELECCIONA UN JUEGO",
                 font=("Arial", 20, "bold"), bg='#2C3E50', fg='white',  # Reducido de 22 a 20
                 pady=15).pack()  # Reducido de 20 a 15
        
        # Frame para juegos CON SCROLL
        frame_contenedor = tk.Frame(main_frame, bg='#2C3E50')
        frame_contenedor.pack(fill='both', expand=True)
        
        # Canvas con scrollbar
        canvas = tk.Canvas(frame_contenedor, bg='#2C3E50', highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_contenedor, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        # Frame interior para los juegos
        frame_juegos = tk.Frame(canvas, bg='#2C3E50')
        canvas_frame = canvas.create_window((0, 0), window=frame_juegos, anchor='nw', width=canvas.winfo_reqwidth())
        
        # Lista de juegos
        juegos = [
            ("Sopa de Letras", "🔤", '#E74C3C'),
            ("Crucigrama", "🧩", '#3498DB'),
            ("Buscaminas", "💣", '#2ECC71'),
            ("Conecta Puntos", "🔴", '#9B59B6'),
            ("Laberinto", "🧭", '#E67E22'),
            ("Ahorcado", "🎯", '#1ABC9C'),
            ("Torre de Hanói", "🗼", '#16A085'),
            ("Sudoku", "🔢", '#8E44AD'),
            ("Pong", "🏓", '#3498DB')
        ]
        
        for juego, emoji, color in juegos:
            frame_juego = tk.Frame(frame_juegos, bg='#34495E', relief='raised', bd=2)
            frame_juego.pack(fill='x', pady=5, padx=50)  # Reducido pady de 6 a 5
            
            content = tk.Frame(frame_juego, bg='#34495E')
            content.pack(fill='x', padx=12, pady=8)  # Reducido padding
            
            tk.Label(content, text=f"{emoji} {juego}",
                    font=("Arial", 12, "bold"), bg='#34495E', fg='white').pack(side='left')  # Reducido de 13 a 12
            
            btn = tk.Button(content, text="VER RANKING",
                           font=("Arial", 9, "bold"), bg=color, fg='white',  # Reducido de 10 a 9
                           width=12, cursor='hand2',  # Reducido width de 14 a 12
                           command=lambda j=juego: self.mostrar_ranking_juego(j))
            btn.pack(side='right')
        
        # Configurar scroll
        frame_juegos.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        # Configurar ancho del canvas interior
        def configurar_ancho(event):
            canvas.itemconfig(canvas_frame, width=event.width)
        
        canvas.bind('<Configure>', configurar_ancho)
    
    def mostrar_ranking_juego(self, juego):
        """Muestra el ranking de un juego específico"""
        self.juego_actual = juego
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title(f"Ranking - {juego}")
        self.root.geometry("950x700")
        self.root.configure(bg='#2C3E50')
        
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=30, pady=15)  # Reducido de 20 a 15
        
        # Header
        header = tk.Frame(main_frame, bg='#2C3E50')
        header.pack(fill='x', pady=(0, 15))  # Reducido de 20 a 15
        
        tk.Button(header, text="← VOLVER",
                 font=("Arial", 10, "bold"), bg='#95A5A6', fg='white',
                 padx=12, pady=4, cursor='hand2',  # Reducido padding
                 command=self.mostrar_menu_juegos).pack(side='left')
        
        tk.Label(header, text=f"🏆 RANKING - {juego.upper()}",
                 font=("Arial", 16, "bold"), bg='#2C3E50', fg='white').pack()  # Reducido de 18 a 16
        
        # Frame para tabla
        frame_tabla = tk.Frame(main_frame, bg='#34495E', relief='ridge', bd=2)
        frame_tabla.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", 
                       background="#ECF0F1",
                       foreground="#2C3E50",
                       rowheight=35,
                       fieldbackground="#ECF0F1",
                       font=('Arial', 11))
        style.configure("Treeview.Heading",
                       background="#34495E",
                       foreground="white",
                       font=('Arial', 12, 'bold'))
        style.map('Treeview', background=[('selected', '#3498DB')])
        
        columns = ("Pos", "Usuario", "Puntaje", "Dificultad", "Categoría", "Fecha")
        tree = ttk.Treeview(frame_tabla, columns=columns, show='headings', height=15)
        
        tree.heading("Pos", text="🏅 Pos")
        tree.heading("Usuario", text="👤 Usuario")
        tree.heading("Puntaje", text="⭐ Puntaje")
        tree.heading("Dificultad", text="📊 Dificultad")
        tree.heading("Categoría", text="📁 Categoría")
        tree.heading("Fecha", text="📅 Fecha")
        
        tree.column("Pos", width=60, anchor='center')
        tree.column("Usuario", width=150, anchor='w')
        tree.column("Puntaje", width=120, anchor='center')
        tree.column("Dificultad", width=120, anchor='center')
        tree.column("Categoría", width=150, anchor='center')
        tree.column("Fecha", width=150, anchor='center')
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Cargar datos
        try:
            puntajes = self.database.obtener_ranking(juego=juego, limite=20)
            
            if not puntajes:
                tk.Label(frame_tabla, text=f"📭 No hay puntajes para {juego} aún",
                        font=("Arial", 14, "bold"), bg='#34495E', fg='#95A5A6',
                        pady=50).pack(fill='both', expand=True)
            else:
                for idx, registro in enumerate(puntajes, 1):
                    username, puntaje, dificultad, categoria, fecha = registro
                    
                    try:
                        fecha_obj = datetime.strptime(fecha, '%Y-%m-d %H:%M:%S')
                        fecha_formato = fecha_obj.strftime('%d/%m/%Y %H:%M')
                    except:
                        fecha_formato = fecha
                    
                    if idx == 1:
                        pos = "🥇"
                    elif idx == 2:
                        pos = "🥈"
                    elif idx == 3:
                        pos = "🥉"
                    else:
                        pos = str(idx)
                    
                    dif_texto = dificultad if dificultad else "-"
                    cat_texto = categoria if categoria else "-"
                    
                    tree.insert("", "end", values=(
                        pos, username, f"{puntaje:,}", dif_texto, cat_texto, fecha_formato
                    ))
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar ranking: {e}")
    
    def mostrar_mis_puntajes(self):
        """Muestra los puntajes personales del usuario"""
        if not self.auth or not self.auth.usuario_actual:
            messagebox.showwarning("Aviso", "Debes iniciar sesión para ver tus puntajes")
            return
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Mis Puntajes")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2C3E50')
        
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=30, pady=15)  # Reducido de 20 a 15
        
        # Header
        header = tk.Frame(main_frame, bg='#2C3E50')
        header.pack(fill='x', pady=(0, 15))  # Reducido de 20 a 15
        
        tk.Button(header, text="← VOLVER",
                 font=("Arial", 10, "bold"), bg='#95A5A6', fg='white',
                 padx=12, pady=4, cursor='hand2',  # Reducido padding
                 command=self.mostrar_menu_principal).pack(side='left')
        
        tk.Label(header, text=f"📊 MIS PUNTAJES - {self.auth.usuario_actual}",
                 font=("Arial", 16, "bold"), bg='#2C3E50', fg='white').pack()  # Reducido de 18 a 16
        
        # Frame para tabla
        frame_tabla = tk.Frame(main_frame, bg='#34495E', relief='ridge', bd=2)
        frame_tabla.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", 
                       background="#ECF0F1",
                       foreground="#2C3E50",
                       rowheight=35,
                       fieldbackground="#ECF0F1",
                       font=('Arial', 11))
        style.configure("Treeview.Heading",
                       background="#34495E",
                       foreground="white",
                       font=('Arial', 12, 'bold'))
        style.map('Treeview', background=[('selected', '#3498DB')])
        
        columns = ("ID", "Juego", "Puntaje", "Dificultad", "Categoría", "Fecha")
        tree = ttk.Treeview(frame_tabla, columns=columns, show='headings', height=15)
        
        tree.heading("ID", text="#")
        tree.heading("Juego", text="🎮 Juego")
        tree.heading("Puntaje", text="⭐ Puntaje")
        tree.heading("Dificultad", text="📊 Dificultad")
        tree.heading("Categoría", text="📁 Categoría")
        tree.heading("Fecha", text="📅 Fecha")
        
        tree.column("ID", width=50, anchor='center')
        tree.column("Juego", width=180, anchor='w')
        tree.column("Puntaje", width=120, anchor='center')
        tree.column("Dificultad", width=120, anchor='center')
        tree.column("Categoría", width=150, anchor='center')
        tree.column("Fecha", width=180, anchor='center')
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Cargar datos del usuario
        try:
            usuario_id = self.database.obtener_id_usuario(self.auth.usuario_actual)
            if not usuario_id:
                tk.Label(frame_tabla, text="❌ Error al obtener datos del usuario",
                        font=("Arial", 14, "bold"), bg='#34495E', fg='#E74C3C',
                        pady=50).pack(fill='both', expand=True)
                return
            
            # Obtener todos los puntajes del usuario
            conexion = self.database.get_conexion()
            cursor = conexion.cursor()
            cursor.execute('''
                SELECT id, juego, puntaje, dificultad, categoria, fecha
                FROM puntajes
                WHERE usuario_id = ?
                ORDER BY fecha DESC
                LIMIT 100
            ''', (usuario_id,))
            puntajes = cursor.fetchall()
            conexion.close()
            
            if not puntajes:
                tk.Label(frame_tabla, text="📭 Aún no tienes puntajes registrados\n\n¡Juega y establece tu primer récord!",
                        font=("Arial", 14, "bold"), bg='#34495E', fg='#95A5A6',
                        pady=50).pack(fill='both', expand=True)
            else:
                for registro in puntajes:
                    id_p, juego, puntaje, dificultad, categoria, fecha = registro
                    
                    try:
                        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
                        fecha_formato = fecha_obj.strftime('%d/%m/%Y %H:%M')
                    except:
                        fecha_formato = fecha
                    
                    dif_texto = dificultad if dificultad else "-"
                    cat_texto = categoria if categoria else "-"
                    
                    tree.insert("", "end", values=(
                        id_p, juego, f"{puntaje:,}", dif_texto, cat_texto, fecha_formato
                    ))
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar puntajes: {e}")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas generales del usuario"""
        if not self.auth or not self.auth.usuario_actual:
            messagebox.showwarning("Aviso", "Debes iniciar sesión para ver estadísticas")
            return
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Mis Estadísticas")
        self.root.geometry("900x700")
        self.root.configure(bg='#2C3E50')
        
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=30, pady=15)  # Reducido de 20 a 15
        
        # Header
        header = tk.Frame(main_frame, bg='#2C3E50')
        header.pack(fill='x', pady=(0, 15))  # Reducido de 20 a 15
        
        tk.Button(header, text="← VOLVER",
                 font=("Arial", 10, "bold"), bg='#95A5A6', fg='white',
                 padx=12, pady=4, cursor='hand2',  # Reducido padding
                 command=self.mostrar_menu_principal).pack(side='left')
        
        tk.Label(header, text=f"📈 ESTADÍSTICAS - {self.auth.usuario_actual}",
                 font=("Arial", 16, "bold"), bg='#2C3E50', fg='white').pack()  # Reducido de 18 a 16
        
        # Obtener estadísticas
        try:
            usuario_id = self.database.obtener_id_usuario(self.auth.usuario_actual)
            if not usuario_id:
                return
            
            conexion = self.database.get_conexion()
            cursor = conexion.cursor()
            
            # Total de partidas
            cursor.execute('SELECT COUNT(*) FROM puntajes WHERE usuario_id = ?', (usuario_id,))
            total_partidas = cursor.fetchone()[0]
            
            # Puntaje total acumulado
            cursor.execute('SELECT SUM(puntaje) FROM puntajes WHERE usuario_id = ?', (usuario_id,))
            puntaje_total = cursor.fetchone()[0] or 0
            
            # Puntaje promedio
            puntaje_promedio = puntaje_total // total_partidas if total_partidas > 0 else 0
            
            # Mejor puntaje
            cursor.execute('SELECT MAX(puntaje), juego FROM puntajes WHERE usuario_id = ?', (usuario_id,))
            mejor_resultado = cursor.fetchone()
            mejor_puntaje = mejor_resultado[0] or 0
            mejor_juego = mejor_resultado[1] or "-"
            
            # Juego más jugado
            cursor.execute('''
                SELECT juego, COUNT(*) as veces
                FROM puntajes
                WHERE usuario_id = ?
                GROUP BY juego
                ORDER BY veces DESC
                LIMIT 1
            ''', (usuario_id,))
            juego_mas_jugado_resultado = cursor.fetchone()
            if juego_mas_jugado_resultado:
                juego_mas_jugado = juego_mas_jugado_resultado[0]
                veces_jugado = juego_mas_jugado_resultado[1]
            else:
                juego_mas_jugado = "-"
                veces_jugado = 0
            
            # Estadísticas por juego
            cursor.execute('''
                SELECT juego, COUNT(*) as partidas, SUM(puntaje) as total, MAX(puntaje) as mejor
                FROM puntajes
                WHERE usuario_id = ?
                GROUP BY juego
                ORDER BY total DESC
            ''', (usuario_id,))
            stats_por_juego = cursor.fetchall()
            
            conexion.close()
            
            # Mostrar estadísticas generales
            frame_general = tk.Frame(main_frame, bg='#34495E', relief='ridge', bd=2)
            frame_general.pack(fill='x', padx=10, pady=10)
            
            tk.Label(frame_general, text="📊 RESUMEN GENERAL",
                    font=("Arial", 14, "bold"), bg='#34495E', fg='white',
                    pady=15).pack()
            
            stats_frame = tk.Frame(frame_general, bg='#34495E')
            stats_frame.pack(fill='x', padx=30, pady=10)
            
            stats = [
                ("🎮 Total de Partidas:", f"{total_partidas}", '#3498DB'),
                ("⭐ Puntaje Total:", f"{puntaje_total:,}", '#F39C12'),
                ("📊 Promedio:", f"{puntaje_promedio:,}", '#9B59B6'),
                ("🏆 Mejor Puntaje:", f"{mejor_puntaje:,} ({mejor_juego})", '#2ECC71'),
                ("🎯 Juego Favorito:", f"{juego_mas_jugado} ({veces_jugado} veces)", '#E74C3C')
            ]
            
            for label, valor, color in stats:
                f = tk.Frame(stats_frame, bg='#2C3E50', relief='solid', bd=1)
                f.pack(fill='x', pady=5)
                
                tk.Label(f, text=label, font=("Arial", 11, "bold"),
                        bg='#2C3E50', fg='white', anchor='w',
                        padx=15, pady=8).pack(side='left', fill='x', expand=True)
                
                tk.Label(f, text=valor, font=("Arial", 11, "bold"),
                        bg='#2C3E50', fg=color, anchor='e',
                        padx=15, pady=8).pack(side='right')
            
            # Estadísticas por juego
            if stats_por_juego:
                frame_juegos = tk.Frame(main_frame, bg='#34495E', relief='ridge', bd=2)
                frame_juegos.pack(fill='both', expand=True, padx=10, pady=10)
                
                tk.Label(frame_juegos, text="🎮 ESTADÍSTICAS POR JUEGO",
                        font=("Arial", 14, "bold"), bg='#34495E', fg='white',
                        pady=15).pack()
                
                # Crear tabla
                columns = ("Juego", "Partidas", "Puntaje Total", "Mejor Puntaje")
                tree = ttk.Treeview(frame_juegos, columns=columns, show='headings', height=8)
                
                tree.heading("Juego", text="🎮 Juego")
                tree.heading("Partidas", text="📊 Partidas")
                tree.heading("Puntaje Total", text="⭐ Total")
                tree.heading("Mejor Puntaje", text="🏆 Mejor")
                
                tree.column("Juego", width=200, anchor='w')
                tree.column("Partidas", width=100, anchor='center')
                tree.column("Puntaje Total", width=150, anchor='center')
                tree.column("Mejor Puntaje", width=150, anchor='center')
                
                scrollbar = ttk.Scrollbar(frame_juegos, orient="vertical", command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)
                
                scrollbar.pack(side='right', fill='y', padx=10)
                tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
                
                for juego, partidas, total, mejor in stats_por_juego:
                    tree.insert("", "end", values=(
                        juego, partidas, f"{total:,}", f"{mejor:,}"
                    ))
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar estadísticas: {e}")
    
    def volver_menu_principal(self):
        """Vuelve al menú principal de la aplicación"""
        try:
            from menu_principal import MenuPrincipal
            for widget in self.root.winfo_children():
                widget.destroy()
            
            from app_manager import app_manager
            MenuPrincipal(self.root, app_manager.auth, app_manager.database)
        except Exception as e:
            print(f"Error volviendo al menú: {e}")
            self.root.quit()


# Test
if __name__ == "__main__":
    root = tk.Tk()
    from database import Database
    from auth import AuthManager
    
    db = Database()
    auth = AuthManager(db)
    
    app = SistemaPuntajes(root, db, auth)
    root.mainloop()