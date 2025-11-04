# app_manager.py
class AppManager:
    def __init__(self):
        self.root = None
        self.auth = None
        self.database = None
        self.menu_principal_callback = None
    
    def inicializar(self, root, auth, database, menu_callback):
        self.root = root
        self.auth = auth
        self.database = database
        self.menu_principal_callback = menu_callback
    
    def volver_al_menu_principal(self):
        if self.menu_principal_callback:
            self.menu_principal_callback()

# Instancia global
app_manager = AppManager()