import os
from flask import Flask
from flask_cors import CORS
import SSS_test_analysis

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend running"

@app.route("/test", methods=["POST"])
def test():

    result = SSS_test_analysis.analyze()

    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))