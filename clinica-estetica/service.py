from flask import Flask, Response, request

from prescription_db import get_prescriptions_by_keys
from robot import *

import json

INFO = {
    "description": "Chatbot para clínicas de estética",
    "version": "0.0.1"
}

service = Flask(ROBOT_NAME)
robot_initialized, robot = init_robot()

@service.get("/")
def info():
    return Response(
        json.dumps(INFO),
        mimetype="application/json",
        status=200
    )

@service.post("/response")
def chat_response():
    if robot_initialized is False:
        return Response(
            json.dumps({"message": "O robô chatbot não foi inicializado corretamente"}),
            mimetype="application/json",
            status=500
        )
    
    request_data = request.get_json()
    robot_response = robot.get_response(request_data["question"])

    return Response(
        json.dumps({"response": robot_response.text, "confidence": robot_response.confidence}),
        mimetype="application/json",
        status=200
    )

@service.post("/prescriptions")
def get_prescriptions():
    request_data = request.get_json()
    success, message, prescriptions = get_prescriptions_by_keys(request_data["keys"])
    prescriptions_result = {}

    order = 1
    for prescription in prescriptions:
        prescriptions_result[prescription["id"]] = {
            "id": prescription["id"],
            "title": prescription["title"],
            "path": prescription["path"],
            "order": order
        }
        order = order + 1

    return Response(
        json.dumps({"prescriptions": list(prescriptions_result.values()), "message": message}),
        mimetype="application/json",
        status=200 if success else 500
    )

if __name__ == "__main__":
    service.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )