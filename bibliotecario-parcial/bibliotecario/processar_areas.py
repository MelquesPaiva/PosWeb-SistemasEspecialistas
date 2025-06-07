from PIL import Image
from areas_db import criar_tabela_areas, gravar_areas, visualizar_areas

import pytesseract
import os

from inicializar_modelo import iniciar_ia, obter_resposta

CAMINHO_IMAGENS = os.getcwd() + "/artigos"
MAXIMO_IMAGENS = 1_000

def init_prompt():
    prompt = []
    prompt.append(("system", "Você é um assistente capaz de realizar correções gramaticais do idioma português"))
    prompt.append(("system", "Sua função principal é revisar, corrigir e normalizar palavras fornecidas pelo usuário"))
    prompt.append(("system", "As palavras tratadas são áreas de conhecimento de TI. Normalize as palavras para algo que faça sentido "
                             "no contexto de um artigo de conclusão do curso relacionado a tecnologia da informação"))
    prompt.append(("system", "As palavras são provenientes de um processo de OCR, e podem ter erros comuns a esse processo "
                             "como segmentos de texto quebrados, problemas de espaçamento, erros de capitalização,"
                             "e outros ruídos. Esses devem ser tratados e corrigidos. Se atente as áreas de conhecimento"))
    prompt.append(("system", "O usuário irá informar lista de palavras para ser corrigida"))
    prompt.append(("system", "Seja extremamente direto e responda para o usuário apenas a palavra corrigida"))
    prompt.append(("human", "{palavras}"))
    return prompt

def get_areas_de_conhecimento(imagem, IA):
    areas_corrigidas = []

    texto = pytesseract.image_to_string(Image.open(imagem), lang="por")
    areas = texto.split("\n")
    areas = [area for area in areas if area != '']

    sucesso, resposta = obter_resposta(IA, {"palavras": areas})
    if sucesso:
        areas_corrigidas = resposta.content.split("\n")
    else:
        print("Erro ao corrigir palavras")

    return areas_corrigidas

def processar_imagens(IA):
    criar_tabela_areas()
    for contador in range(1, MAXIMO_IMAGENS):
        imagem = f"{CAMINHO_IMAGENS}/{contador}.disciplinas.png"
        if os.path.exists(imagem):
            print(f"Processando a imagem: {imagem}")
            areas = get_areas_de_conhecimento(imagem, IA)
            print(f"Areas encontradas: {areas}")

            gravar_areas(contador, areas)

            print("Areas gravadas com sucesso")

            continue

        break

    print("\nProcessamento finalizado\n")

if __name__ == "__main__":
    prompt = init_prompt()
    iniciado, IA = iniciar_ia(prompt)
    if iniciado:
        processar_imagens(IA)

    print(f"{visualizar_areas()}")