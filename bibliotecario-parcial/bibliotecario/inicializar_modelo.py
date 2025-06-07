import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

API_KEY = os.getcwd() + '/genai.key'
MODELO = "gemini-2.5-flash-preview-04-17"

def iniciar_ia(prompt):
    iniciado, IA = False, None
    try:
        with open(API_KEY, "r") as chave_gemini:
            chave = chave_gemini.read()
            os.environ["GOOGLE_API_KEY"] = chave

            chave_gemini.close()

        llm = ChatGoogleGenerativeAI(model=MODELO, temperature=0, max_tokens=None, timeout=None, max_retries=2)
        IA = ChatPromptTemplate.from_messages(prompt) | llm

        iniciado = True
    except Exception as e:
        print(f"Erro iniciando a IA: {str(e)}")

    return iniciado, IA

def obter_resposta(IA, parametros):
    sucesso, resposta = False, None
    try:
        resposta = IA.invoke(parametros)
        sucesso = True
    except Exception as e:
        print(f"Ocorreu um erro obtendo resposta: {str(e)}")

    return sucesso, resposta
