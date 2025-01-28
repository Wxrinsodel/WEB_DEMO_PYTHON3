from flask import Flask, request
from flask import render_template
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

@app.route("/test/<value1>/<value2>")
def test_square(value1, value2):
    result = int(value1)**2 + int(value2)**2

    return f"<p> Answer is: {result}</p>"

@app.route("/calculate", methods=["POST"])
def calculate():
    value = int(request.form['number'])
    return render_template("calculator.html", result=value**2)

@app.route("/plot", methods=["GET", "POST"])
def plot():
    if request.method == "POST":
        xleft = int(request.form["xleft"])
        xright = int(request.form["xright"])

        x = np.linspace(xleft, xright, 100)
        y = np.sin(x)

        plt.plot(x, y)

        image_name = f"static/images/plot.png"
        plt.savefig(image_name)
        plt.close()
        return render_template("plotter.html", image_path=image_name)
    else:
        return render_template("plotter.html")