from flask import Flask, request, render_template
from flask_cors import CORS
import SSS_test_analysis
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["audio"]

    filepath = "recording.wav"
    file.save(filepath)

    result = SSS_test_analysis.analyze(filepath)

    return str(result)

if __name__ == "__main__":
    app.run()
