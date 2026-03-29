from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend running"

@app.route("/test", methods=["POST"])
def test():
    return "Python executed successfully"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)