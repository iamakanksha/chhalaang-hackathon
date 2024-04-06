from flask import Flask, request
from utils import detect
import time

app = Flask(__name__)

@app.route('/fraud/detection', methods=['POST'])
def detect_fraud():
    # Get the request data
    data = request.get_json()
    # Perform fraud detection logic here
    # ...
    #detect(data)
    status = "ALERT";
    # Return the result
    rule_violated = ["RULE-001", "RULE-003"]; # replace with method to get rule violated
    if (rule_violated == None):
        status = "OK"  # or "ALERT" based on your logic

    result = {
        "status": status,
        "ruleViolated": rule_violated,
        "timestamp": str(int(time.time()))
    }

    return result


@app.route('/fraud', methods=['GET'])
def get_fraud():
    print("GET request received")

if __name__ == '__main__':
    app.run()