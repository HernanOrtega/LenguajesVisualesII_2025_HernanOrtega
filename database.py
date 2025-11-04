import sqlite3
import os

class Database:
    def __init__(self):
        self.db_name = 'juegos_suite.db'
        self.inicializar_base_datos()
    
    def get_conexion(self):
        """Obtiene una conexión a la base de datos"""
        return sqlite3.connect(self.db_name)
    
    def inicializar_base_datos(self):
        """Inicializa solo las tablas necesarias (sin datos de sopa de letras)"""
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de puntajes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS puntajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                juego TEXT NOT NULL,
                puntaje INTEGER NOT NULL,
                dificultad TEXT,
                categoria TEXT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        conexion.commit()
        conexion.close()
        print("✓ Base de datos inicializada (solo usuarios y puntajes)")
    
    def registrar_usuario(self, username, password):
        """Registra un nuevo usuario"""
        try:
            conexion = self.get_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO usuarios (username, password) VALUES (?, ?)",
                (username, password)
            )
            conexion.commit()
            conexion.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def verificar_usuario_existe(self, username):
        """Verifica si un usuario existe en la base de datos"""
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE username = ?", (username,))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado is not None

    def verificar_login(self, username, password):
        """Verifica las credenciales de login"""
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id FROM usuarios WHERE username = ? AND password = ?",
            (username, password)
        )
        resultado = cursor.fetchone()
        conexion.close()
        return resultado is not None
    
    def obtener_id_usuario(self, username):
        """Obtiene el ID de un usuario por su nombre"""
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE username = ?", (username,))
        resultado = cursor.fetchone()
        conexion.close()
        return resultado[0] if resultado else None
    
    def guardar_puntaje(self, usuario_id, juego, puntaje, dificultad=None, categoria=None):
        """Guarda un puntaje en la base de datos"""
        try:
            conexion = self.get_conexion()
            cursor = conexion.cursor()
            cursor.execute('''
                INSERT INTO puntajes (usuario_id, juego, puntaje, dificultad, categoria)
                VALUES (?, ?, ?, ?, ?)
            ''', (usuario_id, juego, puntaje, dificultad, categoria))
            conexion.commit()
            conexion.close()
            return True
        except Exception as e:
            print(f"Error guardando puntaje: {e}")
            return False
    
    def obtener_ranking(self, juego=None, limite=10):
        """Obtiene el ranking de puntajes"""
        conexion = self.get_conexion()
        cursor = conexion.cursor()
        
        if juego:
            cursor.execute('''
                SELECT u.username, p.puntaje, p.dificultad, p.categoria, p.fecha
                FROM puntajes p
                JOIN usuarios u ON p.usuario_id = u.id
                WHERE p.juego = ?
                ORDER BY p.puntaje DESC
                LIMIT ?
            ''', (juego, limite))
        else:
            cursor.execute('''
                SELECT u.username, p.puntaje, p.juego, p.dificultad, p.categoria, p.fecha
                FROM puntajes p
                JOIN usuarios u ON p.usuario_id = u.id
                ORDER BY p.puntaje DESC
                LIMIT ?
            ''', (limite,))
        
        resultado = cursor.fetchall()
        conexion.close()
        return resultado