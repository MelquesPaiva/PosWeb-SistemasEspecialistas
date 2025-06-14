from flask import Flask, render_template, request, Response, session, send_from_directory

import json
import secrets
import requests

CONFIDENCE_LEVEL = 0.5
ROBOT_SERVICE_URL = "http://localhost:5000"
ROBOT_SERVICE_RESPONSE_URL = f"{ROBOT_SERVICE_URL}/response"
ROBOT_SERVICE_FIND_PRESCRIPTIONS_BY_KEYS = f"{ROBOT_SERVICE_URL}/prescriptions"
SEARCH_MODE_KEY = "search_mode"

chat = Flask(__name__)
chat.secret_key = secrets.token_hex(16)

def robot_request(url, data = None) -> tuple[bool, dict]:
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

def robot_question(question) -> tuple[str, bool]:
    success, result = robot_request(ROBOT_SERVICE_RESPONSE_URL, {"question": question})
    message = "Infelizmente, ainda não sei responder essa pergunta. Entre em contato com um bibliotecário para mais informações."
    if success and result["confidence"] >= CONFIDENCE_LEVEL:
        message = result["response"]

    return message, True if "Informe os ativos que deseja pesquisar" in message else False

def find_prescription_by_keys(keys) -> list:
    prescriptions = []
    if len(keys) < 1:
        return prescriptions

    success, result = robot_request(ROBOT_SERVICE_FIND_PRESCRIPTIONS_BY_KEYS, {"keys": keys})
    if success:
        prescriptions_data = result["prescriptions"]
        for prescription in prescriptions_data:
            prescriptions.append({
                "id": prescription["id"],
                "title": f"{prescription["order"]} - {prescription["title"]}",
                "path": prescription["path"]
            })

    return prescriptions

@chat.get("/")
def index():
    return render_template("index.html")

@chat.post("/response")
def response() -> Response:
    result, prescriptions = "", []

    data = request.json
    question = data["question"]

    search_mode = SEARCH_MODE_KEY in session.keys() and session[SEARCH_MODE_KEY]
    if search_mode:
        session[SEARCH_MODE_KEY] = False
        keys = question.split(",")
        prescriptions = find_prescription_by_keys(keys)
        if len(prescriptions):
            result = ("Caso deseja fazer a pesquisa novamente, digite 'pequisar de novo' ou pressione os botões. Caso deseja mais detalhes"
                      " sobre um receituário, clique no botão ❓")
        else:
            result = "Não encontrei nenhum receituário. Tente novamente com outros parâmetros"
    else:
        result, search_mode = robot_question(question)
        session[SEARCH_MODE_KEY] = search_mode

    session["prescriptions"] = prescriptions

    return Response(
        json.dumps({"response": result, "prescriptions": prescriptions}),
        mimetype="application/json",
        status=200
    )

@chat.get("/prescription/<path:prescription_name>")
def download_prescription(prescription_name):
    return send_from_directory("static/prescriptions", prescription_name, as_attachment=True)

if __name__ == "__main__":
    chat.run(
        host = "0.0.0.0",
        port = 5001,
        debug=True
    )
