import os
import sqlite3

BD_ARTIGOS = os.getcwd() + '/artigos.sqlite3'

def criar_tabela_areas():
    conexao = sqlite3.connect(BD_ARTIGOS)
    cursor = conexao.cursor()

    cursor.execute("""
    DROP TABLE IF EXISTS areas
    """)
    cursor.execute("""
    CREATE TABLE areas (id_artigo INTEGER, area TEXT)
    """)

    cursor.close()
    conexao.commit()
    conexao.close()

def gravar_areas(id_artigo, areas):
    conexao = sqlite3.connect(BD_ARTIGOS)
    cursor = conexao.cursor()

    for area in areas:
        cursor.execute("""
        INSERT INTO areas (id_artigo, area) VALUES (?, ?)
        """, (id_artigo, area))

    cursor.close()
    conexao.commit()
    conexao.close()

def visualizar_areas():
    conexao = sqlite3.connect(BD_ARTIGOS)
    cursor = conexao.cursor()
    conexao.row_factory = sqlite3.SQLITE_ROW

    cursor.execute("""
    SELECT id, GROUP_CONCAT (areas.area) Related FROM artigos JOIN areas ON areas.id_artigo = artigos.id GROUP BY artigos.id
    """)
    areas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return areas