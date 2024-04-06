from app import app
from Flask import request
import time

@app.route('/fraud/detection', methods=['POST'])
def detect_fraud():
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