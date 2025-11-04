# main.py
import tkinter as tk
from menu_principal import MenuPrincipal
from database import Database
from auth import AuthManager
from app_manager import app_manager

class SuiteJuegos:
    def __init__(self):
        self.root = tk.Tk()
        self.database = Database()
        self.auth = AuthManager(self.database)
    
    # Configurar el app_manager
        app_manager.inicializar(
            self.root, 
            self.auth, 
            self.database,
            self.mostrar_menu_principal
    )
    
    # Mostrar mensaje de bienvenida si hay sesión cargada
        if self.auth.usuario_actual:
            print(f"Bienvenido de nuevo, {self.auth.usuario_actual}!")
    
        self.mostrar_menu_principal()
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Crear menú principal
        self.menu = MenuPrincipal(self.root, self.auth, self.database)
    
    def ejecutar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SuiteJuegos()
    app.ejecutar()