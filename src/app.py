from flask import Flask, request
import time

app = Flask(__name__)

@app.route('/fraud/detection', methods=['POST'])
def detect_fraud(userId):
    # Get the request data
    data = request.get_json()

    # Perform fraud detection logic here
    # ...

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

if __name__ == '__main__':
    app.run()