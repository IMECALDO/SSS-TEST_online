from flask import Flask, request, render_template
import SSS_test_analysis

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])

def upload():
    file = request.files["audio"]

    file.save("recording.wav")

    result = SSS_test_analysis.analyze("recording.wav")

    return result

@app.route('/test', methods=['POST'])
def test():
    return "Python executed successfully"

if __name__ == "__main__":
    app.run(debug=True)