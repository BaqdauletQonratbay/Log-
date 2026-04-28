from flask import Flask, jsonify

app = Flask(__name__)

# Егер logs.txt жоқ болса — автоматты түрде жасайды
def create_sample_logs():
    sample_logs = """2026-04-28 19:10:23 INFO User login success
2026-04-28 19:11:02 ERROR Database connection failed
2026-04-28 19:12:45 WARNING High memory usage
2026-04-28 19:13:10 ERROR API timeout
2026-04-28 19:14:01 INFO Request processed
"""
    with open("logs.txt", "w") as f:
        f.write(sample_logs)


def analyze_logs(file_path):
    result = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "total": 0
    }

    try:
        with open(file_path, "r") as file:
            logs = file.readlines()
    except FileNotFoundError:
        create_sample_logs()
        with open(file_path, "r") as file:
            logs = file.readlines()

    for line in logs:
        result["total"] += 1

        if "INFO" in line:
            result["INFO"] += 1
        elif "WARNING" in line:
            result["WARNING"] += 1
        elif "ERROR" in line:
            result["ERROR"] += 1

    return result


@app.route("/")
def home():
    return """
    <h1>📊 Log Analyzer</h1>
    <p>Endpoint:</p>
    <ul>
        <li>/analyze - лог анализ жасау</li>
    </ul>
    """


@app.route("/analyze")
def analyze():
    data = analyze_logs("logs.txt")
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
