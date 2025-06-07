import sqlite3

from chatterbot import ChatBot
import os

NOME_ROBO = "Robô Bibliotecário Akhenaton"
BD_ROBO = "chat.sqlite3"

CONFIANCA_MINIMA = 0.6

CAMINHO_BD = os.getcwd()
BD_ARTIGOS = f"{CAMINHO_BD}/artigos.sqlite3"

def inicializar():
    sucesso, robo, artigos = False, None, None

    try:
        robo = ChatBot(NOME_ROBO, read_only=True, storage_adapter="chatterbot.storage.SQLStorageAdapter", database_uri=f"sqlite:///{BD_ROBO}")
        artigos = get_artigos(como_linhas=True)

        sucesso = True
    except Exception as e:
        print(f"erro inicializando o robô: {str(e)}")

    return sucesso, robo, artigos

def pesquisar_artigos_por_chaves(chaves, artigos):
    encontrou, artigos_selecionados = False, {}

    for artigo in artigos:
        for chave in chaves:
            chave = chave.strip()

            if chave and any (chave.lower() in c.lower() for c in artigo['chaves']):
                artigos_selecionados[artigo["id"]] = {
                    "id": artigo["id"],
                    "titulo": artigo["titulo"],
                    "artigo": artigo["artigo"]
                }

                encontrou = True

    return encontrou, artigos_selecionados

def pesquisar_artigos_por_areas(areas, artigos):
    encontrou, artigos_selecionados = False, {}
    for artigo in artigos:
        for area in areas:
            area = area.strip()
            if area and any (area.lower() in c.lower() for c in artigo['areas']):
                artigos_selecionados[artigo["id"]] = {
                    "id": artigo["id"],
                    "titulo": artigo["titulo"],
                    "artigo": artigo["artigo"]
                }

                encontrou = True

    return encontrou, artigos_selecionados

def get_artigos(como_linhas = False):
    conexao = sqlite3.connect(BD_ARTIGOS)
    if como_linhas:
        conexao.row_factory = sqlite3.Row

    cursor = conexao.cursor()
    cursor.execute("""
    SELECT 
        id,
        titulo,
        artigo,
        chave1,
        chave2,
        chave3,
        chave4,
        chave5,
        chave6,
        chave7,
        GROUP_CONCAT(areas.area) areas
    FROM artigos, chaves, areas
    WHERE chaves.id_artigo = artigos.id AND areas.id_artigo = artigos.id
    GROUP BY artigos.id""")

    artigos = cursor.fetchall()
    artigos = [dict(row) for row in artigos]
    artigos_resultados = []

    for artigo in artigos:
        areas = artigo["areas"].split(",")
        artigo_data = {
            "id": artigo["id"],
            "titulo": artigo["titulo"],
            "artigo": artigo["artigo"],
            "chaves": [artigo["chave1"], artigo["chave2"], artigo["chave3"], artigo["chave4"], artigo["chave5"], artigo["chave6"], artigo["chave7"]],
            "areas": areas
        }
        artigos_resultados.append(artigo_data)

    conexao.close()

    return artigos_resultados

def executar(robo):
    while True:
        mensagem = input("👤 ")
        resposta = robo.get_response(mensagem.lower())

        if resposta.confidence >= CONFIANCA_MINIMA:
            print(f"🤖 {resposta.text} [confiança = {resposta.confidence}]")
        else:
            print(f"🤖 Infelizmente, ainda não sei responder esta pergunta. Entre em contato com a biblioteca. Mais informações no site https://portal.ifba.edu.br/conquista/ensino/biblioteca [confiança = {resposta.confidence}]")
            # registrar a pergunta em um log

if __name__ == "__main__":
    sucesso, robo, artigos = inicializar()
    print(f"{pesquisar_artigos_por_areas(["Algoritmos e Programação"], artigos)}")
    # if sucesso:
    #     executar(robo)