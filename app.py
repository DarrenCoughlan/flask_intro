from flask import Flask, render_template, url_for

# __name__ referencing this file
app = Flask(__name__)

# index route so when we browse to url we dont immediately just 404
@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
