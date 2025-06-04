from chatterbot.trainers import ListTrainer
from robot import init_robot

import json
import os

CHATS = [
    os.getcwd() + "/chat_data/greetings.json",
    os.getcwd() + "/chat_data/informations.json",
    os.getcwd() + "/chat_data/search_commands.json"
]

def load_data():
    chats = []
    for file in CHATS:
        try:
            with open(file, "r") as f:
                # conversas.extend(json.load(f))
                chat_data = json.load(f)
                chats.append(chat_data["data"])
                f.close()
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {file}")
            return None
        except json.JSONDecodeError:
            print(f"Erro ao decodificar JSON no arquivo: {file}")
            return None

    return chats

def create_trainer():
    success, robot = init_robot()
    if success:
        robot.storage.drop()
        return ListTrainer(robot)
    
    return None

def train_robot(trainer: ListTrainer, chats):
    for chat in chats:
        for question_answer in chat:
            messages = question_answer["message"]
            response = question_answer["response"]

            for message in messages:
                print(f"Treinando com: {message} -> {response}")
                trainer.train([message, response])

if __name__ == "__main__":
    chats = load_data()
    trainer = create_trainer()
    if trainer is None:
        print("Falha ao criar o treinador do robô.")
    else:
        print("Treinando o robô...")
        train_robot(trainer, chats)
        print("Robô treinado com sucesso!")
