import os
from flask import Flask, request
from flask_cors import CORS
import SSS_test_analysis

app = Flask(__name__)
CORS(app)

@app.route("/health")
def health():
    return "OK"

@app.route("/test", methods=["POST"])
def test():
    audio = request.files["audio"]

    filename = audio.filename
    audio.save(filename)

    print(filename)

    result = SSS_test_analysis.analyze(filename)

    os.remove(filename)

    return f"PLV is: {result}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))