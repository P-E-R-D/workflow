#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
from workflow import add as add_workflow

load_dotenv()

app = Flask(__name__)


class AddRequest(BaseModel):
    a: float
    b: float


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/add", methods=["POST"])
def add_route():
    json_data = request.get_json(silent=True)
    if json_data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    try:
        req = AddRequest(**json_data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    result = add_workflow(req.a, req.b)
    return jsonify({"result": result}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
