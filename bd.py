import sqlite3
from datetime import datetime

DB_NAME = "libellum.db"  # nombre del archivo .db

def conectar():
    return sqlite3.connect(DB_NAME)

def crear_tabla():
    with conectar() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS documentos (
                documento TEXT PRIMARY KEY,
                razon_social TEXT,
                fecha DATE,
                estado TEXT,
                total_factura REAL
            )
        ''')
        conn.commit()

def documento_ya_enviado(doc_id):
    with conectar() as conn:
        cursor = conn.execute("SELECT 1 FROM documentos WHERE documento = ?", (doc_id,))
        return cursor.fetchone() is not None

def insertar_documento(doc):
    # Convertir fecha a formato YYYY-MM-DD
    fecha_formateada = convertir_fecha(doc['fecha'])
    monto = convertir_monto(doc['total_factura'])

    with conectar() as conn:
        conn.execute('''
            INSERT INTO documentos (documento, razon_social, fecha, estado, total_factura)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            doc['documento'],
            doc['razon_social'],
            fecha_formateada,
            doc['estado'],
            monto
        ))
        conn.commit()

def convertir_fecha(fecha):
    try:
        return datetime.strptime(fecha.strip(), "%d/%m/%Y").date()
    except Exception:
        return None  # o puedes lanzar una excepción

def convertir_monto(monto_str):
    try:
        monto_str = monto_str.replace("$", "").replace(".", "").replace(",", ".")
        return float(monto_str)
    except Exception:
        return 0.0
