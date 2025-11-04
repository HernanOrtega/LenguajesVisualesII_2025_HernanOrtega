# auth.py
import tkinter as tk
from tkinter import messagebox
import json
import os

class AuthManager:
    def __init__(self, database):
        self.database = database
        self.usuario_actual = None
        self.archivo_sesion = 'sesion_guardada.json'
        self.cargar_sesion_guardada()
    
    def cargar_sesion_guardada(self):
        """Carga la sesión guardada del archivo JSON"""
        try:
            if os.path.exists(self.archivo_sesion):
                with open(self.archivo_sesion, 'r') as f:
                    datos = json.load(f)
                    username = datos.get('username')
                    
                    # Verificar que el usuario aún existe en la base de datos
                    if username and self.database.verificar_usuario_existe(username):
                        self.usuario_actual = username
                        print(f"Sesión cargada automáticamente: {username}")
        except Exception as e:
            print(f"Error al cargar sesión: {e}")
    
    def guardar_sesion(self, username):
        """Guarda la sesión en un archivo JSON"""
        try:
            datos = {'username': username}
            with open(self.archivo_sesion, 'w') as f:
                json.dump(datos, f)
        except Exception as e:
            print(f"Error al guardar sesión: {e}")
    
    def eliminar_sesion_guardada(self):
        """Elimina la sesión guardada"""
        try:
            if os.path.exists(self.archivo_sesion):
                os.remove(self.archivo_sesion)
        except Exception as e:
            print(f"Error al eliminar sesión: {e}")
    
    def verificar_usuario_existe(self, username):
        """Verifica si un usuario existe en la base de datos"""
        return self.database.verificar_usuario_existe(username)
    
    def crear_barra_usuario(self, padre):
        """Crea la barra superior con información del usuario"""
        barra_usuario = tk.Frame(padre, bg='#34495E', height=40)
        barra_usuario.pack(fill=tk.X, padx=10, pady=5)
        barra_usuario.pack_propagate(False)
        
        if self.usuario_actual:
            texto_usuario = f"👤 Usuario: {self.usuario_actual}"
            color_usuario = '#2ECC71'
        else:
            texto_usuario = "👤 Invitado"
            color_usuario = '#95A5A6'
        
        label_usuario = tk.Label(barra_usuario, text=texto_usuario, 
                                font=("Arial", 10, "bold"), bg='#34495E', fg=color_usuario)
        label_usuario.pack(side=tk.RIGHT, padx=10)
        
        return barra_usuario
    
    def mostrar_ventana_registro(self, parent_window, callback_actualizar):
        """Muestra ventana de registro"""
        ventana = tk.Toplevel(parent_window)
        ventana.title("Registrar Usuario")
        ventana.geometry("300x250")
        ventana.configure(bg='#2C3E50')
        ventana.transient(parent_window)
        ventana.grab_set()
        
        # Centrar ventana
        ventana.geometry("+%d+%d" % (
            parent_window.winfo_rootx() + 50, 
            parent_window.winfo_rooty() + 50
        ))
        
        tk.Label(ventana, text="📝 REGISTRAR USUARIO", 
                font=("Arial", 12, "bold"), bg='#2C3E50', fg='white').pack(pady=10)
        
        tk.Label(ventana, text="Usuario:", 
                font=("Arial", 11), bg='#2C3E50', fg='white').pack(pady=5)
        entry_usuario = tk.Entry(ventana, font=("Arial", 11))
        entry_usuario.pack(pady=5)
        entry_usuario.focus()  # Foco automático
        
        tk.Label(ventana, text="Contraseña:", 
                font=("Arial", 11), bg='#2C3E50', fg='white').pack(pady=5)
        entry_password = tk.Entry(ventana, show="*", font=("Arial", 11))
        entry_password.pack(pady=5)
        
        def registrar():
            self.procesar_registro(entry_usuario.get(), entry_password.get(), ventana, callback_actualizar)
        
        # Botón registrar
        btn_registrar = tk.Button(ventana, text="Registrar", 
                 font=("Arial", 11), bg='#2ECC71', fg='white',
                 command=registrar)
        btn_registrar.pack(pady=10)
        
        # Bind Enter key
        entry_password.bind('<Return>', lambda e: registrar())
        entry_usuario.bind('<Return>', lambda e: entry_password.focus())
        
        # Info sobre Enter
        lbl_info = tk.Label(ventana, text="💡 Presiona Enter para registrar", 
                           font=("Arial", 9), bg='#2C3E50', fg='#BDC3C7')
        lbl_info.pack(pady=5)
    
    def procesar_registro(self, usuario, password, ventana, callback_actualizar):
        """Procesa el registro de usuario"""
        usuario = usuario.strip()
        password = password.strip()
        
        if not usuario or not password:
            messagebox.showerror("Error", "Completa todos los campos")
            return
        
        if len(usuario) < 3:
            messagebox.showerror("Error", "El usuario debe tener al menos 3 caracteres")
            return
        
        if len(password) < 4:
            messagebox.showerror("Error", "La contraseña debe tener al menos 4 caracteres")
            return
        
        if self.database.registrar_usuario(usuario, password):
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            ventana.destroy()
            # Iniciar sesión automáticamente después del registro
            self.usuario_actual = usuario
            self.guardar_sesion(usuario)
            callback_actualizar()
        else:
            messagebox.showerror("Error", "El usuario ya existe")
    
    def mostrar_ventana_login(self, parent_window, callback_actualizar):
        """Muestra ventana de login"""
        ventana = tk.Toplevel(parent_window)
        ventana.title("Iniciar Sesión")
        ventana.geometry("300x250")
        ventana.configure(bg='#2C3E50')
        ventana.transient(parent_window)
        ventana.grab_set()
        
        # Centrar ventana
        ventana.geometry("+%d+%d" % (
            parent_window.winfo_rootx() + 50, 
            parent_window.winfo_rooty() + 50
        ))
        
        tk.Label(ventana, text="🔐 INICIAR SESIÓN", 
                font=("Arial", 12, "bold"), bg='#2C3E50', fg='white').pack(pady=10)
        
        tk.Label(ventana, text="Usuario:", 
                font=("Arial", 11), bg='#2C3E50', fg='white').pack(pady=5)
        entry_usuario = tk.Entry(ventana, font=("Arial", 11))
        entry_usuario.pack(pady=5)
        entry_usuario.focus()  # Foco automático
        
        # Si hay sesión guardada, autocompletar
        if self.usuario_actual:
            entry_usuario.insert(0, self.usuario_actual)
        
        tk.Label(ventana, text="Contraseña:", 
                font=("Arial", 11), bg='#2C3E50', fg='white').pack(pady=5)
        entry_password = tk.Entry(ventana, show="*", font=("Arial", 11))
        entry_password.pack(pady=5)
        
        def login():
            self.procesar_login(entry_usuario.get(), entry_password.get(), ventana, callback_actualizar)
        
        # Botón login
        btn_login = tk.Button(ventana, text="Iniciar Sesión", 
                 font=("Arial", 11), bg='#2ECC71', fg='white',
                 command=login)
        btn_login.pack(pady=10)
        
        # Bind Enter key
        entry_password.bind('<Return>', lambda e: login())
        entry_usuario.bind('<Return>', lambda e: entry_password.focus())
        
        # Info sobre Enter
        lbl_info = tk.Label(ventana, text="💡 Presiona Enter para ingresar", 
                           font=("Arial", 9), bg='#2C3E50', fg='#BDC3C7')
        lbl_info.pack(pady=5)
    
    def procesar_login(self, usuario, password, ventana, callback_actualizar):
        """Procesa el inicio de sesión"""
        usuario = usuario.strip()
        password = password.strip()
        
        if not usuario or not password:
            messagebox.showerror("Error", "Completa todos los campos")
            return
        
        if self.database.verificar_login(usuario, password):
            self.usuario_actual = usuario
            self.guardar_sesion(usuario)  # Guardar sesión
            messagebox.showinfo("Éxito", f"¡Bienvenido {usuario}!")
            ventana.destroy()
            callback_actualizar()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    
    def cerrar_sesion(self, callback_actualizar):
        """Cierra la sesión del usuario actual"""
        self.usuario_actual = None
        self.eliminar_sesion_guardada()  # Eliminar sesión guardada
        messagebox.showinfo("Sesión", "Sesión cerrada correctamente")
        callback_actualizar()