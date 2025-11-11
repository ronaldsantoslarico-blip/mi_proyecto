# sistema_contador/database.py
import mysql.connector
import os
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta

load_dotenv()

# Configuración de la base de datos
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'sistema_contador')
}

def get_db_connection():
    """Obtener conexión a MySQL"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as e:
        print(f"Error de conexión: {e}")
        return None

def init_database():
    """Inicializar la base de datos con datos de ejemplo"""
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    try:
        # Crear tabla clientes si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                telefono VARCHAR(20),
                direccion VARCHAR(255),
                estado_actual VARCHAR(20) DEFAULT 'al_dia',
                fecha_registro DATE DEFAULT (CURRENT_DATE),
                sueldo DECIMAL(10,2) DEFAULT 0,
                otros_ingresos DECIMAL(10,2) DEFAULT 0,
                gastos_vivienda DECIMAL(10,2) DEFAULT 0,
                tiene_propiedad BOOLEAN DEFAULT FALSE,
                valor_propiedad DECIMAL(12,2) DEFAULT 0,
                apto_prestamo VARCHAR(20) DEFAULT 'pendiente',
                evaluacion_ia TEXT,
                calificacion_crediticia DECIMAL(3,1) DEFAULT 0,
                fecha_evaluacion DATETIME,
                notas TEXT,
                monto_solicitado DECIMAL(12,2) DEFAULT 0
            )
        """)
        
        # Agregar columnas faltantes si es necesario
        cursor.execute("SHOW COLUMNS FROM clientes")
        columnas_existentes = [row[0] for row in cursor.fetchall()]
        
        columnas_necesarias = {
            'telefono': 'VARCHAR(20)',
            'direccion': 'VARCHAR(255)',
            'sueldo': 'DECIMAL(10,2) DEFAULT 0',
            'otros_ingresos': 'DECIMAL(10,2) DEFAULT 0',
            'gastos_vivienda': 'DECIMAL(10,2) DEFAULT 0',
            'tiene_propiedad': 'BOOLEAN DEFAULT FALSE',
            'valor_propiedad': 'DECIMAL(12,2) DEFAULT 0',
            'apto_prestamo': 'VARCHAR(20) DEFAULT "pendiente"',
            'evaluacion_ia': 'TEXT',
            'calificacion_crediticia': 'DECIMAL(3,1) DEFAULT 0',
            'fecha_evaluacion': 'DATETIME',
            'notas': 'TEXT',
            'monto_solicitado': 'DECIMAL(12,2) DEFAULT 0'
        }
        
        for columna, tipo in columnas_necesarias.items():
            if columna not in columnas_existentes:
                try:
                    cursor.execute(f"ALTER TABLE clientes ADD COLUMN {columna} {tipo}")
                    print(f"✅ Columna '{columna}' agregada")
                except Exception as e:
                    print(f"⚠️  No se pudo agregar columna '{columna}': {e}")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pagos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cliente_id INT,
                mes INT,
                año INT,
                estado VARCHAR(20),
                monto DECIMAL(10,2),
                descripcion TEXT,
                fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
            )
        """)
        
        # Insertar datos de ejemplo si no existen
        cursor.execute("SELECT COUNT(*) FROM clientes")
        if cursor.fetchone()[0] == 0:
            print("📝 Insertando datos de ejemplo...")
            
            clientes_ejemplo = [
                ('Juan Pérez', 'juan@email.com', 'al_dia'),
                ('María García', 'maria@email.com', 'retraso_leve'),
                ('Carlos López', 'carlos@email.com', 'impago'),
                ('Ana Martínez', 'ana@email.com', 'al_dia'),
                ('Pedro Rodríguez', 'pedro@email.com', 'retraso_grave'),
                ('Laura Fernández', 'laura@email.com', 'al_dia'),
                ('Miguel Torres', 'miguel@email.com', 'retraso_leve'),
                ('Sofía Ramírez', 'sofia@email.com', 'al_dia'),
                ('David Hernández', 'david@email.com', 'al_dia'),
                ('Elena Castro', 'elena@email.com', 'retraso_grave')
            ]
            
            for nombre, email, estado in clientes_ejemplo:
                cursor.execute(
                    'INSERT INTO clientes (nombre, email, estado_actual) VALUES (%s, %s, %s)',
                    (nombre, email, estado)
                )
                cliente_id = cursor.lastrowid
                
                # Generar pagos de ejemplo para los últimos 12 meses
                año_actual = 2024
                montos_base = [2500, 2800, 3000, 2200, 2600, 2400, 2900, 2700, 3100, 2300, 2650, 2850]
                
                for mes in range(1, 13):
                    # Variar el monto ligeramente
                    monto = montos_base[mes-1] * random.uniform(0.9, 1.1)
                    monto = round(monto, 2)
                    
                    # Patrón de comportamiento basado en estado del cliente
                    if estado == 'al_dia':
                        # 80% al día, 20% retraso leve
                        estado_pago = 'al_dia' if random.random() < 0.8 else 'retraso_leve'
                    elif estado == 'retraso_leve':
                        # 40% al día, 40% retraso leve, 20% retraso grave
                        rand = random.random()
                        if rand < 0.4:
                            estado_pago = 'al_dia'
                        elif rand < 0.8:
                            estado_pago = 'retraso_leve'
                        else:
                            estado_pago = 'retraso_grave'
                    elif estado == 'retraso_grave':
                        # 20% retraso leve, 50% retraso grave, 30% impago
                        rand = random.random()
                        if rand < 0.2:
                            estado_pago = 'retraso_leve'
                        elif rand < 0.7:
                            estado_pago = 'retraso_grave'
                        else:
                            estado_pago = 'impago'
                    else:  # impago
                        # 10% retraso grave, 90% impago
                        estado_pago = 'retraso_grave' if random.random() < 0.1 else 'impago'
                    
                    descripcion = f"Pago mensual {mes}/{año_actual}"
                    
                    cursor.execute(
                        'INSERT INTO pagos (cliente_id, mes, año, estado, monto, descripcion) VALUES (%s, %s, %s, %s, %s, %s)',
                        (cliente_id, mes, año_actual, estado_pago, monto, descripcion)
                    )
        
        conn.commit()
        print("✅ Base de datos lista")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()