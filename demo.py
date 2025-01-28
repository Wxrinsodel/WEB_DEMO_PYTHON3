from flask import Flask, request

app = Flask(__name__)

@app.route("/test/<value1>/<value2>")
def test_square(value1, value2):
    result = int(value1)**2 + int(value2)**2
    
    return f"<p> Answer is: {result}</p>"