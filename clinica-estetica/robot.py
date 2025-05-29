from chatterbot import ChatBot
import os

ROBOT_NAME = "Robô para clínicas de estética"
ROBOT_DB = "clinica_estetica.db"
DB_PATH = os.getcwd()

def init_robot():
    success, robot = False, None
    try:
        robot = ChatBot(
            ROBOT_NAME,
            read_only=True,
            storage_adapter="chatterbot.storage.SQLStorageAdapter",
            database_uri=f"sqlite:///{ROBOT_DB}",
        )
        success = True
    except Exception as e:
        print(f"Erro ao inicializar o robô: {str(e)}")

    return success, robot


def execute(robot: ChatBot):
    while True:
        message = input("👤 ")
        response = robot.get_response(message.lower())
        
        if response.confidence < 0.5:
            print(f"🤖 Desculpe, não consegui entender. Tente novamente. \n (confiança = {response.confidence})")
            # registra a pergunta em um log
        else:
            print(f"🤖 {response.text} \n (confiança = {response.confidence})")

if __name__ == "__main__":
    success, robot = init_robot()
    if success:
        print(f"{ROBOT_NAME} inicializado com sucesso!")
        execute(robot)
    else:
        print(f"Falha ao inicializar {ROBOT_NAME}.")
