# ahorcado.py
import tkinter as tk
from tkinter import messagebox
import random
from app_manager import app_manager

class Ahorcado:
    def __init__(self, root):
        self.root = root
        self.palabra_secreta = ""
        self.letras_adivinadas = set()
        self.letras_incorrectas = set()
        self.intentos_fallidos = 0
        self.max_intentos = 6
        self.categoria_actual = None
        self.juego_activo = False
        self.canvas = None
        
        # Categorías con palabras
        self.categorias = {
            'Animales': [
                'ELEFANTE', 'JIRAFA', 'RINOCERONTE', 'HIPOPOTAMO', 'COCODRILO',
                'LEOPARDO', 'PANTERA', 'AGUILA', 'PINGUINO', 'DELFIN',
                'BALLENA', 'TIBURON', 'MARIPOSA', 'GORILA', 'CANGURO'
            ],
            'Países': [
                'ARGENTINA', 'PARAGUAY', 'BRASIL', 'COLOMBIA', 'VENEZUELA',
                'ECUADOR', 'PERU', 'BOLIVIA', 'CHILE', 'URUGUAY',
                'MEXICO', 'ESPAÑA', 'FRANCIA', 'ALEMANIA', 'ITALIA'
            ],
            'Comida': [
                'HAMBURGUESA', 'PIZZA', 'ESPAGUETI', 'LASAGNA', 'EMPANADA',
                'MILANESA', 'ASADO', 'CHOCOLATE', 'HELADO', 'PANQUEQUE',
                'SANDWICH', 'ENSALADA', 'SUSHI', 'TACOS', 'BURRITO'
            ],
            'Deportes': [
                'FUTBOL', 'BALONCESTO', 'VOLEIBOL', 'TENIS', 'NATACION',
                'ATLETISMO', 'CICLISMO', 'BOXEO', 'GIMNASIA', 'RUGBY',
                'BEISBOL', 'HOCKEY', 'GOLF', 'KARATE', 'ESQUI'
            ],
            'Profesiones': [
                'ARQUITECTO', 'INGENIERO', 'MEDICO', 'ENFERMERO', 'PROFESOR',
                'ABOGADO', 'CONTADOR', 'PROGRAMADOR', 'DISEÑADOR', 'DENTISTA',
                'VETERINARIO', 'PSICOLOGO', 'ELECTRICISTA', 'CARPINTERO', 'CHEF'
            ]
        }
        
        self.mostrar_menu_categorias()
    
    def mostrar_menu_categorias(self):
        """Muestra el menú de selección de categorías"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Ahorcado - Selección de Categoría")
        self.root.geometry("700x650")  # Aumenté un poco la altura
        self.root.configure(bg='#2C3E50')
        
        # Frame principal con grid para mejor control
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Configurar grid weights para que el frame de botones se expanda
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Título (fila 0)
        tk.Label(main_frame, text="🎯 AHORCADO 🎯",
                 font=("Arial", 28, "bold"), bg='#2C3E50', fg='white', pady=20).grid(row=0, column=0, sticky="ew")
        
        tk.Label(main_frame, text="Selecciona una categoría:",
                 font=("Arial", 16), bg='#2C3E50', fg='#BDC3C7', pady=10).grid(row=1, column=0, sticky="n")
        
        # Frame para botones de categorías (fila 2 - se expande)
        frame_categorias = tk.Frame(main_frame, bg='#2C3E50')
        frame_categorias.grid(row=2, column=0, sticky="nsew", pady=20)
        
        colores = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6']
        
        for idx, (categoria, palabras) in enumerate(self.categorias.items()):
            color = colores[idx % len(colores)]
            
            frame_cat = tk.Frame(frame_categorias, bg='#34495E', relief='raised', bd=2)
            frame_cat.pack(fill='x', pady=8, padx=20)
            
            content = tk.Frame(frame_cat, bg='#34495E')
            content.pack(fill='x', padx=15, pady=12)
            
            tk.Label(content, text=categoria,
                    font=("Arial", 16, "bold"), bg='#34495E', fg='white').pack(side='left')
            
            tk.Label(content, text=f"({len(palabras)} palabras)",
                    font=("Arial", 11), bg='#34495E', fg='#BDC3C7').pack(side='left', padx=10)
            
            btn = tk.Button(content, text="JUGAR",
                           font=("Arial", 12, "bold"), bg=color, fg='white',
                           width=12, height=1, cursor='hand2',
                           command=lambda c=categoria: self.iniciar_juego(c))
            btn.pack(side='right')
        
        # Botón volver al menú principal (fila 3 - abajo)
        frame_volver = tk.Frame(main_frame, bg='#2C3E50')
        frame_volver.grid(row=3, column=0, sticky="s", pady=(20, 10))
        
        btn_volver = tk.Button(frame_volver, text="← VOLVER AL MENÚ PRINCIPAL",
                  font=("Arial", 12, "bold"), bg='#95A5A6', fg='white',
                  padx=30, pady=12, cursor='hand2',
                  command=self.volver_menu_principal)
        btn_volver.pack()
    
    def iniciar_juego(self, categoria):
        """Inicia el juego con la categoría seleccionada"""
        self.categoria_actual = categoria
        self.palabra_secreta = random.choice(self.categorias[categoria])
        self.letras_adivinadas = set()
        self.letras_incorrectas = set()
        self.intentos_fallidos = 0
        self.juego_activo = True
        
        self.mostrar_pantalla_juego()
    
    def mostrar_pantalla_juego(self):
        """Muestra la pantalla principal del juego"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title(f"Ahorcado - {self.categoria_actual}")
        self.root.geometry("1000x700")
        self.root.configure(bg='#34495E')
        
        main_frame = tk.Frame(self.root, bg='#34495E')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header = tk.Frame(main_frame, bg='#34495E')
        header.pack(fill='x', pady=10)
        
        tk.Label(header, text=f"🎯 {self.categoria_actual}",
                 font=("Arial", 18, "bold"), bg='#34495E', fg='white').pack(side='left')
        
        self.label_intentos = tk.Label(header, text=f"❤️ Vidas: {self.max_intentos - self.intentos_fallidos}",
                                       font=("Arial", 14, "bold"), bg='#34495E', fg='#E74C3C')
        self.label_intentos.pack(side='right', padx=20)
        
        # Contenedor principal
        contenedor = tk.Frame(main_frame, bg='#34495E')
        contenedor.pack(fill='both', expand=True)
        
        # Panel izquierdo - Canvas para el ahorcado
        panel_izq = tk.Frame(contenedor, bg='#2C3E50', relief='ridge', bd=3)
        panel_izq.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        tk.Label(panel_izq, text="👤 EL AHORCADO",
                 font=("Arial", 14, "bold"), bg='#2C3E50', fg='white', pady=10).pack()
        
        self.canvas = tk.Canvas(panel_izq, bg='#ECF0F1', width=400, height=400,
                               highlightthickness=0)
        self.canvas.pack(padx=20, pady=20)
        
        self.dibujar_horca()
        
        # Panel derecho - Controles
        panel_der = tk.Frame(contenedor, bg='#34495E', width=500)
        panel_der.pack(side='right', fill='both', expand=True)
        panel_der.pack_propagate(False)
        
        # Palabra oculta
        tk.Label(panel_der, text="📝 PALABRA:",
                 font=("Arial", 14, "bold"), bg='#34495E', fg='white', pady=10).pack()
        
        self.label_palabra = tk.Label(panel_der, text=self.obtener_palabra_oculta(),
                                      font=("Arial", 32, "bold"), bg='#34495E', fg='#3498DB',
                                      pady=20)
        self.label_palabra.pack()
        
        # Frame para entrada
        frame_entrada = tk.Frame(panel_der, bg='#34495E')
        frame_entrada.pack(pady=20)
        
        tk.Label(frame_entrada, text="Letra o Palabra:",
                 font=("Arial", 12, "bold"), bg='#34495E', fg='#BDC3C7').pack()
        
        self.entry_letra = tk.Entry(frame_entrada, font=("Arial", 16, "bold"),
                                    width=20, justify='center')
        self.entry_letra.pack(pady=10)
        self.entry_letra.focus()
        
        btn_intentar = tk.Button(frame_entrada, text="✓ INTENTAR",
                                font=("Arial", 12, "bold"), bg='#2ECC71', fg='white',
                                width=15, height=2, cursor='hand2',
                                command=self.intentar)
        btn_intentar.pack(pady=5)
        
        self.entry_letra.bind('<Return>', lambda e: self.intentar())
        
        # Letras correctas e incorrectas
        frame_letras = tk.Frame(panel_der, bg='#34495E')
        frame_letras.pack(fill='x', pady=20, padx=20)
        
        tk.Label(frame_letras, text="✓ Letras Correctas:",
                 font=("Arial", 11, "bold"), bg='#34495E', fg='#2ECC71').pack(anchor='w')
        
        self.label_correctas = tk.Label(frame_letras, text="Ninguna aún",
                                        font=("Arial", 12), bg='#34495E', fg='#2ECC71',
                                        wraplength=400, justify='left')
        self.label_correctas.pack(anchor='w', pady=5)
        
        tk.Label(frame_letras, text="✗ Letras Incorrectas:",
                 font=("Arial", 11, "bold"), bg='#34495E', fg='#E74C3C').pack(anchor='w', pady=(10, 0))
        
        self.label_incorrectas = tk.Label(frame_letras, text="Ninguna aún",
                                          font=("Arial", 12), bg='#34495E', fg='#E74C3C',
                                          wraplength=400, justify='left')
        self.label_incorrectas.pack(anchor='w', pady=5)
        
        # Botones de control en FILA
        frame_botones = tk.Frame(panel_der, bg='#34495E')
        frame_botones.pack(pady=20)
        
        tk.Button(frame_botones, text="🔄 REINICIAR",
                 font=("Arial", 10, "bold"), bg='#3498DB', fg='white',
                 width=14, height=2, cursor='hand2',
                 command=lambda: self.iniciar_juego(self.categoria_actual)).pack(side='left', padx=3)
        
        tk.Button(frame_botones, text="📋 CATEGORÍAS",
                 font=("Arial", 10, "bold"), bg='#9B59B6', fg='white',
                 width=14, height=2, cursor='hand2',
                 command=self.mostrar_menu_categorias).pack(side='left', padx=3)
        
        tk.Button(frame_botones, text="🏳️ RENDIRSE",
                 font=("Arial", 10, "bold"), bg='#E74C3C', fg='white',
                 width=14, height=2, cursor='hand2',
                 command=self.rendirse).pack(side='left', padx=3)
    
    def obtener_palabra_oculta(self):
        """Devuelve la palabra con las letras adivinadas"""
        resultado = ""
        for letra in self.palabra_secreta:
            if letra in self.letras_adivinadas:
                resultado += letra + " "
            else:
                resultado += "_ "
        return resultado.strip()
    
    def intentar(self):
        """Procesa un intento del usuario"""
        if not self.juego_activo:
            return
        
        intento = self.entry_letra.get().upper().strip()
        self.entry_letra.delete(0, tk.END)
        
        if not intento:
            messagebox.showwarning("Advertencia", "Debes escribir una letra o palabra.")
            return
        
        # Validar que solo sean letras
        if not intento.replace('Ñ', 'N').isalpha():
            messagebox.showwarning("Advertencia", "Solo se permiten letras.")
            return
        
        # Caso 1: Intento de palabra completa
        if len(intento) > 1:
            if intento == self.palabra_secreta:
                # ¡Adivinó la palabra completa!
                self.letras_adivinadas.update(self.palabra_secreta)
                self.actualizar_interfaz()
                self.victoria()
            else:
                # Palabra incorrecta
                self.intentos_fallidos += 1
                self.actualizar_interfaz()
                
                if self.intentos_fallidos >= self.max_intentos:
                    self.game_over()
                else:
                    messagebox.showinfo("Incorrecto", f"❌ '{intento}' no es la palabra correcta.\n\nPerdiste una vida.")
        
        # Caso 2: Intento de letra
        else:
            letra = intento
            
            # Verificar si ya fue intentada
            if letra in self.letras_adivinadas or letra in self.letras_incorrectas:
                messagebox.showinfo("Ya intentada", f"Ya intentaste la letra '{letra}'.")
                return
            
            # Verificar si está en la palabra
            if letra in self.palabra_secreta:
                self.letras_adivinadas.add(letra)
                self.actualizar_interfaz()
                
                # Verificar victoria
                if all(l in self.letras_adivinadas for l in self.palabra_secreta):
                    self.victoria()
            else:
                self.letras_incorrectas.add(letra)
                self.intentos_fallidos += 1
                self.actualizar_interfaz()
                
                if self.intentos_fallidos >= self.max_intentos:
                    self.game_over()
    
    def actualizar_interfaz(self):
        """Actualiza todos los elementos de la interfaz"""
        # Actualizar palabra
        self.label_palabra.config(text=self.obtener_palabra_oculta())
        
        # Actualizar vidas
        self.label_intentos.config(text=f"❤️ Vidas: {self.max_intentos - self.intentos_fallidos}")
        
        # Actualizar letras correctas
        if self.letras_adivinadas:
            correctas = ", ".join(sorted(self.letras_adivinadas))
            self.label_correctas.config(text=correctas)
        else:
            self.label_correctas.config(text="Ninguna aún")
        
        # Actualizar letras incorrectas
        if self.letras_incorrectas:
            incorrectas = ", ".join(sorted(self.letras_incorrectas))
            self.label_incorrectas.config(text=incorrectas)
        else:
            self.label_incorrectas.config(text="Ninguna aún")
        
        # Dibujar parte del ahorcado
        self.dibujar_ahorcado(self.intentos_fallidos)
    
    def dibujar_horca(self):
        """Dibuja la horca base"""
        self.canvas.delete('all')
        
        # Base
        self.canvas.create_line(50, 350, 200, 350, width=5, fill='#8B4513')
        # Poste vertical
        self.canvas.create_line(100, 350, 100, 50, width=5, fill='#8B4513')
        # Poste horizontal
        self.canvas.create_line(100, 50, 250, 50, width=5, fill='#8B4513')
        # Cuerda
        self.canvas.create_line(250, 50, 250, 100, width=3, fill='#8B4513')
    
    def dibujar_ahorcado(self, intentos):
        """Dibuja las partes del ahorcado según los intentos fallidos"""
        self.dibujar_horca()
        
        if intentos >= 1:
            # Cabeza
            self.canvas.create_oval(220, 100, 280, 160, width=3, outline='#2C3E50', fill='#FFF8DC')
            # Ojos X
            self.canvas.create_line(235, 120, 245, 130, width=3, fill='#E74C3C')
            self.canvas.create_line(245, 120, 235, 130, width=3, fill='#E74C3C')
            self.canvas.create_line(255, 120, 265, 130, width=3, fill='#E74C3C')
            self.canvas.create_line(265, 120, 255, 130, width=3, fill='#E74C3C')
            # Boca triste
            self.canvas.create_arc(235, 135, 265, 155, start=0, extent=-180, width=2, outline='#2C3E50', style='arc')
        
        if intentos >= 2:
            # Cuerpo
            self.canvas.create_line(250, 160, 250, 250, width=4, fill='#2C3E50')
        
        if intentos >= 3:
            # Brazo izquierdo
            self.canvas.create_line(250, 180, 210, 220, width=3, fill='#2C3E50')
        
        if intentos >= 4:
            # Brazo derecho
            self.canvas.create_line(250, 180, 290, 220, width=3, fill='#2C3E50')
        
        if intentos >= 5:
            # Pierna izquierda
            self.canvas.create_line(250, 250, 220, 310, width=3, fill='#2C3E50')
        
        if intentos >= 6:
            # Pierna derecha
            self.canvas.create_line(250, 250, 280, 310, width=3, fill='#2C3E50')
    
    def victoria(self):
        """Maneja la victoria del jugador"""
        self.juego_activo = False
        
        # Dibujar cara feliz
        self.canvas.delete('all')
        self.dibujar_horca()
        
        # Cara feliz grande
        self.canvas.create_oval(170, 150, 330, 310, width=5, outline='#2ECC71', fill='#D5F4E6')
        # Ojos felices
        self.canvas.create_oval(200, 190, 220, 210, fill='#2C3E50')
        self.canvas.create_oval(280, 190, 300, 210, fill='#2C3E50')
        # Sonrisa HACIA ARRIBA
        self.canvas.create_arc(210, 220, 290, 270, start=180, extent=180, width=4, outline='#2C3E50', style='arc')
        
        # Calcular puntaje
        puntaje = (len(self.palabra_secreta) * 10) + ((self.max_intentos - self.intentos_fallidos) * 20)
        
        # Guardar puntaje
        if hasattr(app_manager, 'auth') and app_manager.auth and \
           getattr(app_manager.auth, 'usuario_actual', None) and \
           getattr(app_manager, 'database', None):
            try:
                usuario_id = app_manager.database.obtener_id_usuario(app_manager.auth.usuario_actual)
                if usuario_id:
                    app_manager.database.guardar_puntaje(
                        usuario_id,
                        "Ahorcado",
                        puntaje,
                        dificultad="Media",
                        categoria=self.categoria_actual
                    )
            except Exception as e:
                print(f"Error guardando puntaje: {e}")
        
        mensaje = f"🎉 ¡FELICITACIONES! 🎉\n\n"
        mensaje += f"Adivinaste la palabra:\n\n'{self.palabra_secreta}'\n\n"
        mensaje += f"💚 Vidas restantes: {self.max_intentos - self.intentos_fallidos}\n"
        mensaje += f"⭐ Puntaje: {puntaje}"
        
        messagebox.showinfo("¡Victoria!", mensaje)
        self.mostrar_menu_categorias()
    
    def rendirse(self):
        """Maneja la rendición del jugador"""
        if not self.juego_activo:
            return
        
        respuesta = messagebox.askyesno(
            "¿Rendirse?",
            "¿Estás seguro de que quieres rendirte?\n\n⚠️ Perderás la partida y se revelará la palabra."
        )
        
        if respuesta:
            self.juego_activo = False
            
            # Completar el muñeco
            self.intentos_fallidos = self.max_intentos
            self.dibujar_ahorcado(self.intentos_fallidos)
            
            # Revelar toda la palabra
            self.label_palabra.config(text=" ".join(self.palabra_secreta), fg='#E74C3C')
            
            # Actualizar vidas
            self.label_intentos.config(text=f"❤️ Vidas: 0")
            
            # Mostrar mensaje
            mensaje = f"🏳️ TE HAS RENDIDO 🏳️\n\n"
            mensaje += f"Has perdido la partida.\n\n"
            mensaje += f"La palabra era:\n\n'{self.palabra_secreta}'"
            
            messagebox.showinfo("Rendido", mensaje)
            self.mostrar_menu_categorias()
    
    def game_over(self):
        """Maneja la derrota del jugador"""
        self.juego_activo = False
        
        mensaje = f"😢 GAME OVER 😢\n\n"
        mensaje += f"Te quedaste sin vidas.\n\n"
        mensaje += f"La palabra era:\n\n'{self.palabra_secreta}'"
        
        messagebox.showinfo("Perdiste", mensaje)
        self.mostrar_menu_categorias()
    
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
    app = Ahorcado(root)
    root.mainloop()