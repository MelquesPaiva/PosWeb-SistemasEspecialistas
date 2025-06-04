import os
import sqlite3

BD_PATH = os.getcwd()
BD_PRESCRIPTIONS = f"{BD_PATH}/prescriptions.sqlite3"

def init_prescription_db():
    if os.path.exists(BD_PRESCRIPTIONS):
        os.remove(BD_PRESCRIPTIONS)

    connection = sqlite3.connect(BD_PRESCRIPTIONS)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER,
            title TEXT NOT NULL,
            path TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS keys(
            id_prescription INTEGER,
            key TEXT       
        )
    """)

def generate_prescription(id_prescription: int, prescription_title: str, prescription_path: str, token_list: list):
    success, message = False, "Houve um erro ao se comunicar com o banco de dados"

    connection = sqlite3.connect(BD_PRESCRIPTIONS)
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO prescriptions (id, title, path) VALUES (?, ?, ?)",
                       (id_prescription, prescription_title.strip(), prescription_path))
        for token in token_list:
            cursor.execute("INSERT INTO keys (id_prescription, key) VALUES (?, ?)", (id_prescription, token))

        connection.commit()
        success = True
        message = "Prescrição salva com sucesso"
    except Exception as e:
        message = f"{message}: {str(e)}"
    finally:
        connection.close()
        return success, message

def get_prescriptions_by_keys(keys):
    success, message, prescriptions = False, "Não foi possível recuperar as prescriçẽos", []

    connection = sqlite3.connect(BD_PRESCRIPTIONS)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT p.* FROM prescriptions p JOIN keys k ON p.id = k.id_prescription WHERE k.key in (%s) GROUP BY p.id' % ','.join('?'*len(keys)), list(map(str.strip, keys)))
        prescriptions = cursor.fetchall()

        success = True
        message = "Artigos recuperados com sucesso"
    except Exception as e:
        message = f"{message}: {str(e)}"

    connection.close()

    return success, message, prescriptions
