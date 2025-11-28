# torre_hanoi.py
import tkinter as tk
from tkinter import messagebox
import time
from app_manager import app_manager

class TorreHanoi:
    def __init__(self, root):
        self.root = root
        self.num_discos = 3
        self.torres = [[], [], []]
        self.movimientos = 0
        self.disco_seleccionado = None
        self.torre_origen = None
        self.juego_activo = False
        self.canvas = None
        self.animando = False
        
        # Colores para los discos
        self.colores_discos = [
            '#E74C3C', '#3498DB', '#2ECC71', '#F39C12', 
            '#9B59B6', '#1ABC9C', '#E67E22', '#34495E'
        ]
        
        self.mostrar_menu_niveles()
    
    def mostrar_menu_niveles(self):
        """Muestra el menú de selección de niveles"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Torre de Hanói - Selección de Nivel")
        self.root.geometry("700x600")
        self.root.configure(bg='#2C3E50')
        
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=40, pady=20)  # Reducí pady
        
        # Botón volver - EN LA ESQUINA SUPERIOR IZQUIERDA
        btn_volver = tk.Button(main_frame, text="← VOLVER AL MENÚ PRINCIPAL",
                  font=("Arial", 10, "bold"), bg='#95A5A6', fg='white',
                  padx=15, pady=6, cursor='hand2',  # Reducí pady
                  command=self.volver_menu_principal)
        btn_volver.place(x=0, y=0)
        
        # Título
        tk.Label(main_frame, text="🗼 TORRE DE HANÓI 🗼",
                 font=("Arial", 24, "bold"), bg='#2C3E50', fg='white', pady=15).pack()  # Reducí fuente y pady
        
        tk.Label(main_frame, text="Mueve todos los discos de la torre izquierda a la derecha",
                 font=("Arial", 12), bg='#2C3E50', fg='#BDC3C7', pady=3).pack()  # Reducí fuente y pady
        
        tk.Label(main_frame, text="Reglas: Solo un disco a la vez, nunca uno grande sobre uno pequeño",
                 font=("Arial", 10), bg='#2C3E50', fg='#95A5A6', pady=5).pack()  # Reducí fuente y pady
        
        # Frame para niveles
        frame_niveles = tk.Frame(main_frame, bg='#2C3E50')
        frame_niveles.pack(fill='both', expand=True, pady=15)  # Reducí pady
        
        niveles_info = [
            (3, "Fácil", "Mínimo 7 movimientos", '#2ECC71'),
            (4, "Medio", "Mínimo 15 movimientos", '#3498DB'),
            (5, "Difícil", "Mínimo 31 movimientos", '#F39C12'),
            (6, "Experto", "Mínimo 63 movimientos", '#E67E22'),
            (7, "Maestro", "Mínimo 127 movimientos", '#E74C3C')
        ]
        
        for discos, nivel, info, color in niveles_info:
            frame_nivel = tk.Frame(frame_niveles, bg='#34495E', relief='raised', bd=1)  # Reducí borde
            frame_nivel.pack(fill='x', pady=4, padx=50)  # Reducí pady y padx
            
            content = tk.Frame(frame_nivel, bg='#34495E')
            content.pack(fill='x', padx=15, pady=8)  # Reducí padx y pady
            
            info_frame = tk.Frame(content, bg='#34495E')
            info_frame.pack(side='left', fill='both', expand=True)
            
            tk.Label(info_frame, text=f"{discos} Discos - {nivel}",
                    font=("Arial", 12, "bold"), bg='#34495E', fg='white').pack(anchor='w')  # Reducí fuente
            
            tk.Label(info_frame, text=info,
                    font=("Arial", 9), bg='#34495E', fg='#BDC3C7').pack(anchor='w', pady=(1, 0))  # Reducí fuente y pady
            
            btn = tk.Button(content, text="JUGAR",
                           font=("Arial", 10, "bold"), bg=color, fg='white',  # Reducí fuente
                           width=10, height=1, cursor='hand2',  # Reducí width
                           command=lambda d=discos: self.iniciar_juego(d))
            btn.pack(side='right')

    # ... (el resto del código se mantiene EXACTAMENTE igual)
    def iniciar_juego(self, num_discos):
        """Inicia el juego con el número de discos seleccionado"""
        self.num_discos = num_discos
        self.movimientos = 0
        self.disco_seleccionado = None
        self.torre_origen = None
        self.juego_activo = True
        self.animando = False
        
        # Inicializar torres: todos los discos en la torre izquierda (más grande abajo)
        self.torres = [list(range(num_discos, 0, -1)), [], []]
        
        self.mostrar_pantalla_juego()
    
    def mostrar_pantalla_juego(self):
        """Muestra la pantalla principal del juego"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title(f"Torre de Hanói - {self.num_discos} Discos")
        self.root.geometry("1100x750")
        self.root.configure(bg='#34495E')
        
        main_frame = tk.Frame(self.root, bg='#34495E')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header = tk.Frame(main_frame, bg='#34495E')
        header.pack(fill='x', pady=10)
        
        tk.Label(header, text=f"🗼 Torre de Hanói - {self.num_discos} Discos",
                 font=("Arial", 18, "bold"), bg='#34495E', fg='white').pack(side='left')
        
        self.label_movimientos = tk.Label(header, text=f"📊 Movimientos: {self.movimientos}",
                                         font=("Arial", 14, "bold"), bg='#34495E', fg='#3498DB')
        self.label_movimientos.pack(side='right', padx=20)
        
        # Movimientos mínimos
        min_movimientos = (2 ** self.num_discos) - 1
        tk.Label(header, text=f"⭐ Mínimo: {min_movimientos}",
                 font=("Arial", 12), bg='#34495E', fg='#F39C12').pack(side='right', padx=10)
        
        # Contenedor principal
        contenedor = tk.Frame(main_frame, bg='#34495E')
        contenedor.pack(fill='both', expand=True)
        
        # Canvas para las torres
        canvas_frame = tk.Frame(contenedor, bg='#2C3E50', relief='ridge', bd=3)
        canvas_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg='#ECF0F1', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Instrucciones
        instrucciones_frame = tk.Frame(main_frame, bg='#34495E')
        instrucciones_frame.pack(fill='x', pady=10)
        
        tk.Label(instrucciones_frame, text="💡 Haz clic en un disco para seleccionarlo, luego haz clic en la torre destino",
                 font=("Arial", 11, "bold"), bg='#34495E', fg='#F39C12').pack()
        
        # Botones de control
        frame_botones = tk.Frame(main_frame, bg='#34495E')
        frame_botones.pack(pady=15)
        
        tk.Button(frame_botones, text="🔄 REINICIAR",
                 font=("Arial", 10, "bold"), bg='#3498DB', fg='white',
                 width=14, height=2, cursor='hand2',
                 command=lambda: self.iniciar_juego(self.num_discos)).pack(side='left', padx=5)
        
        tk.Button(frame_botones, text="📋 NIVELES",
                 font=("Arial", 10, "bold"), bg='#9B59B6', fg='white',
                 width=14, height=2, cursor='hand2',
                 command=self.mostrar_menu_niveles).pack(side='left', padx=5)
        
        tk.Button(frame_botones, text="🏳️ RENDIRSE",
                 font=("Arial", 10, "bold"), bg='#E74C3C', fg='white',
                 width=14, height=2, cursor='hand2',
                 command=self.rendirse).pack(side='left', padx=5)
        
        # Bind clicks en el canvas
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.canvas.bind('<Configure>', lambda e: self.dibujar_torres())
        
        # Dibujar estado inicial
        self.root.update()
        self.dibujar_torres()
    
    def dibujar_torres(self):
        """Dibuja las tres torres y los discos"""
        if not self.canvas:
            return
        
        self.canvas.delete('all')
        
        # Obtener dimensiones del canvas
        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()
        
        if ancho <= 1 or alto <= 1:
            return
        
        # Calcular posiciones
        espacio_torre = ancho // 3
        base_y = alto - 50
        altura_torre = alto - 150
        ancho_base = 200
        
        # Dibujar las tres torres
        for i in range(3):
            x_centro = espacio_torre * i + espacio_torre // 2
            
            # Base de la torre
            self.canvas.create_rectangle(
                x_centro - ancho_base // 2, base_y - 10,
                x_centro + ancho_base // 2, base_y + 10,
                fill='#8B4513', outline='#654321', width=2
            )
            
            # Palo vertical
            self.canvas.create_rectangle(
                x_centro - 8, base_y - altura_torre,
                x_centro + 8, base_y - 10,
                fill='#A0522D', outline='#654321', width=2
            )
            
            # Etiqueta de la torre
            nombres = ['ORIGEN', 'AUXILIAR', 'DESTINO']
            colores_label = ['#E74C3C', '#F39C12', '#2ECC71']
            self.canvas.create_text(
                x_centro, base_y + 35,
                text=nombres[i], font=("Arial", 12, "bold"),
                fill=colores_label[i]
            )
            
            # Dibujar discos en esta torre
            for j, disco in enumerate(self.torres[i]):
                self.dibujar_disco(i, j, disco, x_centro, base_y, ancho_base)
    
    def dibujar_disco(self, torre_idx, posicion, tamaño_disco, x_centro, base_y, ancho_base):
        """Dibuja un disco individual"""
        # Calcular ancho del disco (proporcional a su tamaño)
        ancho_max = ancho_base - 40
        ancho_disco = (ancho_max * tamaño_disco) // self.num_discos + 30
        
        # Altura del disco
        altura_disco = 25
        
        # Posición Y (apilados desde abajo)
        y_disco = base_y - 10 - (posicion * (altura_disco + 5))
        
        # Color del disco
        color = self.colores_discos[(tamaño_disco - 1) % len(self.colores_discos)]
        
        # Efecto de selección
        if self.disco_seleccionado == tamaño_disco and self.torre_origen == torre_idx:
            # Disco seleccionado: brillo y elevación
            y_disco -= 20
            self.canvas.create_rectangle(
                x_centro - ancho_disco // 2 - 3, y_disco - 3,
                x_centro + ancho_disco // 2 + 3, y_disco + altura_disco + 3,
                fill='#FFD700', outline='#FFA500', width=3
            )
        
        # Dibujar el disco con efecto 3D
        # Sombra
        self.canvas.create_rectangle(
            x_centro - ancho_disco // 2 + 3, y_disco + 3,
            x_centro + ancho_disco // 2 + 3, y_disco + altura_disco + 3,
            fill='#34495E', outline=''
        )
        
        # Disco principal
        disco_id = self.canvas.create_rectangle(
            x_centro - ancho_disco // 2, y_disco,
            x_centro + ancho_disco // 2, y_disco + altura_disco,
            fill=color, outline='#2C3E50', width=2,
            tags=f'disco_{torre_idx}_{tamaño_disco}'
        )
        
        # Brillo en el disco
        self.canvas.create_rectangle(
            x_centro - ancho_disco // 2 + 5, y_disco + 5,
            x_centro + ancho_disco // 2 - 5, y_disco + 10,
            fill=self.aclarar_color(color), outline='', stipple='gray50'
        )
        
        # Número en el disco
        self.canvas.create_text(
            x_centro, y_disco + altura_disco // 2,
            text=str(tamaño_disco), font=("Arial", 14, "bold"),
            fill='white'
        )
    
    def aclarar_color(self, hex_color):
        """Aclara un color para efectos de brillo"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, int(c + (255 - c) * 0.4)) for c in rgb)
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
    
    def on_canvas_click(self, event):
        """Maneja los clics en el canvas"""
        if not self.juego_activo or self.animando:
            return
        
        # Determinar en qué torre se hizo clic
        ancho = self.canvas.winfo_width()
        espacio_torre = ancho // 3
        torre_clickeada = event.x // espacio_torre
        
        if torre_clickeada >= 3:
            torre_clickeada = 2
        
        # Si no hay disco seleccionado, seleccionar uno
        if self.disco_seleccionado is None:
            if len(self.torres[torre_clickeada]) > 0:
                self.disco_seleccionado = self.torres[torre_clickeada][-1]
                self.torre_origen = torre_clickeada
                self.dibujar_torres()
        else:
            # Ya hay un disco seleccionado, intentar moverlo
            if torre_clickeada == self.torre_origen:
                # Deseleccionar
                self.disco_seleccionado = None
                self.torre_origen = None
                self.dibujar_torres()
            else:
                # Intentar mover a otra torre
                self.mover_disco(self.torre_origen, torre_clickeada)
    
    def mover_disco(self, origen, destino):
        """Intenta mover un disco de una torre a otra"""
        if len(self.torres[origen]) == 0:
            messagebox.showwarning("Movimiento inválido", "No hay discos en la torre de origen.")
            return
        
        disco = self.torres[origen][-1]
        
        # Verificar si el movimiento es válido
        if len(self.torres[destino]) > 0 and self.torres[destino][-1] < disco:
            messagebox.showwarning(
                "Movimiento inválido",
                "❌ No puedes colocar un disco grande sobre uno pequeño."
            )
            self.disco_seleccionado = None
            self.torre_origen = None
            self.dibujar_torres()
            return
        
        # Movimiento válido - animar
        self.animar_movimiento(origen, destino)
    
    def animar_movimiento(self, origen, destino):
        """Anima el movimiento de un disco"""
        self.animando = True
        
        # Realizar el movimiento
        disco = self.torres[origen].pop()
        self.torres[destino].append(disco)
        self.movimientos += 1
        
        # Actualizar interfaz
        self.label_movimientos.config(text=f"📊 Movimientos: {self.movimientos}")
        
        # Animación simple con redibujado
        for _ in range(3):
            self.dibujar_torres()
            self.root.update()
            time.sleep(0.05)
        
        # Deseleccionar disco
        self.disco_seleccionado = None
        self.torre_origen = None
        self.dibujar_torres()
        
        self.animando = False
        
        # Verificar victoria
        if len(self.torres[2]) == self.num_discos:
            self.root.after(300, self.victoria)
    
    def victoria(self):
        """Maneja la victoria del jugador"""
        self.juego_activo = False
        
        # Calcular puntaje
        min_movimientos = (2 ** self.num_discos) - 1
        
        if self.movimientos == min_movimientos:
            bonus = 1000
            calificacion = "¡PERFECTO!"
        elif self.movimientos <= min_movimientos * 1.5:
            bonus = 500
            calificacion = "¡EXCELENTE!"
        elif self.movimientos <= min_movimientos * 2:
            bonus = 250
            calificacion = "¡MUY BIEN!"
        else:
            bonus = 100
            calificacion = "¡BIEN HECHO!"
        
        puntaje = (self.num_discos * 100) + bonus
        
        # Guardar puntaje
        if hasattr(app_manager, 'auth') and app_manager.auth and \
           getattr(app_manager.auth, 'usuario_actual', None) and \
           getattr(app_manager, 'database', None):
            try:
                usuario_id = app_manager.database.obtener_id_usuario(app_manager.auth.usuario_actual)
                if usuario_id:
                    app_manager.database.guardar_puntaje(
                        usuario_id,
                        "Torre de Hanói",
                        puntaje,
                        dificultad=f"{self.num_discos} Discos",
                        categoria=f"{self.num_discos} Discos"
                    )
            except Exception as e:
                print(f"Error guardando puntaje: {e}")
        
        # Mensaje de victoria
        mensaje = f"🎉 {calificacion} 🎉\n\n"
        mensaje += f"¡Completaste la Torre de Hanói!\n\n"
        mensaje += f"🗼 Discos: {self.num_discos}\n"
        mensaje += f"📊 Movimientos: {self.movimientos}\n"
        mensaje += f"⭐ Mínimo posible: {min_movimientos}\n"
        mensaje += f"━━━━━━━━━━━━━━━━━\n"
        mensaje += f"💰 Puntaje: {puntaje}"
        
        messagebox.showinfo("¡Victoria!", mensaje)
        self.mostrar_menu_niveles()
    
    def rendirse(self):
        """Maneja la rendición del jugador"""
        if not self.juego_activo:
            return
        
        respuesta = messagebox.askyesno(
            "¿Rendirse?",
            "¿Estás seguro de que quieres rendirte?\n\n⚠️ Perderás el progreso actual."
        )
        
        if respuesta:
            self.juego_activo = False
            
            mensaje = f"🏳️ TE HAS RENDIDO 🏳️\n\n"
            mensaje += f"Movimientos realizados: {self.movimientos}\n"
            mensaje += f"Discos movidos: {len(self.torres[2])}/{self.num_discos}"
            
            messagebox.showinfo("Rendido", mensaje)
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
    app = TorreHanoi(root)
    root.mainloop()