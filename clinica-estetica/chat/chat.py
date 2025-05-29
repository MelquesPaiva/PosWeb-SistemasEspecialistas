from flask import Flask, render_template, request, Response

import json
import secrets
import requests

CONFIANCA_MINIMA = 0.5
ROBO_SERVICE_URL = "http://localhost:5000"
ROBO_SERVICE_RESPONSE_URL = f"{ROBO_SERVICE_URL}/response"

chat = Flask(__name__)
chat.secret_key = secrets.token_hex(16)

def robot_request(url, data = None):
    success, response = False, None
    try:
        if data:
            response = requests.post(url, json=data)
        else:
            response = requests.get(url)
        response = response.json()
        success = True
    except Exception as e:
        print(f"Erro ao acessar o robô: {str(e)}")
        return success, response

    return success, response

def robot_question(question):
    success, response = robot_request(ROBO_SERVICE_RESPONSE_URL, {"question": question})
    message = "Infelizmente, ainda não sei responder essa pergunta. Entre em contato com um bibliotecário para mais informações."
    if success and response["confidence"] >= CONFIANCA_MINIMA:
        message = response["response"]

    return message

@chat.get("/")
def index():
    return render_template("index.html")

@chat.post("/response")
def response():
    data = request.json
    question = data["question"]

    response = robot_question(question)

    return Response(
        json.dumps({"response": response}),
        mimetype="application/json",
        status=200
    )

if __name__ == "__main__":
    chat.run(
        host = "0.0.0.0",
        port = 5001,
        debug=True
    )
