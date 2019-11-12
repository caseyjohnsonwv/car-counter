import os, db
from flask import Flask, redirect, session, request, render_template


app = Flask(__name__)
app.config.update(
    SECRET_KEY = os.environ.get("app_key", "app_key")
)


@app.route("/", methods=["GET"])
#main page with statistics
def hello():
    data = db.fetch(0)
    if data:
        id, carCount, totalCount, lastUpdate = data
        return render_template('main.html',totalCars=totalCount,lastUpdate=lastUpdate)
    else:
        return render_template('error.html')


@app.route("/reset", methods=["GET"])
#simple get request to reset car counter
def reset():
    db.reset(0)
    return redirect("/")


@app.route("/upload-data", methods=["POST"])
#route for HTTP POST request
def upload_data():
    try:
        request_key = request.form['upload_key']
    except Exception:
        return "ERROR: Request rejected."

    try:
        upload_key = os.environ['upload_key']
    except Exception:
        return "ERROR: Upload rejected."

    if upload_key != request_key:
        return "ERROR: Data mismatch."

    try:
        car_count = int(request.form['car_count'])
    except Exception:
        return "ERROR: Data not found."

    db.update(car_count, 0)

    return "Success"


if __name__ == "__main__":
    host = os.environ.get("host","127.0.0.1")
    port = os.environ.get("port", "5000")
    #db.drop_all()
    db.generate()
    print(db.view())
    app.run(host,port)
