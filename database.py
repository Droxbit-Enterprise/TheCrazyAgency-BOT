import sqlite3

DB_PATH = "db/bot.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    # [0=telegram_id, nombre=1, sugo_id=2, timo_id=3, salsa_id=4, contigo_id=5, meyo_id=6, 
    # kito_id=7, es_mayor=8, tiene_wifi=9, tiene_tiempo=10, registrada=11, inicio_sesion=12, apellido=13]
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarias (
            telegram_id INTEGER PRIMARY KEY, 
            nombre TEXT,
            sugo_id TEXT,
            timo_id TEXT,
            salsa_id TEXT,
            contigo_id TEXT,
            meyo_id TEXT,
            kito_id TEXT,
            es_mayor INTEGER DEFAULT 0,
            tiene_wifi INTEGER DEFAULT 0,
            tiene_tiempo INTEGER DEFAULT 0,
            registrada INTEGER DEFAULT 0,
            inicio_sesion INTEGER DEFAULT 0,
            apellido TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Base de Datos Creada")
    
def get_user(telegram_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT telegram_id, nombre, sugo_id, timo_id, salsa_id, contigo_id, meyo_id, kito_id, 
                es_mayor, tiene_wifi, tiene_tiempo, registrada, inicio_sesion, apellido
        FROM usuarias WHERE telegram_id = ?
    """, (telegram_id,))
    row = cur.fetchone()
    conn.close()
    return row

def save_user_full(
        telegram_id: int, nombre: str, sugo_id: str, timo_id: str, salsa_id: str, contigo_id: str, meyo_id: str, kito_id: str, 
        es_mayor: int, tiene_wifi: int, tiene_tiempo: int, registrada: int, inicio_sesion: int, apellido: str,
    ):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO usuarias (
            telegram_id, nombre, sugo_id, timo_id, salsa_id, contigo_id, meyo_id, kito_id,
            es_mayor, tiene_wifi, tiene_tiempo, registrada, inicio_sesion, apellido
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
        (
            telegram_id, nombre, sugo_id, timo_id, salsa_id, contigo_id, meyo_id, kito_id,
            es_mayor, tiene_wifi, tiene_tiempo, registrada, inicio_sesion, apellido
        )
    )
    conn.commit()
    conn.close()
    
def update_user_field(telegram_id: int, field: str, value):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"UPDATE usuarias SET {field} = ? WHERE telegram_id = ?", (value, telegram_id))
    conn.commit()
    conn.close()