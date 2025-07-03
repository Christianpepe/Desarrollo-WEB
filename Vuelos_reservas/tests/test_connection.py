# test_connection.py - Script para probar la conexión a PostgreSQL

import os
import django
import psycopg2
from django.conf import settings

def test_direct_postgresql():
    """Prueba conexión directa a PostgreSQL sin Django"""
    print("=== Probando conexión directa a PostgreSQL ===")
    
    try:
        # Configuración de conexión
        conn = psycopg2.connect(
            host="localhost",
            database="Vuelos",
            user="postgres",  # Cambia por tu usuario
            password="12345"       # Cambia por tu contraseña
        )
        
        # Crear cursor
        cur = conn.cursor()
        
        # Ejecutar consulta simple
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f" Conexión exitosa a PostgreSQL")
        print(f"Versión: {version[0]}")
        
        # Verificar que existe la tabla usuarios_usuario
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'usuarios_usuario';
        """)
        
        tabla = cur.fetchone()
        if tabla:
            print(f" Tabla 'usuarios_usuario' encontrada")
            
            # Contar registros
            cur.execute("SELECT COUNT(*) FROM usuarios_usuario;")
            count = cur.fetchone()[0]
            print(f" Registros en tabla: {count}")
            
            # Mostrar estructura de la tabla
            cur.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'usuarios_usuario'
                ORDER BY ordinal_position;
            """)
            
            columnas = cur.fetchall()
            print(" Estructura de la tabla:")
            for col in columnas:
                print(f"   - {col[0]} ({col[1]}) - Nullable: {col[2]}")
                
        else:
            print("  Tabla 'usuarios_usuario' no encontrada")
        
        # Cerrar conexiones
        cur.close()
        conn.close()
        print(" Conexión cerrada correctamente")
        
    except psycopg2.Error as e:
        print(f" Error conectando a PostgreSQL: {e}")
    except Exception as e:
        print(f" Error inesperado: {e}")

def test_django_connection():
    """Prueba conexión a través de Django"""
    print("\n=== Probando conexión a través de Django ===")
    
    try:
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vuelo_reserva.settings')
        django.setup()
        
        from django.db import connection
        from django.contrib.auth.models import User
        
        # Probar conexión
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print(" Conexión Django-PostgreSQL exitosa")
        
        # Verificar modelos
        try:
            user_count = User.objects.count()
            print(f" Usuarios en Django: {user_count}")
        except Exception as e:
            print(f"  Error accediendo a modelos Django: {e}")
            
    except Exception as e:
        print(f" Error en conexión Django: {e}")

def crear_usuario_prueba():
    """Crear un usuario de prueba"""
    print("\n=== Creando usuario de prueba ===")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vuelo_reserva.settings')
        django.setup()
        
        from django.contrib.auth.models import User
        
        # Crear usuario solo si no existe
        username = "usuario_prueba"
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email="prueba@test.com",
                password="password123"
            )
            print(f" Usuario '{username}' creado exitosamente")
        else:
            print(f"  Usuario '{username}' ya existe")
            
        # Mostrar todos los usuarios
        usuarios = User.objects.all()
        print(f" Total de usuarios: {usuarios.count()}")
        
        for user in usuarios:
            print(f"   - ID: {user.id}, Username: {user.username}, Email: {user.email}")
            
    except Exception as e:
        print(f" Error creando usuario: {e}")

if __name__ == "__main__":
    print(" Iniciando pruebas de conexión a base de datos...\n")
    
    # Ejecutar todas las pruebas
    test_direct_postgresql()
    test_django_connection()
    crear_usuario_prueba()
    
    print("\n Pruebas completadas")
    print("\n NOTA: Recuerda cambiar las credenciales en el script:")
    print("   - tu_usuario_postgres")
    print("   - tu_password")