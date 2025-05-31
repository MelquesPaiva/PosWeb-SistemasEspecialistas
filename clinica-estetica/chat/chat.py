from flask import Flask, render_template, request, Response

import json
import secrets
import requests

CONFIDENCE_LEVEL = 0.5
ROBOT_SERVICE_URL = "http://localhost:5000"
ROBOT_SERVICE_RESPONSE_URL = f"{ROBOT_SERVICE_URL}/response"

chat = Flask(__name__)
chat.secret_key = secrets.token_hex(16)

def robot_request(url, data = None):
    success, result = False, None
    try:
        if data:
            result = requests.post(url, json=data)
        else:
            result = requests.get(url)
        result = result.json()
        success = True
    except Exception as e:
        print(f"Erro ao acessar o robô: {str(e)}")
        return success, result

    return success, result

def robot_question(question):
    success, result = robot_request(ROBOT_SERVICE_RESPONSE_URL, {"question": question})
    message = "Infelizmente, ainda não sei responder essa pergunta. Entre em contato com um bibliotecário para mais informações."
    if success and response["confidence"] >= CONFIDENCE_LEVEL:
        message = result["response"]

    return message

@chat.get("/")
def index():
    return render_template("index.html")

@chat.post("/response")
def response():
    data = request.json
    question = data["question"]

    result = robot_question(question)

    return Response(
        json.dumps({"response": result}),
        mimetype="application/json",
        status=200
    )

if __name__ == "__main__":
    chat.run(
        host = "0.0.0.0",
        port = 5001,
        debug=True
    )
