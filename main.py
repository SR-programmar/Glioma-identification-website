import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

LOCAL_IMAGE = "local_image"

app.config["LOCAL_IMAGE"] = "local_image"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
os.makedirs(LOCAL_IMAGE, exist_ok=True)

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/upload_image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        file = request.files["file"]
        filepath = os.path.join(app.config["LOCAL_IMAGE"], file.filename)
        file.save(filepath)


    return redirect(url_for('home_page'))


@app.route("/retrieve_image/<filename>")
def retrieve_image(filename):
    return send_from_directory(app.config["LOCAL_IMAGE"], filename)

if __name__ == '__main__':
    app.run(debug=True)